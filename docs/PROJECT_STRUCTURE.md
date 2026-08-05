# Project Structure & Architecture Guide

This document provides a comprehensive breakdown of the Smart Drone Detection System's folder structure, explaining the responsibilities of each module and file.

---

## 📁 Root Directory Layout

```text
smart-drone-detection-system/
├── app/                        # Application Source Code
├── datasets/                   # YOLO Training Data (Ignored in Git)
├── docs/                       # Project Documentation
├── logs/                       # Application & Detection Logs
├── models/                     # Trained YOLO Weights
├── screenshots/                # Automatically Captured Frames
├── tests/                      # Unit & Integration Testing
├── .dockerignore               # Docker build exclusions
├── .gitignore                  # Git commit exclusions
├── Dockerfile                  # Production container definition
├── LICENSE                     # MIT License
├── packages.txt                # System-level Linux dependencies (Apt)
├── README.md                   # Main Project Overview
├── requirements.txt            # Python Package Dependencies
├── runtime.txt                 # Python version specifier for cloud
└── streamlit_app.py            # Streamlit Application Entry Point
```

---

## 🧩 The `app/` Directory Breakdown

The `app` directory contains the core logic of the system, designed with separation of concerns.

### `app/config.py`
**Responsibility:** Global Configuration Management.
- Centralizes all magic numbers and paths.
- Defines confidence thresholds, logging directories, and model paths.
- Allows for easy configuration changes without digging through business logic.

### `app/detection/`
**Responsibility:** Inference and Computer Vision Wrappers.
- **`detector.py`:** Contains the `DroneDetector` class. Implements a **Singleton Pattern** to ensure the YOLO model is only loaded into memory once, preventing Out-Of-Memory (OOM) crashes during page navigation.
- **`image_detector.py` / `video_detector.py`:** Wrappers for processing static assets. Handles file I/O, resizing, and feeding frames to the singleton detector.
- **`webcam_detector.py`:** Handles the live OpenCV video capture. Integrates Ultralytics ByteTrack for persistent ID tracking and draws bounded boxes, FPS counters, and analytics onto the live stream.

### `app/services/`
**Responsibility:** Background Utilities and I/O Operations.
- **`alert_service.py`:** Monitors inference output. If a class `Drone` is detected, it triggers console/system alerts. Decoupled from detection logic to allow future SMS/Email integrations.
- **`csv_logger.py`:** Formats and writes detection events (Timestamp, ID, Class, Confidence) to `logs/detection_history.csv` for the Streamlit dashboard to consume.
- **`logger.py`:** Standard application event logger (Startup, Errors, Status changes).

### `app/utils/` (and `utils.py`)
**Responsibility:** Helper Functions.
- Contains generic helper methods (e.g., directory creation, file validation) that don't belong to a specific business domain.

---

## 🌐 The Presentation Layer

### `streamlit_app.py`
**Responsibility:** The Frontend UI and Dashboard State.
- Serves as the main execution script (`streamlit run streamlit_app.py`).
- Implements Streamlit's sidebar navigation.
- **Routing:** Directs user flow between Home, Image Detection, Video Detection, Webcam, History, and Analytics.
- **Lazy Loading:** Crucially, it imports hardware-dependent modules (like `cv2` and `webcam_detector`) *only* when the user clicks the Webcam module. This prevents deployment crashes on cloud instances lacking camera drivers.

---

## 🛠 DevOps & Deployment Files

### `Dockerfile`
- Multi-stage build based on `python:3.12-slim`.
- Installs necessary OS-level shared libraries (`libgl1`, `libsm6`) required by OpenCV.
- Configures environment variables and exposes ports for Hugging Face Spaces / Render.

### `requirements.txt` & `packages.txt`
- `requirements.txt`: Pins `opencv-python-headless` (critical for headless Linux servers) and `ultralytics`.
- `packages.txt`: A specialized file (often used by Streamlit Community Cloud) to install `apt-get` packages before `pip` installs.

---

## 🧠 Design Patterns Utilized

1. **Singleton Pattern:** Applied to the YOLO Model loading to preserve RAM.
2. **Facade Pattern:** The `app/detection` modules act as a simplified facade over the complex `ultralytics` API.
3. **Observer/Pub-Sub Pattern (Lightweight):** The `alert_service` effectively "listens" to the output of the detection loops.
