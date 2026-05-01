# Driver Drowsiness Detection — Core Code Logic

## Project Structure

```
drowsiness_detection/
├── main.py               # Entry point
├── detector.py           # Core detection logic
├── ear_calculator.py     # EAR/MAR math
├── alert.py              # Alert system
├── config.py             # Thresholds & constants
└── requirements.txt      # Dependencies
```

---

## requirements.txt

```
opencv-python
mediapipe
scipy
pygame
numpy
```

---

## config.py

```python
# Thresholds
EAR_THRESHOLD = 0.25        # Below this = eye closing
MAR_THRESHOLD = 0.60        # Above this = yawning
EAR_CONSEC_FRAMES = 20      # Frames before alert triggers
MAR_CONSEC_FRAMES = 15      # Frames of yawn before alert

# MediaPipe landmark indices (FaceMesh 468 points)
# Left eye
LEFT_EYE = [362, 385, 387, 263, 373, 380]
# Right eye
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
# Mouth (outer)
MOUTH = [61, 291, 39, 269, 0, 17]

# Alert sound path
ALERT_SOUND = "alert.wav"
```

---

## ear_calculator.py

```python
import numpy as np
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye_landmarks):
    """
    Calculate EAR for one eye.

    EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)

    Args:
        eye_landmarks: list of 6 (x, y) tuples

    Returns:
        float: EAR value (lower = more closed)
    """
    # Vertical distances
    A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
    # Horizontal distance
    C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])

    ear = (A + B) / (2.0 * C)
    return ear


def mouth_aspect_ratio(mouth_landmarks):
    """
    Calculate MAR for yawn detection.

    Args:
        mouth_landmarks: list of 6 (x, y) tuples

    Returns:
        float: MAR value (higher = more open)
    """
    A = dist.euclidean(mouth_landmarks[1], mouth_landmarks[5])
    B = dist.euclidean(mouth_landmarks[2], mouth_landmarks[4])
    C = dist.euclidean(mouth_landmarks[0], mouth_landmarks[3])

    mar = (A + B) / (2.0 * C)
    return mar


def extract_landmarks(face_landmarks, indices, frame_w, frame_h):
    """
    Extract (x, y) pixel coordinates from MediaPipe landmarks.

    Args:
        face_landmarks: MediaPipe face landmark result
        indices: list of landmark indices to extract
        frame_w: frame width in pixels
        frame_h: frame height in pixels

    Returns:
        list of (x, y) tuples
    """
    coords = []
    for idx in indices:
        lm = face_landmarks.landmark[idx]
        x = int(lm.x * frame_w)
        y = int(lm.y * frame_h)
        coords.append((x, y))
    return coords
```

---

## alert.py

```python
import pygame
import threading

class AlertSystem:
    def __init__(self, sound_path=None):
        pygame.mixer.init()
        self.sound_path = sound_path
        self.is_playing = False

        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
            except:
                self.sound = None
                print("[ALERT] Sound file not found. Using beep fallback.")
        else:
            self.sound = None

    def trigger(self, reason="DROWSINESS DETECTED"):
        """Play alert sound + print warning."""
        print(f"[!!!] ALERT: {reason}")
        if self.sound and not self.is_playing:
            self._play_async()

    def _play_async(self):
        def play():
            self.is_playing = True
            self.sound.play()
            pygame.time.wait(int(self.sound.get_length() * 1000))
            self.is_playing = False
        thread = threading.Thread(target=play, daemon=True)
        thread.start()

    def stop(self):
        if self.sound:
            self.sound.stop()
        self.is_playing = False
```

---

## detector.py

```python
import cv2
import mediapipe as mp
import numpy as np

from config import (
    LEFT_EYE, RIGHT_EYE, MOUTH,
    EAR_THRESHOLD, MAR_THRESHOLD,
    EAR_CONSEC_FRAMES, MAR_CONSEC_FRAMES
)
from ear_calculator import eye_aspect_ratio, mouth_aspect_ratio, extract_landmarks
from alert import AlertSystem


class DrowsinessDetector:
    def __init__(self, alert_sound=None):
        # MediaPipe setup
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Alert system
        self.alert = AlertSystem(alert_sound)

        # Frame counters
        self.eye_frame_count = 0
        self.yawn_frame_count = 0

        # State flags
        self.drowsy = False
        self.yawning = False

    def process_frame(self, frame):
        """
        Main processing pipeline per frame.

        Args:
            frame: BGR numpy array from OpenCV

        Returns:
            annotated frame with overlays
        """
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        status_text = "ALERT"
        status_color = (0, 255, 0)  # Green = alert

        if results.multi_face_landmarks:
            face_lms = results.multi_face_landmarks[0]

            # Extract coordinates
            left_eye  = extract_landmarks(face_lms, LEFT_EYE, w, h)
            right_eye = extract_landmarks(face_lms, RIGHT_EYE, w, h)
            mouth     = extract_landmarks(face_lms, MOUTH, w, h)

            # Calculate ratios
            left_ear  = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear   = (left_ear + right_ear) / 2.0
            mar       = mouth_aspect_ratio(mouth)

            # --- Drowsiness check ---
            if avg_ear < EAR_THRESHOLD:
                self.eye_frame_count += 1
                if self.eye_frame_count >= EAR_CONSEC_FRAMES:
                    self.drowsy = True
                    self.alert.trigger("EYES CLOSED TOO LONG")
                    status_text = "DROWSY!"
                    status_color = (0, 0, 255)  # Red
            else:
                self.eye_frame_count = 0
                self.drowsy = False

            # --- Yawn check ---
            if mar > MAR_THRESHOLD:
                self.yawn_frame_count += 1
                if self.yawn_frame_count >= MAR_CONSEC_FRAMES:
                    self.yawning = True
                    self.alert.trigger("YAWNING DETECTED")
                    status_text = "YAWNING!"
                    status_color = (0, 165, 255)  # Orange
            else:
                self.yawn_frame_count = 0
                self.yawning = False

            # Overlay metrics on frame
            self._draw_overlay(frame, avg_ear, mar, status_text, status_color)
            self._draw_eye_contours(frame, left_eye, right_eye)

        else:
            cv2.putText(frame, "NO FACE DETECTED", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return frame

    def _draw_overlay(self, frame, ear, mar, status, color):
        """Draw EAR, MAR, and status text on frame."""
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"MAR: {mar:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Status: {status}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    def _draw_eye_contours(self, frame, left_eye, right_eye):
        """Draw contours around both eyes."""
        for pts in [left_eye, right_eye]:
            hull = cv2.convexHull(np.array(pts))
            cv2.drawContours(frame, [hull], -1, (0, 255, 255), 1)

    def release(self):
        self.face_mesh.close()
        self.alert.stop()
```

---

## main.py

```python
import cv2
from detector import DrowsinessDetector
from config import ALERT_SOUND

def main():
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    detector = DrowsinessDetector(alert_sound=ALERT_SOUND)
    print("[INFO] Starting drowsiness detection. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame read failed.")
            break

        # Flip for mirror view
        frame = cv2.flip(frame, 1)

        # Run detection
        annotated = detector.process_frame(frame)

        cv2.imshow("Driver Drowsiness Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    detector.release()
    cv2.destroyAllWindows()
    print("[INFO] Session ended.")


if __name__ == "__main__":
    main()
```

---

## How to Run

```bash
# 1. Install dependencies
pip install opencv-python mediapipe scipy pygame numpy

# 2. Run
python main.py
```

---

## EAR Formula Diagram

```
Eye landmark positions:

        p2    p3
   p1            p4
        p6    p5

EAR = ( ||p2-p6|| + ||p3-p5|| ) / ( 2 * ||p1-p4|| )

EAR ~ 0.30  →  Eye open
EAR ~ 0.20  →  Eye closing
EAR < 0.25  →  DROWSY threshold
```

---

## Tuning Tips

| Parameter | Default | Adjust When |
|-----------|---------|-------------|
| `EAR_THRESHOLD` | 0.25 | Glasses/small eyes → lower to 0.20 |
| `EAR_CONSEC_FRAMES` | 20 | Too many false alarms → raise to 25 |
| `MAR_THRESHOLD` | 0.60 | Beard/moustache → raise to 0.70 |
| Camera FPS | 30 | Low FPS → reduce `EAR_CONSEC_FRAMES` |

---

## Known Limitations & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| False alerts with glasses | Glare on lens | Use IR camera or lower threshold |
| Missing face in low light | Detection fails | Add brightness normalization |
| High CPU usage | MediaPipe overhead | Reduce resolution to 480p |
| Alert keeps firing | No cooldown | Add 5s cooldown timer after alert |
