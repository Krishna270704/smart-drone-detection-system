from app.detector import DroneDetector

detector = DroneDetector()

print("Model Loaded Successfully ✅")

from app.image_detector import ImageDetector

detector = ImageDetector()

detector.detect_image("test_images/test.jpg")

detector.detect_image("test_images/drone.jpg")