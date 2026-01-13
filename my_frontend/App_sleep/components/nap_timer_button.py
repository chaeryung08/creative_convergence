from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime

PRIMARY = (0.1, 0.4, 0.9, 1)
GRAY = (0.4, 0.4, 0.4, 1)
RED = (0.9, 0.2, 0.2, 1)

class NapTimerButton(BoxLayout):
    """하루 30분 제한 낮잠 타이머"""

    def __init__(self, event_logger=None, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(300)

        # 시간 관리
        self.selected_minutes = 10
        self.remaining_seconds = 0
        self.timer_active = False
        self.timer_event = None
        self.alert_event = None

        self.max_daily_seconds = 30 * 60
        self.used_today = 0
        self.today = datetime.now().date()

        # 배경
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[dp(16)], pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.remaining_label = Label(
            font_size="14sp",
            color=GRAY,
            size_hint_y=None,
            height=dp(24),
        )
        self.add_widget(self.remaining_label)

        self.time_label = Label(
            text="10:00",
            font_size="48sp",
            color=PRIMARY,
            size_hint_y=None,
            height=dp(80),
        )
        self.add_widget(self.time_label)

        self.status_label = Label(
            text="",
            font_size="14sp",
            color=RED,
            size_hint_y=None,
            height=dp(30),
        )
        self.add_widget(self.status_label)

        self.btn = Button(
            text="시작",
            size_hint_y=None,
            height=dp(50),
            background_color=PRIMARY,
        )
        self.btn.bind(on_press=self.toggle)
        self.add_widget(self.btn)

        self.update_remaining()

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_remaining(self):
        if datetime.now().date() != self.today:
            self.used_today = 0
            self.today = datetime.now().date()

        remain = max(0, self.max_daily_seconds - self.used_today)
        m, s = divmod(remain, 60)
        self.remaining_label.text = f"오늘 남은 시간: {m}분 {s:02d}초"

    def toggle(self, *args):
        if self.timer_active:
            self.stop()
        else:
            self.start()

    def start(self):
        remain = self.max_daily_seconds - self.used_today
        if remain <= 0:
            self.status_label.text = "오늘 낮잠 사용 시간 초과"
            return

        self.remaining_seconds = min(self.selected_minutes * 60, remain)
        self.timer_active = True
        self.btn.text = "정지"
        self.btn.background_color = RED
        self.status_label.text = ""

        self.timer_event = Clock.schedule_interval(self.tick, 1)

    def stop(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_active = False
        self.btn.text = "시작"
        self.btn.background_color = PRIMARY

    def tick(self, dt):
        self.remaining_seconds -= 1
        m, s = divmod(self.remaining_seconds, 60)
        self.time_label.text = f"{m:02d}:{s:02d}"

        if self.remaining_seconds <= 0:
            self.finish()

    def finish(self):
        if self.timer_event:
            self.timer_event.cancel()

        self.used_today += self.selected_minutes * 60
        self.timer_active = False
        self.btn.text = "시작"
        self.btn.background_color = PRIMARY
        self.time_label.text = "00:00"

        # 🔔 알림
        self.status_label.text = "일어날 시각입니다! 1분 내 반응 없으면 비수면 모드 전환"
        print("일어날 시각입니다!")

        # 1분 미응답 감지
        self.alert_event = Clock.schedule_once(self.force_wakeup, 60)
        self.update_remaining()

    def force_wakeup(self, dt):
        self.status_label.text = "비수면 모드로 전환됩니다."
        print("😴 반응 없음 → 비수면 모드 전환")
