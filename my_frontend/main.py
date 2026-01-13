from kivy.core.text import LabelBase
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LabelBase.register(
    name="NanumBarunPen",
    fn_regular=os.path.join(
        BASE_DIR,
        "App_sleep",
        "fonts",
        "NanumBarunpenR.ttf"
    ),
    fn_bold=os.path.join(
        BASE_DIR,
        "App_sleep",
        "fonts",
        "NanumBarunpenB.ttf"
    ) if os.path.exists(os.path.join(BASE_DIR, "App_sleep", "fonts", "NanumBarunpenB.ttf")) else None
)

print("✅ Nanum Barun Pen 폰트 로드 성공")

print("✅ 한글 폰트 등록 완료")


from kivy.app import App
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

class TestApp(App):
    def build(self):
        return SleepModeScreen()

if __name__ == "__main__":
    TestApp().run()
