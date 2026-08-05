import cv2
import os
import time
from datetime import datetime

from app.config import MODEL_PATH
from app.detection.detector import DroneDetector
from app.services.csv_logger import CSVLogger
from app.services.alert_service import AlertService
from app.services.logger import DetectionLogger


class WebcamDetector:
    """
    Handles live webcam detection, tracking, and UI display using OpenCV.
    """

    def __init__(self, model_path: str = MODEL_PATH):
        """
        Initialize the webcam detector.
        
        Args:
            model_path (str): Path to the YOLO model file (Passed to Singleton Detector).
        """
        self.detector = DroneDetector(model_path)
        self.model = self.detector.model
        
        self.csv_logger = CSVLogger()
        os.makedirs("screenshots", exist_ok=True)

        self.class_names = {
            0: "Aircraft",
            1: "Bird",
            2: "Drone"
        }

        # Prevent duplicate logging
        self.logged_ids = set()

    def start(self) -> None:
        """Starts the live webcam detection feed with optimized FPS."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise RuntimeError("Could not open webcam. Please ensure a camera is connected.")

        # Optimize Webcam Capture Resolution for FPS gain (640x480 standard)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        DetectionLogger.log("Webcam Started. Press 'S' to save screenshot, 'Q' to quit.", level="INFO")

        prev_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # ---------------- Tracking ---------------- #
            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False
            )

            annotated_frame = results[0].plot()

            # ---------------- FPS ---------------- #
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time < current_time else 0
            prev_time = current_time

            # ---------------- Counters ---------------- #
            drone_count = 0
            bird_count = 0
            aircraft_count = 0

            for result in results:
                if result.boxes is None:
                    continue

                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    track_id = int(box.id[0]) if box.id is not None else -1

                    class_name = self.class_names.get(class_id, "Unknown")

                    # Counter
                    if class_name == "Drone":
                        drone_count += 1
                    elif class_name == "Bird":
                        bird_count += 1
                    elif class_name == "Aircraft":
                        aircraft_count += 1

                    # CSV Logging & Alerts (Only Once Per Track ID)
                    if track_id != -1 and track_id not in self.logged_ids:
                        self.logged_ids.add(track_id)
                        self.csv_logger.log(track_id, class_name, confidence)

                        DetectionLogger.log(f"ID:{track_id} {class_name} {confidence:.2f}", level="INFO")

                        if class_name == "Drone":
                            AlertService.trigger_alert("DRONE DETECTED")

            # ---------------- Dashboard ---------------- #
            cv2.putText(annotated_frame, f"FPS : {int(fps)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Drone : {drone_count}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(annotated_frame, f"Bird : {bird_count}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(annotated_frame, f"Aircraft : {aircraft_count}", (20, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            cv2.imshow("Smart Drone Detection System", annotated_frame)
            key = cv2.waitKey(1) & 0xFF

            # Screenshot
            if key == ord("s"):
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
                path = os.path.join("screenshots", filename)
                cv2.imwrite(path, annotated_frame)
                DetectionLogger.log(f"Screenshot Saved : {path}", level="INFO")

            # Quit
            elif key == ord("q"):
                DetectionLogger.log("Closing Webcam...", level="INFO")
                break

        cap.release()
        cv2.destroyAllWindows()