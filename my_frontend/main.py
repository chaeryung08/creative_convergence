from kivy.core.text import LabelBase

# 🔥 폰트 등록 (무조건 제일 위)
LabelBase.register(
    name='NanumGothic',
    fn_regular='C:/Windows/Fonts/malgun.ttf',
    fn_bold='C:/Windows/Fonts/malgunbd.ttf'
)

from kivy.app import App
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

class SleepMonitorApp(App):
    def build(self):
        return SleepModeScreen()

if __name__ == '__main__':
    SleepMonitorApp().run()
