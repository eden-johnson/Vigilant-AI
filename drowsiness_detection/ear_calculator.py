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
