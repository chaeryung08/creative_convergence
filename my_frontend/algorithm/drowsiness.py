import numpy as np
import time
from collections import deque


class DrowsinessDetector:
    def __init__(self):
        self.blink_times = deque()
        self.baseline_blinks = []
        self.baseline_start = time.time()
        self.baseline_rate = None

        self.BLINK_WINDOW = 60
        self.BASELINE_TIME = 60

    def update(self, ear, eye_state, pitch, yaw, timestamp):
        # ===== Blink =====
        if eye_state == "CLOSED":
            self.blink_times.append(timestamp)
            if self.baseline_rate is None:
                self.baseline_blinks.append(timestamp)

        while self.blink_times and timestamp - self.blink_times[0] > self.BLINK_WINDOW:
            self.blink_times.popleft()

        blink_count = len(self.blink_times)

        if self.baseline_rate is None and timestamp - self.baseline_start >= self.BASELINE_TIME:
            self.baseline_rate = len(self.baseline_blinks)

        blink_drop = 0.0
        if self.baseline_rate and self.baseline_rate > 0:
            blink_drop = np.clip(
                (self.baseline_rate - blink_count) / self.baseline_rate, 0, 1
            )

        # ===== EAR score (순간 눈 감김 정도) =====
        ear_score = np.clip((0.25 - ear) / 0.25, 0, 1) if ear else 0

        # ===== Head score (아래 숙이면 증가) =====
        head_score = np.clip((pitch - 10) / 20, 0, 1)

        # ===== 가중치 =====
        drowsy_level = (
            0.35 * ear_score +
            0.40 * blink_drop +
            0.25 * head_score
        )

        if drowsy_level < 0.4:
            state = "NORMAL"
        elif drowsy_level < 0.7:
            state = "WARNING"
        else:
            state = "DROWSY"

        return {
            "drowsy_level": drowsy_level,
            "state": state,
            "ear_score": ear_score,
            "blink_drop": blink_drop,
            "head_score": head_score
        }
