import cv2
import time
import mediapipe as mp

from my_frontend.algorithm.eye_detect import detect_eye_state
from my_frontend.algorithm.head_pose import get_head_pose
from my_frontend.algorithm.drowsiness import DrowsinessDetector


def main():
    cap = cv2.VideoCapture(0)

    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True
    )

    detector = DrowsinessDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            cv2.imshow("Drowsiness", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        landmarks = result.multi_face_landmarks[0]

        eye_state, ear = detect_eye_state(landmarks, w, h)
        pitch, yaw = get_head_pose(landmarks, w, h)

        out = detector.update(
            ear=ear,
            eye_state=eye_state,
            pitch=pitch,
            timestamp=time.time()
        )

        # ===== 화면 출력 =====
        y = 30
        for key in [
            "state", "score",
            "ear", "avg_ear",
            "perclos", "blink_count",
            "blink_drop", "pitch"
        ]:
            value = out[key]
            text = f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}"
            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            y += 25

        cv2.imshow("Drowsiness", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
