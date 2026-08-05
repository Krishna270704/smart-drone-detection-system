import os
from typing import Any
from app.detection.detector import DroneDetector
from app.services.logger import DetectionLogger


class VideoDetector:
    """
    Handles video-based detection.
    """

    def __init__(self):
        self.detector = DroneDetector()

    def detect_video(self, video_path: str) -> None:
        """
        Detect objects in a video.
        
        Args:
            video_path (str): The path to the video file.
        """
        if not os.path.exists(video_path):
            DetectionLogger.log(f"Video not found: {video_path}", level="ERROR")
            return

        DetectionLogger.log(f"Video Detection Started for: {video_path}", level="INFO")

        self.detector.detect(
            source=video_path,
            conf=0.25
        )

        DetectionLogger.log("Video Detection Completed Successfully", level="INFO")