import csv
import os
from datetime import datetime
from typing import Optional


class CSVLogger:
    """
    Logs detection events to a CSV file.
    """

    def __init__(self, log_folder: str = "logs"):
        """
        Initialize the CSVLogger.
        
        Args:
            log_folder (str): The directory where the CSV log will be saved.
        """
        self.log_folder = log_folder
        os.makedirs(self.log_folder, exist_ok=True)
        self.log_file = os.path.join(self.log_folder, "detection_history.csv")
        
        self._initialize_csv()

    def _initialize_csv(self) -> None:
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Track_ID", "Class_Name", "Confidence"])

    def log(self, track_id: int, class_name: str, confidence: float) -> None:
        """
        Log a single detection event.
        
        Args:
            track_id (int): The tracker ID of the object (-1 if no tracker).
            class_name (str): The class name of the detected object.
            confidence (float): The confidence score of the detection.
        """
        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, track_id, class_name, f"{confidence:.2f}"])