import cv2
import os
import time
import platform
from datetime import datetime
from collections import deque

# ─── Directories ─────────────────────────────────────────────────────────────
os.makedirs("captures", exist_ok=True)
os.makedirs("recordings", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ─── Config ───────────────────────────────────────────────────────────────────
MOTION_THRESHOLD       = 1000
MOTION_PIXEL_THRESH    = 20
PHOTO_COOLDOWN_SEC     = 5
ALERT_COOLDOWN_SEC     = 3
VIDEO_RECORD_SECONDS   = 10
FRAME_BLUR             = (5, 5)
DISPLAY_FPS            = 30

# ─── Alert Sound ──────────────────────────────────────────────────────────────
def play_alert():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 200)
        elif platform.system() == "Darwin":
            os.system("afplay /System/Library/Sounds/Ping.aiff &")
        else:
            os.system("paplay /usr/share/sounds/freedesktop/stereo/bell.oga 2>/dev/null || true")
    except:
        pass

# ─── Logger ───────────────────────────────────────────────────────────────────
def log_event(event):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {event}"
    print(line)
    with open("logs/activity_log.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ─── FPS Counter ──────────────────────────────────────────────────────────────
class FPSCounter:
    def __init__(self, window=30):
        self.times = deque(maxlen=window)

    def tick(self):
        self.times.append(time.time())

    def fps(self):
        if len(self.times) < 2:
            return 0.0
        return (len(self.times) - 1) / (self.times[-1] - self.times[0])

# ─── Video Writer ─────────────────────────────────────────────────────────────
class VideoWriter:
    def __init__(self, path, fps, size):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(path, fourcc, fps, size)
        self.path = path
        self.active = True

    def write(self, frame):
        if self.active:
            self.writer.write(frame)

    def release(self):
        if self.active:
            self.writer.release()
            self.active = False
            log_event(f"📹 Video saved: {self.path}")

# ─── AI Models ────────────────────────────────────────────────────────────────
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))

def detect_persons(frame):
    small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    boxes, _ = hog.detectMultiScale(small, winStride=(8, 8), padding=(4, 4), scale=1.05)
    return [(x*2, y*2, w*2, h*2) for (x, y, w, h) in boxes]

# ─── HUD ──────────────────────────────────────────────────────────────────────
def draw_hud(frame, fps, motion, recording, faces, persons):
    h, w = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 40), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, ts, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 100, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    y = 70
    if motion:
        cv2.putText(frame, "MOTION DETECTED", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        y += 30

    if len(faces) > 0:
        cv2.putText(frame, f"FACES: {len(faces)}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 80, 0), 2)
        y += 30

    if len(persons) > 0:
        cv2.putText(frame, f"PERSONS: {len(persons)}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)

    if recording:
        cv2.circle(frame, (w - 20, 20), 8, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (w - 60, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    cv2.putText(frame, "Press Q to quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Camera not opened")
        return

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    cam_fps = cap.get(cv2.CAP_PROP_FPS)

    if cam_fps is None or cam_fps <= 1:
        cam_fps = DISPLAY_FPS

    print(f"✅ Camera opened: {frame_w}x{frame_h} @ {cam_fps}")

    log_event("System started")

    fps_counter = FPSCounter()
    prev_gray = None

    last_photo = 0
    last_alert = 0
    last_motion = 0

    video_writer = None
    frame_count = 0

    try:
        while True:

            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            frame = cv2.flip(frame, 1)
            fps_counter.tick()
            now = time.time()
            frame_count += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, FRAME_BLUR, 0)

            motion = False
            boxes = []

            if prev_gray is not None:
                diff = cv2.absdiff(prev_gray, gray)
                _, thresh = cv2.threshold(diff, MOTION_PIXEL_THRESH, 255, cv2.THRESH_BINARY)
                thresh = cv2.dilate(thresh, None, 2)

                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contours:
                    if cv2.contourArea(c) < MOTION_THRESHOLD:
                        continue
                    boxes.append(cv2.boundingRect(c))
                    motion = True

            prev_gray = gray

            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            faces = detect_faces(frame)

            persons = []
            if frame_count % 5 == 0:
                persons = detect_persons(frame)

            for (x, y, w, h) in persons:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 255), 2)

            # ─── ALERTS ─────────────────────────────
            if motion:
                last_motion = now

                if now - last_alert > ALERT_COOLDOWN_SEC:
                    play_alert()
                    last_alert = now

                if now - last_photo > PHOTO_COOLDOWN_SEC:
                    name = f"captures/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(name, frame)
                    log_event(f"📸 Saved {name}")
                    last_photo = now

                if video_writer is None:
                    vid = f"recordings/{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                    video_writer = VideoWriter(vid, cam_fps, (frame_w, frame_h))
                    log_event(f"🔴 Recording started {vid}")

            if video_writer:
                video_writer.write(frame)
                if now - last_motion > VIDEO_RECORD_SECONDS:
                    video_writer.release()
                    video_writer = None

            draw_hud(frame, fps_counter.fps(), motion, video_writer is not None, faces, persons)

            cv2.imshow("AI Security Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        if video_writer:
            video_writer.release()
        cap.release()
        cv2.destroyAllWindows()
        log_event("System closed")
        print("✅ System closed.")

if __name__ == "__main__":
    main()