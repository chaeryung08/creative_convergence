from kivy.core.text import LabelBase

LabelBase.register(
    name="NanumGothic",
    fn_regular="C:/Windows/Fonts/NanumGothic.ttf",
    fn_bold="C:/Windows/Fonts/NanumGothicBold.ttf",
)

print("✅ 한글 폰트 등록 완료")


from kivy.app import App
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

class TestApp(App):
    def build(self):
        return SleepModeScreen()

if __name__ == "__main__":
    TestApp().run()
