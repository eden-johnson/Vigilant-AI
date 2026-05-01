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
