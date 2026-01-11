from kivy.app import App
from App_sleep.screens.sleep_mode_screen import SleepModeScreen

class SleepMonitorApp(App):
    def build(self):
        return SleepModeScreen()

if __name__ == '__main__':
    SleepMonitorApp().run()