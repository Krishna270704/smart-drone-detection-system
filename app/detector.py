from ultralytics import YOLO

class DroneDetector:
    def __init__(self, model_path="models/best.pt"):
        self.model = YOLO(model_path)

    def detect(self, source, conf=0.25):
        return self.model.predict(
            source=source,
            conf=conf,
            save=True
        )