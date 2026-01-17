import numpy as np

NOSE_TIP = 1
CHIN = 152
LEFT_EYE = 33
RIGHT_EYE = 263


def get_head_pose(landmarks, w, h):
    lm = landmarks.landmark

    nose = lm[NOSE_TIP]
    chin = lm[CHIN]
    left_eye = lm[LEFT_EYE]
    right_eye = lm[RIGHT_EYE]

    # 필요한 좌표만 계산
    nose_x, nose_y = nose.x * w, nose.y * h
    chin_y = chin.y * h
    left_x = left_eye.x * w
    right_x = right_eye.x * w

    # ===== Pitch (위/아래) =====
    vertical_dist = chin_y - nose_y
    pitch = np.clip((vertical_dist - 80) * 0.5, -40, 40)

    # ===== Yaw (좌/우) =====
    eye_center_x = (left_x + right_x) / 2
    yaw = np.clip((nose_x - eye_center_x) * 0.3, -40, 40)

    return pitch, yaw
