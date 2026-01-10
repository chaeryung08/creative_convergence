from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime, timedelta
from kivy.clock import Clock

class NapTimerButton(BoxLayout):
    """낮잠 타이머 컴포넌트 (하루 최대 30분)"""
    
    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)
        self.event_logger = event_logger
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(300)
        
        # 낮잠 타이머 상태
        self.timer_active = False
        self.timer_end_time = None
        self.selected_minutes = 10
        self.remaining_seconds = 0
        
        # 하루 사용 시간 추적 (초 단위)
        self.today = datetime.now().date()
        self.total_used_today = 0  # 초 단위
        self.max_daily_seconds = 30 * 60  # 30분 = 1800초
        
        # 타이머 및 알림 체크
        self.timer_clock = None
        self.alarm_start_time = None
        self.alarm_check_clock = None
        
        # 배경
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # UI 요소들
        self.title_label = Label(
            text='쪽잠 타이머',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.emoji_label = Label(
            text='😴',
            font_size='48sp',
            size_hint_y=None,
            height=dp(60)
        )
        
        # 시간 선택 스피너
        self.time_spinner = Spinner(
            text='10분',
            values=('5분', '10분', '15분', '20분', '25분', '30분'),
            size_hint_y=None,
            height=dp(44),
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.time_spinner.bind(text=self.on_spinner_select)
        
        self.status_label = Label(
            text='타이머가 설정되지 않았습니다',
            font_size='16sp',
            color=(0.46, 0.46, 0.46, 1),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 남은 시간 표시 레이블
        self.usage_label = Label(
            text=f'오늘 사용 가능: 30분 00초',
            font_size='14sp',
            color=(0.13, 0.59, 0.95, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.action_button = Button(
            text='타이머 시작',
            background_color=(0.13, 0.59, 0.95, 1),
            size_hint_y=None,
            height=dp(50)
        )
        self.action_button.bind(on_press=self.toggle_timer)
        
        self.add_widget(self.title_label)
        self.add_widget(self.emoji_label)
        self.add_widget(self.time_spinner)
        self.add_widget(self.status_label)
        self.add_widget(self.usage_label)
        self.add_widget(self.action_button)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_spinner_select(self, spinner, text):
        """스피너에서 시간 선택"""
        self.selected_minutes = int(text.replace('분', ''))
        self.update_usage_label()
    
    def update_usage_label(self):
        """남은 사용 가능 시간 업데이트"""
        # 날짜가 바뀌면 초기화
        if datetime.now().date() != self.today:
            self.today = datetime.now().date()
            self.total_used_today = 0
        
        remaining = self.max_daily_seconds - self.total_used_today
        mins = remaining // 60
        secs = remaining % 60
        
        if remaining <= 0:
            self.usage_label.text = '오늘 사용 시간을 모두 소진했습니다'
            self.usage_label.color = (0.96, 0.26, 0.21, 1)
        else:
            self.usage_label.text = f'오늘 사용 가능: {mins}분 {secs:02d}초'
            self.usage_label.color = (0.13, 0.59, 0.95, 1)
    
    def toggle_timer(self, instance):
        """타이머 토글"""
        if not self.timer_active:
            self.start_timer()
        else:
            self.cancel_timer()
    
    def start_timer(self):
        """타이머 시작"""
        # 남은 시간 확인
        remaining = self.max_daily_seconds - self.total_used_today
        if remaining <= 0:
            self.status_label.text = '오늘 사용 시간을 초과했습니다'
            self.status_label.color = (0.96, 0.26, 0.21, 1)
            return
        
        # 선택한 시간이 남은 시간보다 크면 조정
        requested_seconds = self.selected_minutes * 60
        if requested_seconds > remaining:
            actual_seconds = remaining
            actual_minutes = actual_seconds // 60
            self.status_label.text = f'남은 시간({actual_minutes}분)만 사용합니다'
        else:
            actual_seconds = requested_seconds
        
        self.timer_active = True
        self.remaining_seconds = actual_seconds
        self.timer_end_time = datetime.now() + timedelta(seconds=actual_seconds)
        
        self.emoji_label.text = '💤'
        self.time_spinner.disabled = True
        self.action_button.text = '타이머 취소'
        self.action_button.background_color = (0.96, 0.26, 0.21, 1)
        
        # 타이머 시작
        self.timer_clock = Clock.schedule_interval(self.update_timer, 1)
        
        self.event_logger.log_nap_timer_start(actual_seconds)
    
    def update_timer(self, dt):
        """타이머 업데이트 (1초마다)"""
        self.remaining_seconds -= 1
        
        if self.remaining_seconds <= 0:
            self.timer_complete()
        else:
            mins = self.remaining_seconds // 60
            secs = self.remaining_seconds % 60
            self.status_label.text = f'남은 시간: {mins}분 {secs:02d}초'
            self.status_label.font_size = '24sp'
            self.status_label.color = (0.13, 0.59, 0.95, 1)
    
    def timer_complete(self):
        """타이머 완료 - 알람 울림"""
        if self.timer_clock:
            self.timer_clock.cancel()
        
        # 사용 시간 기록
        used_time = self.selected_minutes * 60
        self.total_used_today += used_time
        self.update_usage_label()
        
        # 알람 시작
        self.emoji_label.text = '🔔'
        self.status_label.text = '알람! 일어나세요!'
        self.status_label.color = (0.96, 0.26, 0.21, 1)
        self.action_button.text = '알람 끄기'
        self.action_button.background_color = (0.96, 0.26, 0.21, 1)
        
        self.alarm_start_time = datetime.now()
        self.alarm_check_clock = Clock.schedule_interval(self.check_alarm_recognition, 1)
        
        self.event_logger.log_nap_timer_complete()
    
    def check_alarm_recognition(self, dt):
        """알람 인식 확인 - 1분 이상 인식 못하면 비수면 모드 전환"""
        if self.alarm_start_time:
            elapsed = (datetime.now() - self.alarm_start_time).total_seconds()
            
            if elapsed >= 60:  # 1분 경과
                # 비수면 모드로 자동 전환
                if self.alarm_check_clock:
                    self.alarm_check_clock.cancel()
                
                self.event_logger.log_deep_sleep_detected()
                self.force_non_sleep_mode()
    
    def force_non_sleep_mode(self):
        """깊은 수면 감지 - 강제로 비수면 모드 전환"""
        self.timer_active = False
        self.alarm_start_time = None
        
        self.emoji_label.text = '😴'
        self.status_label.text = '깊은 수면 감지 - 비수면 모드로 전환됨'
        self.status_label.color = (0.96, 0.26, 0.21, 1)
        self.status_label.font_size = '16sp'
        self.time_spinner.disabled = False
        self.action_button.text = '타이머 시작'
        self.action_button.background_color = (0.13, 0.59, 0.95, 1)
        
        # 여기서 실제 앱의 수면 모드를 비활성화하는 로직 추가 필요
        print("⚠️ 깊은 수면 감지! 비수면 모드로 전환")
    
    def cancel_timer(self):
        """타이머 취소 또는 알람 끄기"""
        if self.timer_clock:
            self.timer_clock.cancel()
            # 사용한 시간만큼 기록
            if self.timer_end_time:
                elapsed_seconds = (self.timer_end_time - datetime.now()).total_seconds()
                used_time = (self.selected_minutes * 60) - max(0, int(elapsed_seconds))
                self.total_used_today += used_time
        
        if self.alarm_check_clock:
            self.alarm_check_clock.cancel()
        
        self.timer_active = False
        self.timer_end_time = None
        self.alarm_start_time = None
        self.remaining_seconds = 0
        
        self.emoji_label.text = '😴'
        self.status_label.text = '타이머가 설정되지 않았습니다'
        self.status_label.font_size = '16sp'
        self.status_label.color = (0.46, 0.46, 0.46, 1)
        self.time_spinner.disabled = False
        self.action_button.text = '타이머 시작'
        self.action_button.background_color = (0.13, 0.59, 0.95, 1)
        
        self.update_usage_label()
        self.event_logger.log_nap_timer_cancel()