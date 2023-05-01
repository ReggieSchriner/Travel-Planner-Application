from json import dumps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.uix.screenmanager import ScreenManager, Screen

from rest import RESTConnection
from travel_planner_app import combined_installer
from travel_planner_app.database import DealsDatabase

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'
COUNT = 5


class TravelPlannerApp(App):
    def __init__(self, **kwargs):
        super(TravelPlannerApp, self).__init__(**kwargs)
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'package_deals', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        return kv

    def get_forecast_from_api(self, api_key):
        # url = f"http://api.openweathermap.org/data/2.5/forecast?port=443&lat=40.813618&lon=-96.702599&appid={api_key}&units=imperial"
        # response = requests.get(url)
        # if response.status_code != 200:
        #     print("error")
        print(api_key);
        self.records = []
        connection = RESTConnection('api.openweathermap.org', 443, '/data/2.5')
        connection.send_request(
            'forecast',
            {
                'appid': api_key,
                'lat': UNL_LATITUDE,
                'lon': UNL_LONGITUDE,
                'units': UNITS,
                'cnt': COUNT
            },
            None,
            self.on_records_loaded,
            self.on_records_not_loaded,
            self.on_records_not_loaded
        )

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        print('success')

    def on_records_not_loaded(self, _, error):
        self.records = ['[Failed to load records]']
        print(error)


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
