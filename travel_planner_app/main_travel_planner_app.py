from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.uix.screenmanager import ScreenManager, Screen

from travel_planner_app import combined_installer


class TravelPlannerApp(App):
    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        return kv


class MainWindow(ScreenManager):
    pass


class CredentialsWindow(Screen):
    def add_credentials(self):
        attributes = [self.ids.authority.text, self.ids.port.text, self.ids.database.text,
                      self.ids.username.text, self.ids.password.text,
                      self.ids.weatherauthority.text, self.ids.weatherport.text,
                      self.ids.apikey.text]
        if any(attribute.isspace() or attribute == '' for attribute in attributes):
            self.ids.message.text = 'Fill in all text boxes'
            self.ids.authority.text, self.ids.port.text, self.ids.database.text, \
                self.ids.username.text, self.ids.password.text, \
                self.ids.weatherauthority.text, self.ids.weatherport.text, \
                self.ids.apikey.text = '', '', '', '', '', '', '', ''
        else:
            self.ids.message.text = 'Success!'
            addition = combined_installer.Credentials(authority=attributes[0], port=attributes[1],
                                                      database=attributes[2],
                                                      username=attributes[3], password=attributes[4],
                                                      weatherauthority=attributes[5], weatherport=attributes[6],
                                                      apikey=attributes[7])
            app = App.get_running_app()
            app.commit(addition)
        self.ids.authority.text, self.ids.port.text, self.ids.database.text, \
            self.ids.username.text, self.ids.password.text, \
            self.ids.weatherauthority.text, self.ids.weatherport.text, \
            self.ids.apikey.text = '', '', '', '', '', '', '', ''


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


class ItineraryPage(Screen):
    pass


if __name__ == '__main__':
    app = TravelPlannerApp()
    app.run()
