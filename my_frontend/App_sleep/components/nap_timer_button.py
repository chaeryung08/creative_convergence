from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime

PRIMARY = (0.1, 0.4, 0.9, 1)
LIGHT_BLUE = (0.9, 0.95, 1, 1)
GRAY = (0.4, 0.4, 0.4, 1)

class TimerButton(BoxLayout):
    """30분 제한 낮잠 타이머 (Nap Timer)"""

    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)
        self.event_logger = event_logger

        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(16)
        self.size_hint_y = None
        self.height = dp(340)

        # 상태
        self.selected_minutes = 10
        self.remaining_seconds = 0
        self.timer_active = False
        self.timer_event = None

        self.max_daily_seconds = 30 * 60
        self.used_today = 0
        self.today = datetime.now().date()

        # 배경 카드
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[dp(16)], pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # 오늘 남은 시간
        self.remaining_label = Label(
            font_size='14sp',
            color=GRAY,
            size_hint_y=None,
            height=dp(24),
            font_name='NanumGothic'
        )
        self.add_widget(self.remaining_label)
        self.update_remaining()

        # 중앙 타이머
        self.time_label = Label(
            text='10:00',
            font_size='56sp',
            bold=True,
            color=PRIMARY,
            size_hint_y=None,
            height=dp(120),
            font_name='NanumGothic'
        )
        self.add_widget(self.time_label)

        # 시간 버튼
        btn_row = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(48))
        for m in (1, 5, 10):
            b = Button(
                text=f'+{m}분',
                background_normal='',
                background_color=LIGHT_BLUE,
                color=PRIMARY,
                font_name='NanumGothic'
            )
            b.bind(on_press=lambda x, mm=m: self.add_time(mm))
            btn_row.add_widget(b)
        self.add_widget(btn_row)

        # 시작 버튼
        self.start_btn = Button(
            text='시작',
            background_normal='',
            background_color=PRIMARY,
            color=(1,1,1,1),
            font_size='18sp',
            size_hint_y=None,
            height=dp(56),
            font_name='NanumGothic'
        )
        self.start_btn.bind(on_press=self.toggle)
        self.add_widget(self.start_btn)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_remaining(self):
        if datetime.now().date() != self.today:
            self.used_today = 0
            self.today = datetime.now().date()

        remain = max(0, self.max_daily_seconds - self.used_today)
        m, s = divmod(remain, 60)
        self.remaining_label.text = f'오늘 남은 시간: {m}분 {s:02d}초'

    def add_time(self, minutes):
        if self.timer_active:
            return
        self.selected_minutes = min(30, self.selected_minutes + minutes)
        self.time_label.text = f'{self.selected_minutes:02d}:00'

    def toggle(self, instance):
        if self.timer_active:
            self.stop()
        else:
            self.start()

    def start(self):
        remain = self.max_daily_seconds - self.used_today
        if remain <= 0:
            self.remaining_label.text = '오늘 사용 시간 초과'
            return

        self.remaining_seconds = min(self.selected_minutes * 60, remain)
        self.timer_active = True
        self.start_btn.text = '정지'
        self.start_btn.background_color = (0.9, 0.2, 0.2, 1)

        self.timer_event = Clock.schedule_interval(self.tick, 1)
        self.event_logger.log_nap_timer_start(self.remaining_seconds)

    def tick(self, dt):
        self.remaining_seconds -= 1
        if self.remaining_seconds <= 0:
            self.finish()
            return

        m, s = divmod(self.remaining_seconds, 60)
        self.time_label.text = f'{m:02d}:{s:02d}'

    def finish(self):
        if self.timer_event:
            self.timer_event.cancel()

        self.used_today += self.selected_minutes * 60
        self.timer_active = False
        self.start_btn.text = '시작'
        self.start_btn.background_color = PRIMARY
        self.time_label.text = '00:00'
        self.update_remaining()
        self.event_logger.log_nap_timer_complete()

    def stop(self):
        if self.timer_event:
            self.timer_event.cancel()

        self.timer_active = False
        self.start_btn.text = '시작'
        self.start_btn.background_color = PRIMARY
        self.time_label.text = f'{self.selected_minutes:02d}:00'
