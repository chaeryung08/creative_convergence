from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime, timedelta

class AlarmButton(BoxLayout):
    """알람 버튼 컴포넌트"""
    
    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)
        self.event_logger = event_logger
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(250)
        
        # 알람 상태
        self.alarm_set = False
        self.alarm_time = None
        
        # 배경
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # UI 요소들
        self.title_label = Label(
            text='알람 설정',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.emoji_label = Label(
            text='🔕',
            font_size='48sp',
            size_hint_y=None,
            height=dp(60)
        )
        
        self.time_label = Label(
            text='알람이 설정되지 않았습니다',
            font_size='16sp',
            color=(0.46, 0.46, 0.46, 1),
            size_hint_y=None,
            height=dp(40)
        )
        
        self.action_button = Button(
            text='1시간 후 알람 설정',
            background_color=(0.13, 0.59, 0.95, 1),
            size_hint_y=None,
            height=dp(50)
        )
        self.action_button.bind(on_press=self.toggle_alarm)
        
        self.info_label = Label(
            text='💡 졸음이 감지되면 자동으로 알람이 울립니다',
            font_size='12sp',
            color=(0.46, 0.46, 0.46, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.add_widget(self.title_label)
        self.add_widget(self.emoji_label)
        self.add_widget(self.time_label)
        self.add_widget(self.action_button)
        self.add_widget(self.info_label)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def toggle_alarm(self, instance):
        """알람 토글"""
        if not self.alarm_set:
            self.set_alarm()
        else:
            self.cancel_alarm()
    
    def set_alarm(self):
        """알람 설정"""
        self.alarm_time = datetime.now() + timedelta(hours=1)
        self.alarm_set = True
        
        self.emoji_label.text = '⏰'
        self.time_label.text = self.alarm_time.strftime('%H:%M')
        self.time_label.font_size = '32sp'
        self.time_label.color = (0.13, 0.59, 0.95, 1)
        self.action_button.text = '알람 취소'
        self.action_button.background_color = (0.96, 0.26, 0.21, 1)
        
        self.event_logger.log_alarm_set(self.alarm_time.isoformat())
    
    def cancel_alarm(self):
        """알람 취소"""
        self.alarm_time = None
        self.alarm_set = False
        
        self.emoji_label.text = '🔕'
        self.time_label.text = '알람이 설정되지 않았습니다'
        self.time_label.font_size = '16sp'
        self.time_label.color = (0.46, 0.46, 0.46, 1)
        self.action_button.text = '1시간 후 알람 설정'
        self.action_button.background_color = (0.13, 0.59, 0.95, 1)
        
        self.event_logger.log_alarm_cancel()