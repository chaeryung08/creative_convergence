import cv2
import time
import csv
import mediapipe as mp
import numpy as np
from collections import deque

from .eye_detect import detect_eye_state, set_ear_threshold
from .head_pose import estimate_head_pose

LOG_FILE = "drowsiness_log.csv"


def main():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )

    cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30

    # ================= 기준 =================
    CLOSED_FRAME_THRESHOLD = int(fps * 2.0)
    BLINK_WINDOW = 60
    PERCLOS_WINDOW = 60
    BASELINE_TIME = 60

    # ================= 상태 =================
    closed_frames = 0
    blink_closed_frames = 0

    blink_times = deque()
    frame_states = deque()

    baseline_blinks = []
    baseline_start = time.time()
    baseline_blink_rate = None

    # ================= EAR 캘리브레이션 =================
    CALIBRATION_TIME = 5
    ear_samples = []
    calibrated = False
    calibration_start = time.time()

    # ================= EAR 재보정 =================
    EAR_RECAL_WINDOW = 60
    ear_history = deque()
    avg_ear = None

    # ================= CSV =================
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "EAR", "eye_state",
            "blink_1min", "blink_drop",
            "perclos", "head_pitch",
            "drowsy_level", "state"
        ])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()

        # -------- FaceMesh --------
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        landmarks = None
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

        # -------- Eye state --------
        state, ear = detect_eye_state(frame, face_mesh)

        # ===== 초기 EAR 캘리브레이션 =====
        if not calibrated:
            if ear is not None:
                ear_samples.append(ear)

            if now - calibration_start >= CALIBRATION_TIME and ear_samples:
                avg_ear = sum(ear_samples) / len(ear_samples)
                set_ear_threshold(avg_ear * 0.75)
                calibrated = True

            cv2.putText(frame, "Calibrating EAR...",
                        (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)
            cv2.imshow("Drowsiness", frame)
            cv2.waitKey(1)
            continue

        # ===== Blink detection =====
        if state == "CLOSED":
            blink_closed_frames += 1
        else:
            if 1 <= blink_closed_frames <= int(fps * 0.3):
                blink_times.append(now)
                if baseline_blink_rate is None:
                    baseline_blinks.append(now)
            blink_closed_frames = 0

        while blink_times and now - blink_times[0] > BLINK_WINDOW:
            blink_times.popleft()

        blink_count = len(blink_times)

        if baseline_blink_rate is None and now - baseline_start >= BASELINE_TIME:
            baseline_blink_rate = len(baseline_blinks)

        blink_drop = 0.0
        if baseline_blink_rate and baseline_blink_rate > 0:
            blink_drop = np.clip(
                (baseline_blink_rate - blink_count) / baseline_blink_rate,
                0, 1
            )

        # ===== Long close =====
        closed_frames = closed_frames + 1 if state == "CLOSED" else 0
        long_close_ratio = np.clip(
            closed_frames / CLOSED_FRAME_THRESHOLD, 0, 1
        )

        # ===== PERCLOS =====
        frame_states.append((now, state))
        while frame_states and now - frame_states[0][0] > PERCLOS_WINDOW:
            frame_states.popleft()

        perclos = (
            sum(1 for _, s in frame_states if s == "CLOSED") / len(frame_states)
            if frame_states else 0
        )

        # ===== EAR 재보정 =====
        if state == "OPEN" and perclos < 0.2 and ear is not None:
            ear_history.append((now, ear))

        while ear_history and now - ear_history[0][0] > EAR_RECAL_WINDOW:
            ear_history.popleft()

        if len(ear_history) >= 30:
            avg_ear = sum(e for _, e in ear_history) / len(ear_history)
            set_ear_threshold(avg_ear * 0.7)

        # ===== Head pose =====
        head_pitch = None
        head_score = 0.0
        if landmarks:
            pose = estimate_head_pose(landmarks, frame.shape)
            if pose:
                pitch, _, _ = pose
                head_pitch = pitch
                if pitch < -10:
                    head_score = np.clip(abs(pitch) / 25, 0, 1)

        # ===== Score =====
        ear_score = 0.0
        if avg_ear and ear is not None:
            ear_score = np.clip((avg_ear - ear) / avg_ear, 0, 1)

        perclos_score = np.clip(perclos / 0.4, 0, 1)

        drowsy_level = (
            0.35 * ear_score +
            0.30 * perclos_score +
            0.20 * head_score +
            0.15 * blink_drop
        )

        # ===== State =====
        if drowsy_level < 0.4:
            drowsy_state = "NORMAL"
        elif drowsy_level < 0.7:
            drowsy_state = "WARNING"
        else:
            drowsy_state = "DROWSY"

        # ===== CSV =====
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                int(now),
                round(ear, 4) if ear else None,
                state,
                blink_count,
                round(blink_drop, 3),
                round(perclos, 3),
                round(head_pitch, 2) if head_pitch else None,
                round(drowsy_level, 3),
                drowsy_state
            ])

        # ===== Display =====
        cv2.putText(frame, f"STATE: {drowsy_state} ({drowsy_level:.2f})",
                    (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255) if drowsy_state == "DROWSY"
                    else (0, 255, 255) if drowsy_state == "WARNING"
                    else (0, 255, 0), 2)

        cv2.imshow("Drowsiness", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
