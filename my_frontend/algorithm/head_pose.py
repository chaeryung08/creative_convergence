import cv2
import numpy as np

# MediaPipe FaceMesh landmark index
NOSE_TIP = 1
CHIN = 152
LEFT_EYE = 33
RIGHT_EYE = 263
LEFT_MOUTH = 61
RIGHT_MOUTH = 291


def estimate_head_pose(landmarks, image_shape):
    """
    return: (pitch, yaw, roll) in degrees
    """
    image_h, image_w = image_shape[:2]

    image_points = np.array([
        (landmarks[NOSE_TIP].x * image_w, landmarks[NOSE_TIP].y * image_h),
        (landmarks[CHIN].x * image_w, landmarks[CHIN].y * image_h),
        (landmarks[LEFT_EYE].x * image_w, landmarks[LEFT_EYE].y * image_h),
        (landmarks[RIGHT_EYE].x * image_w, landmarks[RIGHT_EYE].y * image_h),
        (landmarks[LEFT_MOUTH].x * image_w, landmarks[LEFT_MOUTH].y * image_h),
        (landmarks[RIGHT_MOUTH].x * image_w, landmarks[RIGHT_MOUTH].y * image_h),
    ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -63.6, -12.5),
        (-43.3, 32.7, -26.0),
        (43.3, 32.7, -26.0),
        (-28.9, -28.9, -24.1),
        (28.9, -28.9, -24.1)
    ])

    focal_length = image_w
    center = (image_w / 2, image_h / 2)

    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return None

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

    sy = np.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2)

    pitch = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    yaw = np.arctan2(-rotation_matrix[2, 0], sy)
    roll = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

    return (
        np.degrees(pitch),
        np.degrees(yaw),
        np.degrees(roll)
    )
