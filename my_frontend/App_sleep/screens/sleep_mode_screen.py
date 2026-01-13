from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp
from datetime import datetime
import random

from App_sleep.components.sleep_status_display import SleepStatusDisplay
from App_sleep.components.timer_button import TimerButton
from App_sleep.components.nap_timer_button import NapTimerButton
from App_sleep.data.mock_data import (
    get_drowsiness_level,
    fetch_drowsiness_status,
    USE_MOCK_DATA
)
from App_sleep.utils.event_logger import event_logger


class SleepModeScreen(BoxLayout):
    """수면 모니터링 메인 화면"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # 데이터
        self.sleep_data = fetch_drowsiness_status()

        # ================= 헤더 =================
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(70),
            padding=dp(16),
            spacing=dp(16)
        )

        title_box = BoxLayout(orientation='vertical', size_hint_x=0.7)

        header_title = Label(
            text='수면 모니터링',
            font_size='24sp',
            bold=True,
            color=(0, 0, 0, 1),
            font_name='NanumGothic'
        )

        mode_label = Label(
            text='🔵 Mock 데이터 모드' if USE_MOCK_DATA else '🟢 실시간 연동 모드',
            font_size='12sp',
            color=(0.46, 0.46, 0.46, 1),
            font_name='NanumGothic'
        )

        title_box.add_widget(header_title)
        title_box.add_widget(mode_label)

        self.log_button = Button(
            text='로그 보기',
            size_hint_x=0.3,
            background_color=(0.13, 0.59, 0.95, 1),
            font_name='NanumGothic'
        )
        self.log_button.bind(on_press=self.toggle_logs)

        header.add_widget(title_box)
        header.add_widget(self.log_button)

        # ================= 스크롤 영역 =================
        scroll_view = ScrollView()

        self.content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None
        )
        self.content_layout.bind(
            minimum_height=self.content_layout.setter('height')
        )

        # ================= 컴포넌트 =================
        self.status_display = SleepStatusDisplay()
        self.timer_button = TimerButton(event_logger)
        self.nap_timer_button = NapTimerButton(event_logger)

        self.content_layout.add_widget(self.status_display)
        self.content_layout.add_widget(self.timer_button)
        self.content_layout.add_widget(self.nap_timer_button)  # 🔥 이게 핵심

        scroll_view.add_widget(self.content_layout)

        self.add_widget(header)
        self.add_widget(scroll_view)

        # 로그
        event_logger.log_screen_enter('SleepModeScreen')

        Clock.schedule_interval(self.update_data, 3.0)
        self.update_status()

    def update_data(self, dt):
        old_level = get_drowsiness_level(
            self.sleep_data['drowsiness_level']
        )['level']

        if USE_MOCK_DATA:
            self.sleep_data['drowsiness_level'] = random.randint(0, 100)
            self.sleep_data['last_update'] = datetime.now().isoformat()
        else:
            self.sleep_data = fetch_drowsiness_status()

        new_level = get_drowsiness_level(
            self.sleep_data['drowsiness_level']
        )['level']

        if old_level != new_level:
            event_logger.log_drowsiness_change(
                old_level,
                new_level,
                self.sleep_data['drowsiness_level']
            )

        self.update_status()

    def update_status(self):
        score = self.sleep_data['drowsiness_level']
        status_info = get_drowsiness_level(score)
        self.status_display.update_status(score, status_info)

    def toggle_logs(self, instance):
        print("\n최근 이벤트 로그")
        for log in event_logger.get_all_logs()[:10]:
            print(log)
