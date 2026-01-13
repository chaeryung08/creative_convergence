import sys
from kivy.app import App
from kivy.core.text import LabelBase
import os

from App_sleep.screens.sleep_mode_screen import SleepModeScreen

# Windows 폰트 경로
font_path = 'C:/Windows/Fonts/malgun.ttf'

if os.path.exists(font_path):
    LabelBase.register(
        name='NanumGothic',
        fn_regular=font_path
    )
    print(f"✅ 폰트 로드 성공: {font_path}")
else:
    print(f"⚠️ 폰트 파일 없음: {font_path}")

class SleepMonitorApp(App):
    def build(self):
        if os.path.exists(font_path):
            from kivy.factory import Factory
            Factory.Label.font_name = 'NanumGothic'
            Factory.Button.font_name = 'NanumGothic'

        return SleepModeScreen()

if __name__ == '__main__':
    SleepMonitorApp().run()