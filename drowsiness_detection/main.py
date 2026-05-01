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
