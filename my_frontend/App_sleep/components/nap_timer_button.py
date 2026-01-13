from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.metrics import dp
from datetime import datetime, timedelta
from kivy.clock import Clock
import math

class CircularProgress(Widget):
    """원형 프로그레스 바 (시계 애니메이션)"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = 0  # 0~1
        self.size_hint = (None, None)
        self.size = (dp(200), dp(200))
        
        with self.canvas:
            # 배경 원 (회색)
            Color(1, 1, 1, 0.3)
            self.bg_circle = Line(
                circle=(self.center_x, self.center_y, dp(90)),
                width=dp(12)
            )
            
            # 진행률 원 (흰색)
            Color(1, 1, 1, 1)
            self.progress_circle = Line(
                circle=(self.center_x, self.center_y, dp(90), 0, 0),
                width=dp(12)
            )
        
        self.bind(pos=self.update_circle, size=self.update_circle)
    
    def update_circle(self, *args):
        """원 위치 업데이트"""
        self.bg_circle.circle = (self.center_x, self.center_y, dp(90))
        angle = 360 * self.progress
        self.progress_circle.circle = (self.center_x, self.center_y, dp(90), 0, angle)
    
    def set_progress(self, value):
        """진행률 설정 (0~1)"""
        self.progress = max(0, min(1, value))
        self.update_circle()


class NapTimerButton(BoxLayout):
    """낮잠 타이머 컴포넌트 - 완전 개선된 UI"""
    
    def __init__(self, event_logger, **kwargs):
        super().__init__(**kwargs)
        self.event_logger = event_logger
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(16)
        self.size_hint_y = None
        self.height = dp(520)
        
        # 타이머 상태
        self.timer_active = False
        self.selected_minutes = 10
        self.remaining_seconds = 0
        self.total_seconds = 0
        
        # 하루 사용 시간 추적
        self.today = datetime.now().date()
        self.total_used_today = 0
        self.max_daily_seconds = 30 * 60
        
        # 타이머 및 알림
        self.timer_clock = None
        self.alarm_start_time = None
        self.alarm_check_clock = None
        
        # 배경 (파란색 그라데이션)
        with self.canvas.before:
            Color(0.2, 0.6, 0.86, 1)  # 밝은 파란색
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # === 오늘 남은 시간 표시 ===
        self.usage_label = Label(
            text='',
            font_size='16sp',
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(30),
            bold=True
        )
        self.update_usage_label()
        
        # === 원형 프로그레스 + 타이머 디스플레이 ===
        timer_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220)
        )
        
        # 원형 프로그레스 (시계)
        self.circular_progress = CircularProgress()
        
        # 타이머 숫자 (원 중앙에 배치)
        self.timer_display = Label(
            text='10:00',
            font_size='48sp',
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        timer_container.add_widget(self.circular_progress)
        timer_container.add_widget(self.timer_display)
        
        # === 프리셋 버튼들 (5분, 10분, 15분, 20분, 30분) ===
        preset_label = Label(
            text='빠른 설정',
            font_size='14sp',
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(25)
        )
        
        preset_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(45)
        )
        
        presets = [5, 10, 15, 20, 30]
        for minutes in presets:
            btn = Button(
                text=f'{minutes}분',
                background_normal='',
                background_color=(1, 1, 1, 0.25),
                color=(1, 1, 1, 1),
                font_size='14sp',
                bold=True
            )
            btn.bind(on_press=lambda x, m=minutes: self.set_preset(m))
            preset_layout.add_widget(btn)
        
        # === 시간 미세 조정 버튼 (+1, +5, -1, -5) ===
        adjust_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(45)
        )
        
        adjustments = [
            (-5, '-5분'),
            (-1, '-1분'),
            (1, '+1분'),
            (5, '+5분')
        ]
        
        for minutes, text in adjustments:
            btn = Button(
                text=text,
                background_normal='',
                background_color=(1, 1, 1, 0.2),
                color=(1, 1, 1, 1),
                font_size='13sp',
                bold=True
            )
            btn.bind(on_press=lambda x, m=minutes: self.adjust_time(m))
            adjust_layout.add_widget(btn)
        
        # === 진행률 바 ===
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(8)
        )
        
        # === 시작/정지 버튼 ===
        self.control_button = Button(
            text='시작',
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.6, 0.86, 1),
            size_hint_y=None,
            height=dp(60),
            font_size='20sp',
            bold=True
        )
        self.control_button.bind(on_press=self.toggle_timer)
        
        # === 상태 메시지 ===
        self.status_label = Label(
            text='쪽잠으로 학습 효율을 높이세요 ☕',
            font_size='14sp',
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 위젯 추가
        self.add_widget(self.usage_label)
        self.add_widget(timer_container)
        self.add_widget(preset_label)
        self.add_widget(preset_layout)
        self.add_widget(adjust_layout)
        self.add_widget(self.progress_bar)
        self.add_widget(self.control_button)
        self.add_widget(self.status_label)
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def set_preset(self, minutes):
        """프리셋 버튼 클릭"""
        if self.timer_active:
            return
        
        # 남은 시간 확인
        remaining_daily = (self.max_daily_seconds - self.total_used_today) // 60
        if minutes > remaining_daily:
            self.status_label.text = f'⚠️ 오늘은 {remaining_daily}분만 사용 가능합니다'
            return
        
        self.selected_minutes = minutes
        self.timer_display.text = f'{self.selected_minutes:02d}:00'
        self.status_label.text = f'{minutes}분 타이머 설정 완료 ✓'
    
    def adjust_time(self, minutes):
        """시간 미세 조정"""
        if self.timer_active:
            return
        
        new_minutes = max(1, min(30, self.selected_minutes + minutes))
        
        # 남은 시간 확인
        remaining_daily = (self.max_daily_seconds - self.total_used_today) // 60
        if new_minutes > remaining_daily:
            self.status_label.text = f'⚠️ 오늘은 {remaining_daily}분만 사용 가능합니다'
            return
        
        self.selected_minutes = new_minutes
        self.timer_display.text = f'{self.selected_minutes:02d}:00'
    
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
            self.usage_label.text = '⏰ 오늘 사용 시간 소진'
        else:
            self.usage_label.text = f'오늘 남은 시간: {mins}분 {secs:02d}초'
    
    def toggle_timer(self, instance):
        """타이머 토글"""
        if not self.timer_active:
            self.start_timer()
        else:
            self.cancel_timer()
    
    def start_timer(self):
        """타이머 시작"""
        remaining = self.max_daily_seconds - self.total_used_today
        if remaining <= 0:
            self.status_label.text = '⚠️ 오늘 사용 시간을 초과했습니다'
            return
        
        requested_seconds = self.selected_minutes * 60
        if requested_seconds > remaining:
            actual_seconds = remaining
        else:
            actual_seconds = requested_seconds
        
        self.timer_active = True
        self.remaining_seconds = actual_seconds
        self.total_seconds = actual_seconds
        
        # UI 변경
        self.control_button.text = '정지'
        self.control_button.background_color = (0.96, 0.26, 0.21, 1)
        self.control_button.color = (1, 1, 1, 1)
        self.status_label.text = '⏱️ 타이머 실행 중...'
        
        # 타이머 시작
        self.timer_clock = Clock.schedule_interval(self.update_timer, 1)
        
        self.event_logger.log_nap_timer_start(actual_seconds)
    
    def update_timer(self, dt):
        """타이머 업데이트 (원형 애니메이션 포함)"""
        self.remaining_seconds -= 1
        
        if self.remaining_seconds <= 0:
            self.timer_complete()
        else:
            # 시간 표시
            mins = self.remaining_seconds // 60
            secs = self.remaining_seconds % 60
            self.timer_display.text = f'{mins:02d}:{secs:02d}'
            
            # 진행률 업데이트
            progress = 1 - (self.remaining_seconds / self.total_seconds)
            self.progress_bar.value = progress * 100
            self.circular_progress.set_progress(progress)
            
            self.update_usage_label()
    
    def timer_complete(self):
        """타이머 완료 - 알람"""
        if self.timer_clock:
            self.timer_clock.cancel()
        
        # 사용 시간 기록
        used_time = self.selected_minutes * 60
        self.total_used_today += used_time
        self.update_usage_label()
        
        # 알람 시작
        self.timer_display.text = '00:00'
        self.status_label.text = '🔔 알람! 일어나세요!'
        self.control_button.text = '알람 끄기'
        self.control_button.background_color = (1, 0.6, 0, 1)
        self.progress_bar.value = 100
        self.circular_progress.set_progress(1)
        
        self.alarm_start_time = datetime.now()
        self.alarm_check_clock = Clock.schedule_interval(self.check_alarm_recognition, 1)
        
        self.event_logger.log_nap_timer_complete()
    
    def check_alarm_recognition(self, dt):
        """1분 이상 인식 못하면 깊은 수면으로 판단"""
        if self.alarm_start_time:
            elapsed = (datetime.now() - self.alarm_start_time).total_seconds()
            
            if elapsed >= 60:
                if self.alarm_check_clock:
                    self.alarm_check_clock.cancel()
                
                self.event_logger.log_deep_sleep_detected()
                self.force_non_sleep_mode()
    
    def force_non_sleep_mode(self):
        """깊은 수면 감지 - 비수면 모드 전환"""
        self.timer_active = False
        self.alarm_start_time = None
        
        self.status_label.text = '😴 깊은 수면 감지 - 비수면 모드로 전환'
        self.control_button.text = '시작'
        self.control_button.background_color = (1, 1, 1, 1)
        self.control_button.color = (0.2, 0.6, 0.86, 1)
        self.timer_display.text = f'{self.selected_minutes:02d}:00'
        self.progress_bar.value = 0
        self.circular_progress.set_progress(0)
        
        print("⚠️ 깊은 수면 감지! 비수면 모드로 전환")
    
    def cancel_timer(self):
        """타이머 취소"""
        if self.timer_clock:
            self.timer_clock.cancel()
            # 사용한 시간 기록
            elapsed = self.total_seconds - self.remaining_seconds
            self.total_used_today += elapsed
        
        if self.alarm_check_clock:
            self.alarm_check_clock.cancel()
        
        self.timer_active = False
        self.alarm_start_time = None
        
        self.timer_display.text = f'{self.selected_minutes:02d}:00'
        self.control_button.text = '시작'
        self.control_button.background_color = (1, 1, 1, 1)
        self.control_button.color = (0.2, 0.6, 0.86, 1)
        self.status_label.text = '쪽잠으로 학습 효율을 높이세요 ☕'
        self.progress_bar.value = 0
        self.circular_progress.set_progress(0)
        
        self.update_usage_label()
        self.event_logger.log_nap_timer_cancel()