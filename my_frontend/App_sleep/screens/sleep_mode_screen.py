from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from my_frontend.App_sleep.components.nap_timer_button import NapTimerButton


class SleepModeScreen(BoxLayout):
    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = dp(24)
        self.spacing = dp(20)

        # 배경
        with self.canvas.before:
            Color(0.95, 0.97, 1, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # 제목
        title = Label(
            text='낮잠 모드',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=dp(48),
            font_name='NanumBarunPen'
        )

        subtitle = Label(
            text='하루 최대 30분',
            font_size='14sp',
            color=(0.45, 0.45, 0.45, 1),
            size_hint_y=None,
            height=dp(28),
            font_name='NanumBarunPen'
        )

        # 낮잠 타이머
        nap_timer = NapTimerButton(event_logger)

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(nap_timer)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
