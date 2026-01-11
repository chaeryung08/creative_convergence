from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

class TimerButton(BoxLayout):
    """타이머 버튼 컴포넌트"""
    
    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)
        self.event_logger = event_logger
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(250)
        
        # 타이머 상태
        self.is_running = False
        self.time_left = 20 * 60  # 20분 (초 단위)
        self.timer_event = None
        
        # 배경
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # UI 요소들
        self.title_label = Label(
            text='휴식 타이머',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            font_name='NanumGothic'
        )
        
        self.timer_display = Label(
            text=self.format_time(self.time_left),
            font_size='56sp',
            bold=True,
            size_hint_y=None,
            height=dp(80),
            font_name='NanumGothic'
        )
        
        # 버튼 레이아웃
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.start_button = Button(
            text='시작',
            background_color=(0.3, 0.69, 0.31, 1),
            size_hint_x=0.5,
            font_name='NanumGothic'
        )
        self.start_button.bind(on_press=self.on_start)
        
        self.reset_button = Button(
            text='리셋',
            background_color=(0.46, 0.46, 0.46, 1),
            size_hint_x=0.5,
            font_name='NanumGothic'
        )
        self.reset_button.bind(on_press=self.on_reset)
        
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.reset_button)
        
        self.subtitle_label = Label(
            text='20분 휴식 권장',
            font_size='14sp',
            color=(0.46, 0.46, 0.46, 1),
            size_hint_y=None,
            height=dp(30),
            font_name='NanumGothic'
        )
        
        self.add_widget(self.title_label)
        self.add_widget(self.timer_display)
        self.add_widget(button_layout)
        self.add_widget(self.subtitle_label)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def format_time(self, seconds: int) -> str:
        """시간 포맷팅"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def on_start(self, instance):
        """시작/정지 버튼"""
        if not self.is_running:
            self.is_running = True
            self.start_button.text = '정지'
            self.start_button.background_color = (0.96, 0.26, 0.21, 1)
            self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)
            self.event_logger.log_timer_start(self.time_left)
            self.subtitle_label.text = '타이머 실행 중...'
        else:
            self.is_running = False
            self.start_button.text = '시작'
            self.start_button.background_color = (0.3, 0.69, 0.31, 1)
            if self.timer_event:
                self.timer_event.cancel()
            self.event_logger.log_timer_stop(self.time_left)
            self.subtitle_label.text = '20분 휴식 권장'
    
    def on_reset(self, instance):
        """리셋 버튼"""
        self.is_running = False
        self.time_left = 20 * 60
        self.timer_display.text = self.format_time(self.time_left)
        self.start_button.text = '시작'
        self.start_button.background_color = (0.3, 0.69, 0.31, 1)
        if self.timer_event:
            self.timer_event.cancel()
        self.event_logger.log('TIMER_RESET', {})
        self.subtitle_label.text = '20분 휴식 권장'
    
    def update_timer(self, dt):
        """타이머 업데이트"""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_display.text = self.format_time(self.time_left)
        else:
            self.on_timer_complete()
    
    def on_timer_complete(self):
        """타이머 완료"""
        self.is_running = False
        self.start_button.text = '시작'
        self.start_button.background_color = (0.3, 0.69, 0.31, 1)
        if self.timer_event:
            self.timer_event.cancel()
        self.event_logger.log('TIMER_COMPLETE', {'duration': 20 * 60})
        print("타이머가 종료되었습니다!")
        self.subtitle_label.text = '타이머 종료!'