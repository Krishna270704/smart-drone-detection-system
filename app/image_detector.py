import os
from app.detector import DroneDetector


class ImageDetector:
    def __init__(self):
        self.detector = DroneDetector()

    def detect_image(self, image_path):
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return

        print(f"🔍 Detecting objects in: {image_path}")

        results = self.detector.detect(
            source=image_path,
            conf=0.25
        )

        print("✅ Detection Complete")

        return results