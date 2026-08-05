import streamlit as st
import os
import pandas as pd
from PIL import Image
import tempfile


from app.detection.detector import DroneDetector
from app.config import MODEL_PATH
from app.services.alert_service import AlertService



st.set_page_config(
    page_title="Smart Drone Detection System",
    page_icon="🛸",
    layout="wide"
)

@st.cache_resource
def load_detector():
    """Cache the model so it doesn't reload on every UI interaction."""
    try:
        return DroneDetector()
    except Exception as e:
        return None

@st.cache_data(ttl=5)
def load_detection_data(csv_path: str) -> pd.DataFrame:
    """Load and cache the detection history CSV to prevent slow disk reads."""
    if os.path.exists(csv_path):
        try:
            return pd.read_csv(csv_path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


detector = load_detector()



st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Image Detection",
        "Video Detection",
        "Webcam",
        "Detection History",
        "Screenshot Gallery",
        "Analytics",
        "Settings",
        "About"
    ]
)


if "conf_threshold" not in st.session_state:
    st.session_state.conf_threshold = 0.25
if "save_result" not in st.session_state:
    st.session_state.save_result = True
if "tracker_toggle" not in st.session_state:
    st.session_state.tracker_toggle = True



if page == "Home":
    st.title("🛸 Smart Drone Detection & Surveillance System")
    st.markdown("### AI Powered Drone Detection using YOLO11")
    st.divider()

    st.header("Dashboard Overview")
    
    if detector is None:
        st.error("⚠️ Model file not found! Please ensure 'models/best.pt' exists. Check the terminal for more details.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", "YOLO11 Custom")
    with col2:
        st.metric("Total Classes", "3 (Drone, Bird, Aircraft)")
    with col3:
        status = "Ready ✅" if detector else "Error ❌"
        st.metric("Model Status", status)

    st.info("Navigate using the sidebar to explore detection modules, history, and analytics.")



elif page == "Image Detection":
    st.header("📷 Image Detection")
    
    if detector is None:
        st.error("Model is not loaded. Cannot perform detection.")
        st.stop()

    conf_slider = st.slider("Confidence Threshold", 0.0, 1.0, st.session_state.conf_threshold, 0.05)
    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", width="stretch")

        if st.button("Detect"):
            with st.spinner("Detecting objects..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    image.save(tmp.name)
                    tmp_path = tmp.name

                try:
                    results = detector.detect(source=tmp_path, conf=conf_slider)
                    
                    if results:
                        import cv2
                        res = results[0]
                        res_plotted = res.plot()
                        res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                        
                        st.image(res_rgb, caption="Detection Result", width="stretch")
                        
                        st.subheader("Detection Summary")
                        
                        if res.boxes is not None and len(res.boxes) > 0:
                            for box in res.boxes:
                                cls_id = int(box.cls[0])
                                cls_name = res.names[cls_id]
                                conf = float(box.conf[0])
                                
                                st.write(f"✅ **{cls_name}**: Confidence {conf:.2f}")
                                
                                if cls_name == "Drone":
                                    st.error("🚨 ALERT: DRONE DETECTED IN IMAGE! 🚨")
                                    AlertService.trigger_alert("DRONE DETECTED IN IMAGE")
                        else:
                            st.warning("No objects detected.")
                except Exception as e:
                    st.error(f"Detection failed: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)



elif page == "Video Detection":
    st.header("🎥 Video Detection")

    if detector is None:
        st.error("Model is not loaded. Cannot perform detection.")
        st.stop()

    uploaded = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if uploaded:
        if st.button("Detect"):
            with st.spinner("Processing video..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded.read())
                    tmp_path = tmp.name
                
                out_path = tmp_path.replace(".mp4", "_out.mp4")
                st_video_frame = st.empty()
                progress_bar = st.progress(0)
                
                try:
                    import cv2
                    results = detector.detect(source=tmp_path, conf=st.session_state.conf_threshold, stream=True)
                    writer = None
                    drone_alert_triggered = False

                    for idx, res in enumerate(results):

                        progress_bar.progress(min((idx % 100) / 100.0, 1.0))
                        
                        im_bgr = res.plot()
                        im_rgb = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2RGB)
                        st_video_frame.image(im_rgb, channels="RGB", width="stretch")
                        
                        if writer is None:
                            h, w, _ = im_bgr.shape
                            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                            writer = cv2.VideoWriter(out_path, fourcc, 30.0, (w, h))
                        
                        writer.write(im_bgr)
                        

                        if not drone_alert_triggered and res.boxes is not None:
                            for box in res.boxes:
                                cls_id = int(box.cls[0])
                                if res.names[cls_id] == "Drone":
                                    st.toast("🚨 ALERT: Drone detected in video stream!", icon="🚨")
                                    AlertService.trigger_alert("DRONE DETECTED IN VIDEO")
                                    drone_alert_triggered = True
                                    break
                    
                    if writer is not None:
                        writer.release()
                    
                    progress_bar.progress(1.0)
                    st.success("Video processing complete!")
                    
                    if os.path.exists(out_path):
                        with open(out_path, "rb") as file:
                            st.download_button(
                                label="Download Processed Video",
                                data=file,
                                file_name="processed_video.mp4",
                                mime="video/mp4"
                            )
                except Exception as e:
                    st.error(f"Error processing video: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    if os.path.exists(out_path):
                        os.remove(out_path)



elif page == "Webcam":
    st.header("📹 Webcam Detection")
    st.info("This will launch the desktop OpenCV window for webcam detection.")
    
    import sys
    if sys.platform == "linux":
        st.warning("⚠️ Webcam Detection is available only in the local desktop application.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_btn = st.button("Start Webcam")
        with col2:
            st.info("To stop the webcam, click on the video window and press 'q'.")
    
        if start_btn:
            try:

                from app.detection.webcam_detector import WebcamDetector
                
                st.warning("Webcam window opened. Press 'Q' inside the window to stop.")
                WebcamDetector().start()
                st.success("Webcam session ended.")
            except Exception as e:
                st.warning("⚠️ Webcam Detection is available only in the local desktop application.")
                st.error(f"Initialization failed: {e}")



elif page == "Detection History":
    st.header("📊 Detection History")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    csv_path = "logs/detection_history.csv"
    df = load_detection_data(csv_path)

    if not df.empty:

        col_search, col_sort, col_filter = st.columns(3)
        with col_search:
            search_term = st.text_input("🔍 Search Class Name (e.g., Drone)")
        with col_sort:
            sort_by = st.selectbox("Sort By", options=df.columns.tolist())
        with col_filter:
            filter_class = st.selectbox("Filter Class", ["All"] + df['Class_Name'].unique().tolist() if 'Class_Name' in df.columns else ["All"])


        if search_term:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            df = df[mask]
        
        if filter_class != "All" and 'Class_Name' in df.columns:
            df = df[df['Class_Name'] == filter_class]
            

        df = df.sort_values(by=sort_by, ascending=False)
        
        st.dataframe(df)
    else:
        st.warning(f"No Detection History found at {csv_path}. Run the webcam detector to generate logs.")



elif page == "Screenshot Gallery":
    st.header("📸 Screenshot Gallery")
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh Gallery"):
            st.rerun()

    folder = "screenshots"
    if os.path.exists(folder):
        files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))], reverse=True)
        if files:
            cols = st.columns(3)
            for idx, file in enumerate(files):
                path = os.path.join(folder, file)
                try:
                    img = Image.open(path)
                    with cols[idx % 3]:
                        st.image(img, caption=file, width="stretch")
                except Exception as e:
                    st.error(f"Could not load image {file}: {e}")
        else:
            st.info("No screenshots available in the folder.")
    else:
        st.warning("Screenshot folder not found. Take some screenshots during webcam detection!")



elif page == "Analytics":
    st.header("📈 Analytics")
    csv_path = "logs/detection_history.csv"
    df = load_detection_data(csv_path)

    if not df.empty:
        df_str = df.astype(str).apply(lambda x: x.str.lower())
        
        drone_count = (df_str == 'drone').sum().sum()
        bird_count = (df_str == 'bird').sum().sum()
        aircraft_count = (df_str == 'aircraft').sum().sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Drones", drone_count)
        col2.metric("Total Birds", bird_count)
        col3.metric("Total Aircrafts", aircraft_count)

        st.subheader("Detection Distribution")
        chart_data = pd.DataFrame({
            "Classes": ["Drone", "Bird", "Aircraft"],
            "Count": [drone_count, bird_count, aircraft_count]
        }).set_index("Classes")
        
        st.bar_chart(chart_data)
    else:
        st.warning("No data available for analytics (CSV missing or empty).")



elif page == "Settings":
    st.header("⚙️ Settings")
    
    st.session_state.conf_threshold = st.slider(
        "Confidence Threshold", 
        0.0, 1.0, 
        st.session_state.conf_threshold, 
        0.05
    )
    
    st.session_state.save_result = st.toggle("Save Detection Results", value=st.session_state.save_result)
    st.session_state.tracker_toggle = st.toggle("Enable Tracker", value=st.session_state.tracker_toggle)
    
    st.success("Settings applied temporarily for this session.")



elif page == "About":
    st.header("ℹ️ About Project")
    st.markdown("""
    ### Smart Drone Detection & Surveillance System
    
    **Tech Stack:**
    - Python
    - Streamlit
    - YOLO11 (Ultralytics)
    - OpenCV
    - ByteTrack
    
    **Features:**
    - Real-time Webcam Tracking
    - Image & Video Analysis
    - CSV Logging
    - Screenshot Capturing
    - Live Streamlit Dashboard
    
    **Developer:**
    Krishna Rajput
    """)