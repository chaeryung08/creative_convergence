
import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [33, 160, 158, 133, 153, 144]

def calculate_ear(eye):
    """
    Eye Aspect Ratio (EAR) 계산
    """
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])

    if C == 0:
        return 0

    ear = (A + B) / (2.0 * C)
    return ear

def detect_eye_state(frame):
    """
    frame: OpenCV BGR 이미지
    return: "OPEN", "CLOSED", "NO_FACE"
    """
    if frame is None:
        return "UNKNOWN"
    
    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return "NO_FACE"

        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape

        left_eye = np.array([
            [int(landmarks[i].x * w), int(landmarks[i].y * h)]
            for i in LEFT_EYE
        ])

        ear = calculate_ear(left_eye)

        if ear < 0.20:
            return "CLOSED"
        else:
            return "OPEN"