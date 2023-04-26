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


class LoadingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_next_screen, 2)
    def switch_to_next_screen(self, *args):
        self.manager.current = 'main_menu'

class MainMenu(Screen):
    pass

class ValidateLocationsPage(Screen):
    pass

class UpdateRatingsPage(Screen):
    pass

class  ItineraryPage(Screen):
    pass

if __name__ == '__main__':
    app = TravelPlannerApp()
    app.run()
