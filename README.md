# 🛸 Smart Drone Detection & Surveillance System

![Banner](https://via.placeholder.com/1200x300.png?text=Smart+Drone+Detection+System)

![Status](https://img.shields.io/badge/Status-Stable%20%2F%20Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![YOLO](https://img.shields.io/badge/YOLO-11-yellow)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff69b4)
![Release](https://img.shields.io/badge/Release-v1.0.0-purple)

---

## 📖 Overview
The Smart Drone Detection & Surveillance System is a highly optimized, real-time AI-powered application designed to detect, track, and log unauthorized drones, aircraft, and birds. Built for production, it features a scalable Singleton pattern for memory-efficient inference, a robust computer vision pipeline, and a modern web dashboard.

## ✨ Features
- **Real-Time Webcam Tracking:** Live object detection utilizing ByteTrack for accurate frame-to-frame ID tracking.
- **Media Analysis:** Upload images and videos for instant YOLO11 inference and downloadable processed outputs.
- **Interactive Dashboard:** A full-featured Streamlit UI offering Analytics, Detection History, and a visual Screenshot Gallery.
- **Alert System:** Triggers on-screen popups and console alerts instantly when unauthorized drones are detected.
- **CSV Logging:** Automatically logs all unique detections (Timestamp, Track ID, Class, Confidence) into structured CSV files.

## 🛠 Tech Stack
- **Core AI**: Ultralytics YOLO11
- **Computer Vision**: OpenCV & ByteTrack
- **Frontend / UI**: Streamlit
- **Data Processing**: Pandas
- **Language**: Python 3.10+

## 🚀 Installation
**1. Clone the repository:**
```bash
git clone https://github.com/Krishna270704/smart-drone-detection-system.git
cd smart-drone-detection-system
```
**2. Create a virtual environment:**
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/macOS
```
**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

## 📂 Folder Structure
```text
smart-drone-detection-system/
├── app/
│   ├── detection/
│   │   ├── detector.py          # Core YOLO Singleton Wrapper
│   │   ├── image_detector.py    # Image inference logic
│   │   ├── video_detector.py    # Video inference & processing
│   │   └── webcam_detector.py   # Live tracking & OpenCV window
│   ├── services/
│   │   ├── alert_service.py     # Centralized alert system
│   │   ├── csv_logger.py        # Detection history exporter
│   │   └── logger.py            # Standardized console logging
│   └── config.py                # Global configurations
├── logs/                        # Auto-generated CSV and text logs
├── models/                      # Directory for YOLO weights (best.pt)
├── screenshots/                 # Auto-saved webcam captures
├── main.py                      # CLI Application Entrypoint
├── streamlit_app.py             # Streamlit Web Dashboard Entrypoint
├── requirements.txt             # Project Dependencies
└── packages.txt                 # Deployment dependencies
```

## 🏗 Project Architecture
The system is built on a highly decoupled Service-Oriented Architecture (SOA):
- **Singleton Model Cache:** The `DroneDetector` ensures the YOLO model is loaded into RAM only once, preventing memory bloat across the app.
- **Detection Core:** Independent detection controllers for images, video, and live webcam feeds ensuring single-responsibility patterns.
- **Service Layer:** Abstracts I/O functionality such as alert dispatching, CSV writing, and standardized logging.

## 📊 Dataset
The model was trained on a comprehensive custom dataset consisting of diverse weather conditions, altitudes, and lighting environments to ensure robust classification between `Drones`, `Birds`, and general `Aircraft`.

## 🧠 Model
Utilizes **YOLO11** (You Only Look Once), fine-tuned for high-speed edge inference. Weights are stored securely in `models/best.pt`. The model is integrated via Ultralytics' latest Python API, combining deep learning with ByteTrack for seamless object persistence.

## 🎮 Usage
Run the following command to start the interactive Streamlit UI:
```bash
streamlit run streamlit_app.py
```
*For terminal users, `python main.py` provides a lightweight CLI alternative.*

### 🖼 Image Detection
Navigate to the **Image Detection** tab. Upload a `.jpg` or `.png` to immediately receive bounded predictions and instant Drone alerts.

### 🎥 Video Detection
Navigate to the **Video Detection** tab. Upload an `.mp4` to process the stream frame-by-frame. The output is fully downloadable.

### 📹 Webcam Detection
Navigate to the **Webcam** tab to launch the optimized OpenCV live feed. The resolution is scaled for maximum FPS. Press `S` to capture a screenshot or `Q` to quit.

### 📊 Streamlit Dashboard
Features a highly-responsive cache-enabled UI. Includes:
- **Detection History:** Search, filter, and sort past detections.
- **Analytics:** View total counts and charts based on CSV logs.
- **Screenshot Gallery:** View all snapshots captured during live streams.

## 📸 Screenshots
*(Add your project screenshots here)*
- `![Dashboard](docs/dashboard.png)`
- `![Webcam](docs/webcam.png)`

## 🔮 Future Improvements
- Expand detection classes (e.g., specific drone models).
- Add SMS/Email integration via Twilio for off-site alerts.
- Migrate from CSV to PostgreSQL/Firebase for distributed analytics.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact
**Krishna**  
Senior AI Software Engineer & Full Stack Developer  
- **GitHub:** [Krishna270704](https://github.com/Krishna270704)
- **LinkedIn:** [Krishna](https://www.linkedin.com/in/krishna-104b6627a)