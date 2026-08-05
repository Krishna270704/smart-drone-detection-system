import os
from datetime import datetime


class DetectionLogger:
    """
    General application logger for system events and detection lifecycle.
    """
    LOG_FOLDER = "logs"
    LOG_FILE = os.path.join(LOG_FOLDER, "detection.log")

    @classmethod
    def initialize(cls) -> None:
        """Ensure the log directory exists."""
        os.makedirs(cls.LOG_FOLDER, exist_ok=True)

    @classmethod
    def log(cls, message: str, level: str = "INFO") -> None:
        """
        Log a system message to the console and log file.
        
        Args:
            message (str): The message to log.
            level (str): The log level (e.g., INFO, ERROR, WARNING).
        """
        cls.initialize()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{now}] [{level.upper()}] {message}"
        
        print(log_message)
        
        with open(cls.LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_message + "\n")