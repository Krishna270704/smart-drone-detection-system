class AlertService:
    """
    Service responsible for triggering alerts when specific objects are detected.
    """

    @staticmethod
    def trigger_alert(message: str) -> None:
        """
        Trigger a console alert for a detected event.
        
        Args:
            message (str): The alert message to display.
        """
        print(f"\n{'=' * 40}")
        print(f"🚨 ALERT : {message.upper()} 🚨")
        print(f"{'=' * 40}\n")
