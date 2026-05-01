import threading
import time
import webview
import cv2
import os
import base64
from detector import DrowsinessDetector
from config import ALERT_SOUND

# Shared stop flag
stop_event = threading.Event()

class Api:
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def send_telemetry(self, ear, mar, status, alert_message, frame_b64=None):
        if self._window:
            if frame_b64:
                js_code = f"window.updateTelemetry({ear:.4f}, {mar:.4f}, '{status}', '{alert_message}', '{frame_b64}')"
            else:
                js_code = f"window.updateTelemetry({ear:.4f}, {mar:.4f}, '{status}', '{alert_message}')"
            try:
                self._window.evaluate_js(js_code)
            except Exception:
                pass


def on_closed():
    """Called by pywebview when window closes."""
    stop_event.set()


def run_vision_loop(api):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        api.send_telemetry(0.0, 0.0, "ERROR", "WEBCAM NOT FOUND")
        return

    detector = DrowsinessDetector(alert_sound=ALERT_SOUND)

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        annotated = detector.process_frame(frame)

        # Encode frame for UI
        small_frame = cv2.resize(annotated, (480, 360))
        ret_enc, buffer = cv2.imencode('.jpg', small_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        frame_b64 = base64.b64encode(buffer).decode('utf-8') if ret_enc else None

        api.send_telemetry(
            detector.current_ear,
            detector.current_mar,
            detector.current_status,
            detector.alert_message,
            frame_b64
        )

        time.sleep(0.03)

    cap.release()
    detector.release()

    if api._window:
        try:
            api._window.destroy()
        except Exception:
            pass


def main():
    api = Api()

    html_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'index.html')
    )

    window = webview.create_window(
        'Vigilant AI Co-Pilot',
        url=f'file:///{html_path.replace(os.sep, "/")}',
        js_api=api,
        width=1280,
        height=720,
        resizable=True,
        frameless=False
    )

    api.set_window(window)

    # Hook window close → set stop flag
    window.events.closed += on_closed

    vision_thread = threading.Thread(
        target=run_vision_loop, args=(api,), daemon=True
    )
    vision_thread.start()

    # debug=False fixes the recursion crash
    webview.start(debug=False)


if __name__ == '__main__':
    main()