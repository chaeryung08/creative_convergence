import numpy as np
import time
from collections import deque


class DrowsinessDetector:
    """
    EAR, PERCLOS, BLINK 감소, HEAD PITCH
    → 4요소를 모두 사용해 졸음 score 계산
    """

    def __init__(self):
        # 프레임 카운트
        self.total_frames = 0
        self.eye_closed_frames = 0

        # Blink 관련
        self.last_eye_state = "OPEN"
        self.blink_times = deque()
        self.BLINK_WINDOW = 60  # seconds

        # EAR 기준
        self.ear_history = deque()
        self.avg_ear = None
        self.EAR_BASELINE_WINDOW = 60  # seconds

        # Baseline blink
        self.baseline_blinks = []
        self.baseline_start = time.time()
        self.BASELINE_TIME = 60
        self.baseline_blink_rate = None

    def update(self, ear, eye_state, pitch, timestamp):
        self.total_frames += 1

        # ===== Eye closed =====
        if eye_state == "CLOSED":
            self.eye_closed_frames += 1
        else:
            if self.last_eye_state == "CLOSED":
                self.blink_times.append(timestamp)
                if self.baseline_blink_rate is None:
                    self.baseline_blinks.append(timestamp)

        self.last_eye_state = eye_state

        # ===== Blink window 유지 =====
        while self.blink_times and timestamp - self.blink_times[0] > self.BLINK_WINDOW:
            self.blink_times.popleft()

        blink_count = len(self.blink_times)

        # ===== Baseline blink =====
        if self.baseline_blink_rate is None:
            if timestamp - self.baseline_start >= self.BASELINE_TIME:
                self.baseline_blink_rate = max(1, len(self.baseline_blinks))

        # ===== Blink 감소율 =====
        blink_drop = 0.0
        if self.baseline_blink_rate:
            blink_drop = np.clip(
                (self.baseline_blink_rate - blink_count) / self.baseline_blink_rate,
                0, 1
            )

        # ===== PERCLOS =====
        perclos = self.eye_closed_frames / max(1, self.total_frames)
        perclos_score = np.clip(perclos / 0.4, 0, 1)

        # ===== EAR baseline =====
        if ear is not None:
            self.ear_history.append((timestamp, ear))

        while self.ear_history and timestamp - self.ear_history[0][0] > self.EAR_BASELINE_WINDOW:
            self.ear_history.popleft()

        if len(self.ear_history) >= 30:
            self.avg_ear = sum(e for _, e in self.ear_history) / len(self.ear_history)

        ear_score = 0.0
        if self.avg_ear and ear:
            ear_score = np.clip((self.avg_ear - ear) / self.avg_ear, 0, 1)

        # ===== Head pitch =====
        head_score = np.clip((abs(pitch) - 15.0) / 15.0, 0, 1)

        # ===== 최종 score (4요소 전부) =====
        score = (
            0.40 * ear_score +
            0.25 * perclos_score +
            0.15 * blink_drop +
            0.20 * head_score
        )

        # ===== 상태 =====
        if score < 0.4:
            state = "NORMAL"
        elif score < 0.7:
            state = "WARNING"
        else:
            state = "DROWSY"

        return {
            "state": state,
            "score": score,
            "ear": ear,
            "avg_ear": self.avg_ear,
            "perclos": perclos,
            "blink_count": blink_count,
            "blink_drop": blink_drop,
            "pitch": pitch,
            "ear_score": ear_score,
            "perclos_score": perclos_score,
            "blink_score": blink_drop,
            "head_score": head_score,
        }
