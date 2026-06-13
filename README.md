# 🛡️ AI Security Camera (Smart Surveillance System)

A real-time AI-powered security camera system built using Python and OpenCV that detects motion, captures evidence, records video, and logs events automatically.

This project simulates a smart CCTV system using Computer Vision.

---

# 🚀 Features

✅ Real-time motion detection using frame differencing  
✅ Automatic image capture on motion detection  
✅ Auto video recording during motion events  
✅ Face detection using Haar Cascades  
✅ Person detection using HOG descriptor  
✅ Timestamp-based activity logging  
✅ Live bounding boxes for motion, face, and person detection  
✅ On-screen security HUD (FPS, status, alerts)  
✅ Fully works using a normal webcam  

---

# 🛠️ Technologies Used

- Python 🐍  
- OpenCV (Computer Vision)  
- Haar Cascades (Face Detection)  
- HOG Descriptor (Person Detection)  
- OS Module (File Handling)  
- Datetime (Logging System)  

---

# 📦 Installation

```bash
git clone https://github.com/your-username/AI-Security-Camera.git
cd AI-Security-Camera
pip install opencv-python

▶️ Run the Project
python main.py

AI-Security-Camera/
│
├── main.py               # Main application
├── README.md
├── captures/             # Saved images on motion
├── recordings/          # Auto recorded videos
├── logs/                # Activity logs
└── videos/              # Optional storage

🎯 How It Works
Webcam captures live video
Frames are compared to detect motion
If motion is detected:
Bounding boxes are drawn
Image is saved automatically
Video recording starts
Event is logged with timestamp
Face and person detection runs in parallel
Live HUD shows system status
⌨️ Controls
Key	Action
q	Quit program