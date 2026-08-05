# System & Software Architecture

This document outlines the architectural design, data workflows, and AI model specifics of the Smart Drone Detection System.

---

## 1. Overall System Architecture

The system is designed with a monolithic, containerized architecture that bundles the frontend dashboard, backend services, and the AI inference engine into a single deployable unit.

```mermaid
graph TD
    User([User / Operator]) -->|HTTP/HTTPS| UI[Streamlit Dashboard]
    UI -->|Image/Video/Webcam| AppLogic[Application Logic]
    
    subgraph Containerized Application
        AppLogic -->|Inference Request| YOLO[YOLO11 Singleton Detector]
        YOLO -->|Bounded Boxes / IDs| AppLogic
        AppLogic -->|Log Event| CSVLog[(CSV Database)]
        AppLogic -->|Save Frame| Disk[(Screenshot Storage)]
        AppLogic -->|Trigger| Alert[Alert Service]
    end
    
    CSVLog -->|Query| UI
    Alert -->|Notification| User
```

---

## 2. Detection & Inference Pipeline

The core detection loop is highly optimized. It uses ByteTrack for temporal consistency across frames to ensure a single drone is not counted multiple times as it moves across the screen.

```mermaid
sequenceDiagram
    participant Camera as Video/Webcam Source
    participant Frame as Frame Resizer
    participant YOLO as YOLO11 Model
    participant Tracker as ByteTrack
    participant UI as Streamlit UI
    
    Camera->>Frame: Raw Frame (RTSP/Webcam)
    Frame->>YOLO: 640x640 Tensor
    YOLO->>Tracker: Detections (Class, Conf, BBox)
    Tracker->>Tracker: Assign Persistent IDs
    Tracker->>UI: Annotated Frame + Metadata
    UI->>UI: Render bounding boxes & FPS
```

---

## 3. Data & Logging Workflow

Every detection event generates structured data for analytics and forensics.

```mermaid
flowchart LR
    A[Inference Engine] -->|Drone Detected| B{New ID?}
    B -- Yes --> C[Write to CSV Logger]
    B -- No --> D[Ignore]
    
    C --> E[Timestamp]
    C --> F[Class Name]
    C --> G[Confidence Score]
    C --> H[Tracker ID]
    
    E & F & G & H --> I[(logs/detection_history.csv)]
    I --> J[Streamlit Analytics Engine]
```

---

## 4. Application Component Diagram

Illustrates the modular decoupling within the Python codebase.

```mermaid
graph TD
    subgraph UI Layer
        SA[streamlit_app.py]
    end

    subgraph Core Logic
        ID[image_detector.py]
        VD[video_detector.py]
        WD[webcam_detector.py]
        DD[detector.py - Singleton]
    end

    subgraph Services
        AL[alert_service.py]
        CL[csv_logger.py]
    end

    SA --> ID
    SA --> VD
    SA --> WD
    
    ID --> DD
    VD --> DD
    WD --> DD
    
    WD --> AL
    WD --> CL
```

---

## 5. Deployment Architecture

The application is containerized using Docker, allowing seamless deployment to Linux environments like Render or Hugging Face Spaces.

```mermaid
graph LR
    subgraph Cloud Environment [Render / Hugging Face]
        subgraph Docker Container [python:3.12-slim]
            OS[Debian OS Packages] --> |libgl1, libsm6| PyEnv[Python Environment]
            PyEnv --> |OpenCV Headless, Torch| Streamlit[Streamlit Server:7860]
        end
    end
    
    Internet((Internet)) -->|Port 7860| Streamlit
```

---

## 6. AI Model Documentation (YOLO11)

The system relies on Ultralytics YOLO11, the state-of-the-art in single-shot object detection.

### **Architecture Highlights**
- **Backbone:** CSPDarknet53 (Cross Stage Partial Network) for feature extraction.
- **Neck:** PANet (Path Aggregation Network) for multi-scale feature fusion.
- **Head:** Decoupled head for separate bounding box regression and object classification.

### **Inference Details**
- **Classes:** 0: Aircraft, 1: Bird, 2: Drone
- **Default Confidence Threshold:** 0.25 (Configurable via UI)
- **Tracking Algorithm:** ByteTrack (Configured via `bytetrack.yaml`)

### **Prediction Flow**
1. **Input:** Standardized to `640x640` spatial dimensions.
2. **Forward Pass:** The model outputs an Nx6 tensor (x_center, y_center, width, height, confidence, class).
3. **NMS (Non-Maximum Suppression):** Filters overlapping bounding boxes based on the IoU (Intersection over Union) threshold.
4. **Tracking:** ByteTrack associates detections in the current frame to existing tracklets from previous frames using Kalman Filters.
