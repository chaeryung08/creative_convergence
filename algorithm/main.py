import cv2
import time
import csv
from collections import deque
from algorithm.eye_detect import detect_eye_state, set_ear_threshold

LOG_FILE = "drowsiness_log.csv"

def main():
    cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30

    CLOSED_THRESHOLD = int(fps * 3.0)     # 3초
    BLINK_WINDOW_SEC = 60
    PERCLOS_WINDOW_SEC = 60

    closed_frames = 0
    prev_state = "OPEN"

    blink_times = deque()
    frame_states = deque()

    # Calibration
    CALIBRATION_TIME = 5
    ear_samples = []
    calibrated = False
    calibration_start = time.time()

    # CSV 초기화
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "EAR",
            "eye_state",
            "blink_count_1min",
            "perclos",
            "drowsy_state"
        ])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        state, ear = detect_eye_state(frame)
        now = time.time()

        # Calibration 단계
        if not calibrated:
            cv2.putText(frame, "Calibration: Keep eyes open",
                        (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

            if ear is not None:
                ear_samples.append(ear)

            if now - calibration_start >= CALIBRATION_TIME:
                avg_ear = sum(ear_samples) / len(ear_samples)
                set_ear_threshold(avg_ear * 0.75)
                calibrated = True

            cv2.imshow("Drowsiness Detection", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # Blink 감지 (CLOSED → OPEN)
        if prev_state == "CLOSED" and state == "OPEN":
            blink_times.append(now)

        prev_state = state

        # 1분 초과 blink 제거
        while blink_times and now - blink_times[0] > BLINK_WINDOW_SEC:
            blink_times.popleft()

        blink_count = len(blink_times)

        # 장시간 눈 감김
        if state == "CLOSED":
            closed_frames += 1
        else:
            closed_frames = 0

        long_close_drowsy = closed_frames >= CLOSED_THRESHOLD

        # PERCLOS 계산
        frame_states.append((now, state))
        while frame_states and now - frame_states[0][0] > PERCLOS_WINDOW_SEC:
            frame_states.popleft()

        closed_count = sum(1 for _, s in frame_states if s == "CLOSED")
        perclos = closed_count / len(frame_states) if frame_states else 0

        perclos_drowsy = perclos >= 0.4
        blink_drowsy = blink_count <= 10

        drowsy_state = "DROWSY" if (long_close_drowsy or perclos_drowsy or blink_drowsy) else "AWAKE"

        # CSV 저장
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                int(now),
                round(ear, 4) if ear else None,
                state,
                blink_count,
                round(perclos, 3),
                drowsy_state
            ])

        print(f"EAR={ear:.3f} | blink={blink_count} | perclos={perclos:.2f} | {drowsy_state}")

        cv2.imshow("Drowsiness Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()