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
        self.current_ear = 0.30
        self.current_mar = 0.0
        self.current_status = "OPTIMAL"
        self.alert_message = ""

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

            self.current_ear = avg_ear
            self.current_mar = mar
            self.alert_message = ""
            self.current_status = "OPTIMAL"

            # --- Drowsiness check ---
            if avg_ear < EAR_THRESHOLD:
                self.eye_frame_count += 1
                if self.eye_frame_count >= EAR_CONSEC_FRAMES:
                    self.drowsy = True
                    self.alert.trigger("EYES CLOSED TOO LONG")
                    status_text = "DROWSY!"
                    self.current_status = status_text
                    self.alert_message = "EYES CLOSED TOO LONG"
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
                    self.current_status = status_text
                    self.alert_message = "YAWNING DETECTED"
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
            self.current_status = "NO FACE"
            self.alert_message = ""
            self.current_ear = 0.0
            self.current_mar = 0.0

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
