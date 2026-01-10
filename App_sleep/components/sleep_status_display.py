from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime

class SleepStatusDisplay(BoxLayout):
    """졸음 상태 표시 컴포넌트"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(300)
        
        # 배경 설정
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # UI 요소들
        self.emoji_label = Label(
            text='😊',
            font_size='64sp',
            size_hint_y=None,
            height=dp(80)
        )
        
        self.title_label = Label(
            text='현재 상태',
            font_size='16sp',
            color=(0.46, 0.46, 0.46, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.status_label = Label(
            text='정상',
            font_size='32sp',
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=dp(12)
        )
        
        self.score_label = Label(
            text='0%',
            font_size='20sp',
            size_hint_y=None,
            height=dp(40)
        )
        
        self.add_widget(self.emoji_label)
        self.add_widget(self.title_label)
        self.add_widget(self.status_label)
        self.add_widget(self.progress_bar)
        self.add_widget(self.score_label)
    
    def update_bg(self, *args):
        """배경 업데이트"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def update_status(self, drowsiness_score: int, status_info: dict):
        """졸음 상태 업데이트"""
        self.emoji_label.text = status_info['emoji']
        self.status_label.text = status_info['label']
        self.progress_bar.value = drowsiness_score
        self.score_label.text = f"{drowsiness_score}%"
        
        # 색상 업데이트
        color = status_info['color']
        rgb = self.hex_to_rgb(color)
        self.status_label.color = rgb + (1,)
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """헥스 색상을 RGB로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))