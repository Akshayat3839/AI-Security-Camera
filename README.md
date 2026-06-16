# AI Security Camera - Smart AI Surveillance System

A real-time AI-powered surveillance system built using Python and OpenCV that transforms a normal webcam into a smart security camera.

The system performs real-time motion detection, captures security evidence, records suspicious activities, detects faces and persons, and maintains automated event logs.

Additionally, an AI-based hand gesture writing module enables touchless interaction using real-time hand landmark tracking.

---

## Features

### Smart Surveillance System

- Real-time motion detection using frame differencing
- Automatic image capture during motion events
- Automatic video recording when suspicious activity is detected
- Face detection using Haar Cascade classifier
- Person detection using HOG descriptor
- Real-time bounding boxes for detected objects
- Timestamp-based security event logging
- Live security HUD displaying FPS, alerts, and system status
- Works with a standard webcam

### AI Gesture Writing Module

- Real-time hand tracking using MediaPipe
- Virtual writing using index finger movement
- Gesture-based interaction system
- One finger gesture for drawing
- Two finger gesture for erasing
- Three finger gesture for saving drawings
- Contactless computer interaction
- Real-time landmark visualization

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Haar Cascade Classifier
- HOG Descriptor
- Computer Vision
- Image Processing
- File Handling
- Event Logging System

---

## Project Architecture

```
AI-Security-Camera/

│
├── main.py                    # Main AI surveillance system
├── gesture_writing.py         # Basic virtual writing module
├── gesture_writing_v2.py      # Advanced gesture control module
│
├── captures/                  # Motion captured images
├── recordings/                # Recorded security videos
├── logs/                      # Activity logs
├── drawings/                  # Saved gesture drawings
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Security-Camera.git

cd AI-Security-Camera
```

### Install Dependencies

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

---

## Running the Project

### Start AI Security Camera

```bash
python main.py
```

### Start Gesture Writing Module

```bash
python gesture_writing_v2.py
```

---

## How It Works

### Surveillance Pipeline

```
Webcam Feed
      |
      ↓
Frame Processing
      |
      ↓
Motion Detection
      |
      ↓
Object Analysis
      |
      ├── Face Detection
      |
      ├── Person Detection
      |
      ├── Evidence Capture
      |
      └── Event Logging
```

### Gesture Writing Pipeline

```
Camera Input
      |
      ↓
Hand Landmark Detection
      |
      ↓
Finger Gesture Recognition
      |
      ↓
Virtual Canvas Interaction
      |
      ↓
Save / Erase / Draw Actions
```

---

## Controls

| Key | Action |
|-----|--------|
| Q | Quit application |
| C | Clear gesture drawing canvas |

---

## Output

The system automatically generates:

- Captured images during motion events
- Recorded security videos
- Activity logs with timestamps
- Saved virtual drawings

---

## Future Enhancements

- Face recognition-based authentication
- Email/SMS security alerts
- Cloud storage integration
- Multi-camera surveillance support
- AI-based threat detection
- Voice-controlled security commands
- Mobile application dashboard

---

## Project Highlights

- Built an end-to-end Computer Vision surveillance system
- Integrated multiple AI detection techniques
- Implemented real-time hand gesture interaction
- Designed modular architecture for future AI upgrades

---

## Author

**Akshaya**

AI & Machine Learning Enthusiast
