import numpy as np

# MediaPipe FaceMesh 기준 눈 랜드마크 인덱스
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def _distance(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)
    return np.linalg.norm([x1 - x2, y1 - y2])


def _ear(landmarks, eye_idx, w, h):
    lm = landmarks.landmark

    A = _distance(lm[eye_idx[1]], lm[eye_idx[5]], w, h)
    B = _distance(lm[eye_idx[2]], lm[eye_idx[4]], w, h)
    C = _distance(lm[eye_idx[0]], lm[eye_idx[3]], w, h)

    return (A + B) / (2.0 * C)


def detect_eye_state(landmarks, w, h):
    left_ear = _ear(landmarks, LEFT_EYE, w, h)
    right_ear = _ear(landmarks, RIGHT_EYE, w, h)
    ear = (left_ear + right_ear) / 2.0

    eye_state = "CLOSED" if ear < 0.21 else "OPEN"

    return eye_state, ear
