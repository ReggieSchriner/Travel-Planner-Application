import json
from json import dumps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from lazr.restfulclient.errors import HTTPError
from mysql.connector import OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError

import rest
from travel_planner_app import combined_installer

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'
COUNT = 5


class CredentialsWindow(Screen):

    def __init__(self, **kwargs):
        super(CredentialsWindow, self).__init__(**kwargs)
        self.popup_text = Label(text='', color='black')
        self.popup = Popup(content=self.popup_text, size=(400, 400), background='white', size_hint=(None, None))
        self.forecast_rest_connection = None
        self.geocoding_rest_connection = None

    def add_credentials(self):
        try:
            f = open('credentials.json')
            data = json.load(f)
            attributes = []
            for element in data.values():
                attributes.append(element)
            authority = attributes[0]
            port = attributes[1]
            database = attributes[2]
            username = attributes[3]
            password = attributes[4]
            weatherauthority = attributes[5]
            weatherport = attributes[6]
            apikey = attributes[7]
            self.ids.authority.text = authority
            print(self.ids.authority.text)
            self.ids.port.text = port
            self.ids.database.text = database
            self.ids.username.text = username
            self.ids.password.text = ''
            self.ids.weatherauthority.text = weatherauthority
            self.ids.weatherport.text = weatherport
            self.ids.apikey.text = ''
        except FileNotFoundError:
            self.popup_message.text = 'Credentials file not found in root directory'
            self.popup.open()
        except KeyError:
            self.popup_message.text = 'called field in json doesn\'t exist.\nCheck readme for documentation'
            self.popup.open()
        except IndexError:
            self.popup_message.text = 'JSON file indices not set up correctly. \nCheck readme for documentation'

    def submit_credentials(self):
        running_app = App.get_running_app()
        try:
            url = running_app.construct_url({"appid": f"{self.ids.apikey.text}", "units": "imperial"})
            if url is None:
                self.ids.message.text = 'Please enter a valid api key'
            attributes = [self.ids.authority.text, self.ids.port.text, self.ids.database.text,
                          self.ids.username.text, self.ids.password.text,
                          self.ids.weatherauthority.text, self.ids.weatherport.text,
                          self.ids.apikey.text]
            if any(attribute.isspace() or attribute == '' for attribute in attributes):
                self.ids.message.text = 'Fill in all text boxes'
                print(self.ids.message.text)
                self.ids.authority.text, self.ids.port.text, self.ids.database.text, \
                self.ids.username.text, self.ids.password.text, \
                self.ids.weatherauthority.text, self.ids.weatherport.text, \
                self.ids.apikey.text = '', '', '', '', '', '', '', ''
                self.canvas.ask_update()
            else:
                self.ids.error.text = 'Success!'
                addition = combined_installer.Credentials(authority=attributes[0], port=attributes[1],
                                                          database=attributes[2],
                                                          username=attributes[3], password=attributes[4],
                                                          weatherauthority=attributes[5], weatherport=attributes[6],
                                                          apikey=attributes[7])
                self.forecast_rest_connection = rest.RESTConnection(self.ids.weatherauthority.text,
                                                                    self.ids.weatherport.text, '/data/2.5',
                                                                    self.ids.apikey.text)
                self.geocoding_rest_connection = rest.RESTConnection(self.ids.weatherauthority.text,
                                                                     self.ids.weatherport.text, '/geo/1.0',
                                                                     self.ids.apikey.text)

                self.forecast_rest_connection.send_request('weather', {'q': 'Lincoln'}, None, None, ConnectionError,
                                                           ConnectionError)
                running_app = App.get_running_app()
                running_app.commit(addition)
            self.ids.authority.text, self.ids.port.text, self.ids.database.text, \
            self.ids.username.text, self.ids.password.text, \
            self.ids.weatherauthority.text, self.ids.weatherport.text, \
            self.ids.apikey.text = '', '', '', '', '', '', '', ''
            print(url)
            return url

        except ValueError:
            self.popup_message.text = 'port isn\'t a valid number'
            self.popup.open()
            return
        except OperationalError:
            print('operation error')
            self.popup_message.text = 'Unable to establish a connection to the database. Please check your credentials and try again.'
            self.popup.open()
            return
        except ProgrammingError:
            print('programming error')
            self.popup_message.text = 'Incorrect database credentials. Check your password again'
            self.popup.open()
            return
        except SQLAlchemyError as sqlerror:
            self.popup_message.text = 'An error occurred while connecting to the database:\n' + str(sqlerror)
            self.popup.open()
            return
        except ConnectionError:
            self.popup_message.text = 'Couldn\'t connect to OpenWeather. Please check your API credentials.'
            self.popup.open()
            return
        except HTTPError as error:
            if error.response.status_code == 401:
                self.popup_message.text = 'Invalid API key'
                self.popup.open()
            else:
                self.popup_message.text = 'Error connecting to OpenWeather API'
                self.popup.open()

            return self.switch_screen('loading_screen')

    # def on_enter(self, *args):
    #     self.add_credentials()
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


class WindowManager(ScreenManager):
    pass


class ItineraryPage(Screen):
    pass


class TravelPlannerApp(App):

    def __init__(self):
        super().__init__()
        self.rest_connection = None
        self.credentials_window = None

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        self.credentials_window = CredentialsWindow()
        #self.credentials_window = kv.ids.credentials
        # self.credentials_window.add_credentials()
        return kv

    def construct_url(self, get_parameters=None):
        resource = 'forecast'
        if get_parameters["appid"] != '':
            url = self.rest_connection.construct_url(resource, get_parameters)
            return url

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        print('success')

    def on_records_not_loaded(self, _, error):
        self.records = ['[Failed to load records]']
        print(error)


if __name__ == '__main__':
    app = TravelPlannerApp()
    app.run()
