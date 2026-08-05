import os
from typing import Any, Optional
from ultralytics import YOLO
from app.config import MODEL_PATH, CONFIDENCE_THRESHOLD, SAVE_RESULTS


class DroneDetector:
    """
    Core detector wrapper for YOLO11 models utilizing a Singleton pattern
    to drastically reduce memory bloat and initialization times.
    """
    _instance = None
    _model = None

    def __new__(cls, model_path: str = MODEL_PATH):
        """Ensure only one instance of the detector exists."""
        if cls._instance is None:
            cls._instance = super(DroneDetector, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_path: str = MODEL_PATH):
        """
        Initialize the YOLO model (only once).
        
        Args:
            model_path (str): Path to the YOLO model file.
        """
        # Prevent re-initialization if the model is already loaded in memory
        if DroneDetector._model is None:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model exists.")
            
            # Using half=True if supported by device for memory reduction is handled intrinsically by YOLO
            DroneDetector._model = YOLO(model_path)

        self.model = DroneDetector._model

    def detect(self, source: Any, conf: Optional[float] = None, stream: bool = False, **kwargs) -> Any:
        """
        Run inference on the provided source.
        
        Args:
            source (Any): Image path, video path, or frame array.
            conf (float, optional): Confidence threshold. Defaults to config value.
            stream (bool): Whether to stream the results (useful for video/webcam).
            kwargs: Additional YOLO prediction arguments.
            
        Returns:
            Any: YOLO results object or generator if stream=True.
        """
        if conf is None:
            conf = CONFIDENCE_THRESHOLD

        return self.model.predict(
            source=source,
            conf=conf,
            stream=stream,
            save=SAVE_RESULTS,
            **kwargs
        )