# Vigilant AI 👁️🚙

**Vigilant AI** is an automotive-grade, real-time driver drowsiness and fatigue detection system. Built with a robust computer vision backend and a sleek, high-contrast native UI dashboard, it tracks facial landmarks to ensure drivers remain alert and safe on the road.

---

## ✨ Features

- **Real-Time Facial Tracking**: Utilizes Google MediaPipe's 468-point Face Mesh to calculate precise Eye Aspect Ratios (EAR) and Mouth Aspect Ratios (MAR).
- **Asynchronous Audio Alerts**: Triggers a non-blocking synthesized alarm the moment critical drowsiness or yawning thresholds are breached.
- **Native Desktop Dashboard**: A frameless, dark-mode native window powered by PyWebView, rendering a stunning HTML/CSS/JS telemetry UI without requiring a web browser.
- **Glanceable Telemetry**: SVG-based dynamic gauges that visually represent the driver's current Fatigue Index and Attention Level.
- **Critical Alert Overlays**: Full-screen 90% dimmed modals with pulsing neon borders that demand immediate driver intervention when fatigue is detected.

## 🛠️ Tech Stack

**Backend (Computer Vision)**
- Python 3.12
- OpenCV (`cv2`) for webcam stream processing
- Google MediaPipe (`mp.solutions.face_mesh`) for 3D facial landmark extraction
- SciPy for rapid Euclidean distance math
- Pygame-CE for asynchronous audio alert handling

**Frontend (Dashboard UI)**
- Vanilla HTML5 & CSS3
- Modern CSS Variables, Flexbox, and Keyframe Animations
- Vanilla Javascript for DOM manipulation and SVG stroke calculations
- PyWebView (Bridging the Python backend and HTML frontend)

---

## 🚀 Installation & Setup

Because this project relies on specific pre-compiled C++ binaries for facial tracking, **Python 3.12** is strongly recommended.

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/vigilant-ai.git
cd vigilant-ai
```

### 2. Set Up a Virtual Environment
```bash
py -3.12 -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Ensure you are using the exact versions specified in `requirements.txt` to maintain compatibility with the legacy MediaPipe solutions API.
```bash
cd drowsiness_detection
pip install -r requirements.txt
```

---

## 💻 Usage

To launch the Vigilant AI Dashboard, run the master script:

```bash
python app.py
```

1. The webcam will automatically initialize.
2. The native desktop dashboard will appear.
3. The system will immediately begin tracking your face.
4. **Test it out**: Close your eyes for roughly 1 second or mimic a large yawn to see the gauges react and trigger the critical alerts!

---

## ⚙️ Configuration

You can easily adjust the sensitivity of the AI by modifying `drowsiness_detection/config.py`:

```python
EAR_THRESHOLD = 0.25        # Increase to make eye-closure detection MORE sensitive
MAR_THRESHOLD = 0.60        # Decrease to make yawn detection MORE sensitive
EAR_CONSEC_FRAMES = 20      # Number of consecutive frames eyes must be closed to trigger an alert
```

---
*Built with safety in mind. Keep your eyes on the road!*
