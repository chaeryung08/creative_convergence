import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

# Mediapipe FaceMesh 기준 눈 랜드마크
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.20  # Eye Aspect Ratio 임계값

def set_ear_threshold(value: float):
    global EAR_THRESHOLD
    EAR_THRESHOLD = value

def calculate_ear(eye):
    """
    Eye Aspect Ratio (EAR) 계산
    """
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    if C == 0:
        return 0
    
    return (A + B) / (2.0 * C)

def detect_eye_state(frame):
    """
    frame: OpenCV BGR 이미지
    return: (state, avg_ear)
    state: "OPEN", "CLOSED", "NO_FACE"
    """
    if frame is None:
        return None, None
    
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
    ) as face_mesh:

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return "NO_FACE", None

        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        left_eye = np.array([
            [int(landmarks[i].x * w), int(landmarks[i].y * h)]
            for i in LEFT_EYE
        ])
        right_eye = np.array([
            [int(landmarks[i].x * w), int(landmarks[i].y * h)]
            for i in RIGHT_EYE
        ])

        left_eye = calculate_ear(left_eye)
        right_eye = calculate_ear(right_eye)

        ear = (calculate_ear(left_eye) + calculate_ear(right_eye)) / 2.0
        state = "CLOSED" if ear < EAR_THRESHOLD else "OPEN"

        return state, ear