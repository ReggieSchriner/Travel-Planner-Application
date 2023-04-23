from kivy.app import App
from kivy.modules import inspector  # For inspection
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


class TravelPlannerApp(App):
    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        return kv

class MainWindow(ScreenManager):
    pass

class CredentialsWindow(Screen):
    pass

class timer():
    def work1(self):
        self.work1(self).current = 'loading screen'

class LoadingScreen(Screen):
    def switchToNextScreen(self):
        Clock.schedule_once(timer.work1, 2)

class MainMenu(Screen):
    pass




if __name__ == '__main__':
    app = TravelPlannerApp()
    app.run()
