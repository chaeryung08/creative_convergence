from kivy.app import App
from kivy.core.text import LabelBase    
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

class SleepMonitorApp(App):
    def build(self):
        return SleepModeScreen()

if __name__ == '__main__':
    SleepMonitorApp().run()
    from kivy.app import App
from kivy.core.text import LabelBase
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

# 🔥 한글 폰트 등록
LabelBase.register(
    name='NanumGothic',
    fn_regular='C:/Windows/Fonts/malgun.ttf', # 맑은 고딕
    fn_bold='C:/Windows/Fonts/malgunbd.ttf'  # 맑은 고딕 볼드
)

class SleepMonitorApp(App):
    def build(self):
        return SleepModeScreen()
        Factory.Label.font_name = 'NanumGothic'
        Factory.Button.font_name = 'NanumGothic'
        return SleepModeScreen()
if __name__ == '__main__':
    SleepMonitorApp().run()