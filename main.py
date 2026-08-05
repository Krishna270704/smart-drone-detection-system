from app.detection.image_detector import ImageDetector
from app.detection.video_detector import VideoDetector
from app.detection.webcam_detector import WebcamDetector
from app.services.logger import DetectionLogger


def show_menu() -> None:
    """Displays the main application menu."""
    print("\n" + "=" * 50)
    print("      SMART DRONE DETECTION SYSTEM")
    print("=" * 50)
    print("1. Image Detection")
    print("2. Video Detection")
    print("3. Webcam Detection")
    print("4. Exit")
    print("=" * 50)


def main() -> None:
    """Main execution loop for the CLI application."""
    DetectionLogger.log("Application Started")

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                image_path = input("Enter image path: ")
                ImageDetector().detect_image(image_path)

            elif choice == "2":
                video_path = input("Enter video path: ")
                VideoDetector().detect_video(video_path)

            elif choice == "3":
                WebcamDetector().start()

            elif choice == "4":
                DetectionLogger.log("Application Closed")
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid Choice. Please try again.")
                
        except FileNotFoundError as e:
            DetectionLogger.log(f"File Error: {e}", level="ERROR")
            print(f"\n❌ Error: {e}")
        except RuntimeError as e:
            DetectionLogger.log(f"Runtime Error: {e}", level="ERROR")
            print(f"\n❌ Error: {e}")
        except Exception as e:
            DetectionLogger.log(f"Unexpected Error: {e}", level="ERROR")
            print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()