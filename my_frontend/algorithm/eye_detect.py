import cv2
import numpy as np

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.2


def set_ear_threshold(value: float):
    global EAR_THRESHOLD
    EAR_THRESHOLD = value


def calculate_ear(eye: np.ndarray) -> float:
    if not isinstance(eye, np.ndarray):
        return 0.0
    if eye.shape != (6, 2):
        return 0.0

    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])

    if C == 0:
        return 0.0

    return (A + B) / (2.0 * C)


def detect_eye_state(frame, face_mesh):
    if frame is None or face_mesh is None:
        return "NO_FRAME", None

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "NO_FACE", None

    landmarks = results.multi_face_landmarks[0].landmark
    if len(landmarks) < 468:
        return "NO_FACE", None

    h, w = frame.shape[:2]

    left_eye = np.array(
        [[int(landmarks[i].x * w), int(landmarks[i].y * h)] for i in LEFT_EYE],
        dtype=np.float32
    )
    right_eye = np.array(
        [[int(landmarks[i].x * w), int(landmarks[i].y * h)] for i in RIGHT_EYE],
        dtype=np.float32
    )

    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)

    if left_ear == 0.0 or right_ear == 0.0:
        return "UNKNOWN", None

    ear = (left_ear + right_ear) / 2.0
    state = "CLOSED" if ear < EAR_THRESHOLD else "OPEN"

    return state, ear
