<div align="center">

# 🛸 Smart Drone Detection & Surveillance System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLO11](https://img.shields.io/badge/YOLO11-Ultralytics-yellow.svg?style=for-the-badge&logo=yolo&logoColor=white)](https://ultralytics.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5.0+-green.svg?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg?style=for-the-badge)](LICENSE)

*An advanced, AI-powered computer vision system for real-time aerial threat detection, tracking, and analytics.*

[**Live Demo**](#live-demo) • [**Documentation**](#documentation) • [**Deployment**](#deployment-guide) • [**Contributing**](CONTRIBUTING.md)

</div>

---

## 📑 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Deployment Guide](#deployment-guide)
- [Future Scope](#future-scope)
- [License](#license)
- [Contact](#contact)

---

## 📖 Overview

The **Smart Drone Detection & Surveillance System** is a robust, end-to-end computer vision application designed to detect and track aerial objects—specifically distinguishing between drones, birds, and aircraft. Built with a custom-trained **YOLO11** model, it provides high-precision inference across images, recorded videos, and live webcam streams.

This system is engineered with a modular, production-ready architecture, featuring a dynamic Streamlit dashboard for monitoring, historical analytics, and automated alerting.

---

## 🎯 Problem Statement

The rapid proliferation of consumer and commercial drones poses significant security risks to restricted airspaces, critical infrastructure, and privacy. Traditional radar systems often fail to detect small, low-flying UAVs, and distinguishing a drone from a bird remains a complex challenge for conventional surveillance cameras. 

There is a critical need for an automated, AI-driven visual detection system capable of real-time classification and tracking of aerial objects.

---

## 💡 Solution

This project solves the aerial surveillance problem by deploying a highly optimized, state-of-the-art Deep Learning object detection model (YOLO11). The system:
- **Classifies** objects into three categories: Drone, Bird, and Aircraft.
- **Tracks** movement trajectories using ByteTrack to prevent duplicate counting.
- **Alerts** operators instantly upon drone detection.
- **Logs** all events into a structured CSV database for forensic analysis.
- **Visualizes** system health and analytics through an interactive web dashboard.

---

## ✨ Features

- **Real-Time Video Analytics:** Process live RTSP/Webcam feeds with zero-latency inference.
- **Batch Processing:** Upload and analyze static images or recorded MP4/AVI videos.
- **Advanced Object Tracking:** Integrated ByteTrack for persistent ID assignment across video frames.
- **Singleton Inference Engine:** Highly optimized memory management ensuring the model is loaded only once.
- **Automated Event Logging:** Comprehensive CSV logging of detection timestamps, confidence scores, and tracker IDs.
- **Screenshot Gallery:** Automated frame capturing during critical detection events.
- **Interactive Dashboard:** Beautiful, responsive UI built with Streamlit for seamless operator control.
- **Cloud Ready:** Fully containerized with Docker, deployable to Render, Hugging Face Spaces, and AWS.

---

## 🛠 Tech Stack

**Core AI & Vision**
- `Ultralytics YOLO11` - Object Detection & Tracking
- `PyTorch` - Deep Learning Backend
- `OpenCV-Python` - Image Processing & Video I/O

**Application & UI**
- `Streamlit` - Frontend Dashboard & State Management
- `Pandas` - Data Aggregation & Analytics
- `Pillow` - Image Manipulation

**DevOps & Deployment**
- `Docker` - Containerization
- `Render / Hugging Face` - Cloud Hosting

---

## 📁 Folder Structure

A quick glance at the repository architecture. For a deep dive, see [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

```text
smart-drone-detection-system/
├── app/                        # Core application modules
│   ├── config.py               # Global configuration variables
│   ├── detection/              # Inference wrappers (Image, Video, Webcam)
│   └── services/               # Background services (Logging, Alerts)
├── datasets/                   # (Ignored) Training data (Images/Labels)
├── docs/                       # Comprehensive documentation & architecture
├── logs/                       # Generated CSV detection logs
├── models/                     # Trained YOLO weights (best.pt)
├── screenshots/                # Auto-saved detection frames
├── tests/                      # Unit and integration tests
├── Dockerfile                  # Production container definition
├── requirements.txt            # Python dependencies
└── streamlit_app.py            # Main application entry point
```

---

## 💻 System Requirements

**Local Execution (Windows/Linux/Mac):**
- Python 3.10 to 3.12
- 4GB+ RAM (8GB Recommended)
- Webcam (Required for live detection module)
- *Optional:* NVIDIA GPU (CUDA Toolkit 11.8+) for accelerated inference

**Cloud Deployment:**
- Docker Engine
- 2GB+ RAM Container Instance

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Krishna270704/smart-drone-detection-system.git
cd smart-drone-detection-system
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Note: The repository uses `opencv-python-headless` to ensure cloud compatibility. If you plan to use the local webcam module on Windows, you may install `opencv-python` instead).*

---

## 🚀 Usage

Start the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

**Modules Available:**
1. **Home:** System status and model health.
2. **Image Detection:** Upload images for instant classification.
3. **Video Detection:** Process MP4s and download annotated results.
4. **Webcam:** Launch local desktop live-feed with ByteTrack.
5. **Detection History:** Search, filter, and sort the CSV logs.
6. **Analytics:** View aggregate detection metrics.

---

## 📸 Screenshots

*(Replace these placeholders with actual screenshots from your running app)*

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=Dashboard+Overview" alt="Dashboard Overview" width="80%">
  <p><i>Figure 1: Main Dashboard and System Status</i></p>
  
  <img src="https://via.placeholder.com/800x400?text=Live+Webcam+Detection" alt="Webcam Detection" width="80%">
  <p><i>Figure 2: Real-time tracking of aerial objects</i></p>
</div>

---

## 🌐 Live Demo

*(Insert link when deployed)*
**Check out the live deployment here: [Coming Soon]**

---

## ☁️ Deployment Guide

The system is fully containerized and cloud-ready. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for deployment architecture details.

### Deploying via Docker (Local)
```bash
docker build -t drone-detector .
docker run -p 7860:7860 drone-detector
```

### Deploying to Render
1. Connect your GitHub repository to Render.
2. Create a new **Web Service**.
3. Environment: `Docker`.
4. Render will automatically detect the `Dockerfile` and configure the `$PORT`.

### Deploying to Hugging Face Spaces
1. Create a new Docker space.
2. Push the repository contents.
3. The Space will automatically expose port `7860` as defined in the Dockerfile.

---

## 🔭 Future Scope

- **Audio Integration:** Combine vision with acoustic sensors for drone rotor noise detection.
- **PTZ Camera Control:** Output tracking coordinates to physically move Pan-Tilt-Zoom cameras.
- **Night Vision / Thermal:** Train secondary models on IR datasets for 24/7 operability.
- **Edge Deployment:** Convert models to TensorRT/ONNX for deployment on NVIDIA Jetson Nanos.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**Krishna Rajput**  
AI Engineer & Developer  
GitHub: [@Krishna270704](https://github.com/Krishna270704)