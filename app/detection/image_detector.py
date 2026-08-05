import os
from typing import Any
from app.detection.detector import DroneDetector
from app.services.logger import DetectionLogger


class ImageDetector:
    """
    Handles image-based detection.
    """

    def __init__(self):
        self.detector = DroneDetector()

    def detect_image(self, image_path: str) -> Any:
        """
        Detect objects in an image.
        
        Args:
            image_path (str): The path to the image file.
            
        Returns:
            Any: YOLO results or None if file not found.
        """
        if not os.path.exists(image_path):
            DetectionLogger.log(f"Image not found: {image_path}", level="ERROR")
            return None

        DetectionLogger.log(f"Image Detection Started for: {image_path}", level="INFO")

        results = self.detector.detect(
            source=image_path,
            conf=0.25
        )

        DetectionLogger.log("Image Detection Completed Successfully", level="INFO")

        return results