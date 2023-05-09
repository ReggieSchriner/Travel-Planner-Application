import json
from json import dumps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from lazr.restfulclient.errors import HTTPError
from mysql.connector import OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError

import rest
from travel_planner_app import combined_installer, combined_database
from travel_planner_app.combined_database import Venues, DealsDatabase

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'
COUNT = 5


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
    username = StringProperty('')
    Screen.current = 'update_ratings'
    show_venue_with_rating = StringProperty('')
    show_another_venue_with_rating = StringProperty('')
    # labelText = StringProperty('')
    average_score = StringProperty('')


class ScreenManagement(ScreenManager):
    pass


class ItineraryPage(Screen):
    pass


class TravelPlannerApp(App):
    def __init__(self, **kwargs):
        super(combined_database, self).__init__(**kwargs)
        url = DealsDatabase.construct_mysql_url('cse.unl.edu', 3306, 'zridha', 'zridha', 'q2H-sn')
        self.combined_database = DealsDatabase(url)
        self.session = self.combined_database.create_session()
        super().__init__()
        self.session = None
        self.rest_connection = None
        self.credentials_window = None
        self.popup_message = Label(text='', color='black')
        self.popup = Popup(content=self.popup_message, size=(400, 400), background='white', size_hint=(None, None))
        self.forecast_rest_connection = None
        self.geocoding_rest_connection = None

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        return kv

    def add_credentials(self):
        self.manager.current = 'credentials'
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
            layout = self.root.get_screen('credentials_screen').ids
            layout.authority.text = authority
            layout.port.text = port
            layout.database.text = database
            layout.username.text = username
            layout.password.text = ''
            layout.weatherauthority.text = weatherauthority
            layout.weatherport.text = weatherport
            layout.apikey.text = ''

        except FileNotFoundError:
            self.popup_message.text = 'The credentials json was not found in root directory'
            self.popup.open()
        except KeyError:
            self.popup_message.text = 'The field you called in json does not exist.\nCheck the readme for correct documentation'
            self.popup.open()
        except IndexError:
            self.popup_message.text = 'JSON file was not set up correctly. \nCheck the readme for correct documentation'

    def submit_credentials(self):
        # self.manager.current = 'main_menu'
        running_app = App.get_running_app()
        try:
            layout = self.root.get_screen('credentials_screen').ids
            url = running_app.construct_url({"appid": f"{layout.apikey.text}", "units": "imperial"})
            if url is None:
                layout.message.text = 'Please enter a valid api key'
            attributes = [layout.authority.text, layout.port.text, layout.database.text,
                          layout.username.text, layout.password.text,
                          layout.weatherauthority.text, layout.weatherport.text,
                          layout.apikey.text]
            if any(attribute.isspace() or attribute == '' for attribute in attributes):
                layout.message.text = 'Fill in all text boxes'
                print(layout.message.text)
                layout.authority.text, layout.port.text, layout.database.text, \
                    layout.username.text, layout.password.text, \
                    layout.weatherauthority.text, layout.weatherport.text, \
                    layout.apikey.text = '', '', '', '', '', '', '', ''
                self.canvas.ask_update()
            else:
                layout.error.text = 'Success!'
                addition = combined_installer.Credentials(authority=attributes[0], port=attributes[1],
                                                          database=attributes[2],
                                                          username=attributes[3], password=attributes[4],
                                                          weatherauthority=attributes[5], weatherport=attributes[6],
                                                          apikey=attributes[7])
                self.forecast_rest_connection = rest.RESTConnection(layout.weatherauthority.text,
                                                                    layout.weatherport.text, '/data/2.5',
                                                                    layout.apikey.text)
                self.geocoding_rest_connection = rest.RESTConnection(layout.weatherauthority.text,
                                                                     layout.weatherport.text, '/geo/1.0',
                                                                     layout.apikey.text)

                self.forecast_rest_connection.send_request('weather', {'q': 'Lincoln'}, None, None, ConnectionError,
                                                           ConnectionError)
                running_app = App.get_running_app()
                running_app.commit(addition)
            layout.authority.text, layout.port.text, layout.database.text, \
                layout.username.text, layout.password.text, \
                layout.weatherauthority.text, layout.weatherport.text, \
                layout.apikey.text = '', '', '', '', '', '', '', ''
            print(url)
            return url

        except ValueError:
            self.popup_message.text = 'port is invalid'
            self.popup.open()
        except OperationalError:
            print('operation error')
            self.popup_message.text = 'Unable to establish a connection to the database. Please try again.'
            self.popup.open()
        except ProgrammingError:
            print('programming error')
            self.popup_message.text = 'Incorrect database credentials. Please try again.'
            self.popup.open()
        except SQLAlchemyError as sqlerror:
            self.popup_message.text = 'An error occurred while connecting to the database:\n' + str(sqlerror)
            self.popup.open()
        except ConnectionError:
            self.popup_message.text = 'Cannot connect to OpenWeather API. Please try again.'
            self.popup.open()
        except HTTPError as error:
            if error.response.status_code == 401:
                self.popup_message.text = 'Invalid API key'
                self.popup.open()
            else:
                self.popup_message.text = 'Error connecting to OpenWeather API'
                self.popup.open()

    def update_ratings(self):
        venues = self.session.query(Venues)
        show_venue_with_rating = ''
        show_another_venue_with_rating = ''
        for venue in venues:

            if venue.updated_venue_score is not None:
                show_venue_with_rating += f'{venue.venue_name} - {venue.venue_score}\n'
                show_another_venue_with_rating += f'{venue.venue_name} - {venue.updated_venue_score}\n'
        self.root.get_screen('update_page').show_venue_with_rating = show_venue_with_rating
        self.root.get_screen('update_page').show_another_venue_with_rating = show_another_venue_with_rating
        self.average_score()

    def manage_scores(self, accepted_venues_list, rejected_venues_list):
        first_accepted_venues_list = accepted_venues_list.split(' ')
        accepted_venues_list = []
        first_rejected_venues_list = rejected_venues_list.split(' ')
        rejected_venues_list = []
        for i in first_rejected_venues_list:
            rejected_venues_list.append(i)
        for first_venue in first_accepted_venues_list:
            accepted_venues_list.append(first_venue)
            print(accepted_venues_list)
        venues = self.session.query(Venues)
        for venue in venues:
            for second_venue in accepted_venues_list:
                reset = None
                if venue.venue_name == second_venue:
                    score = venue.updated_venue_score
                    name = str(second_venue)
                    ints = str(score)
                    string = f'{venue.venue_score}'
                    strn = f'{score}'
                    print(string, strn, ints)
                    self.session.query(Venues).filter(Venues.venue_name == name).update({"venue_score": ints})
                    self.session.commit()

                    self.session.query(Venues).filter(Venues.venue_name == name).update(
                        {"updated_venue_score": reset})
                    self.session.commit()
                    print('The venues have been accepted!')
                    self.average_score()
                elif venue.venue_name in rejected_venues_list:
                    l = venue.venue_name
                    reset1 = None
                    print(l)
                    self.session.query(Venues).filter(Venues.venue_name == l).update(
                        {"updated_venue_score": reset1})
                    self.session.commit()
                    print('done')

    def average_score(self):
        venues = self.session.query(Venues)
        average_number = 0
        average = ''
        count_of_venues = 0
        for venue in venues:
            count_of_venues += 1
            average_number += int(venue.venue_score)
        average += f'{average_number / count_of_venues}'
        self.root.get_screen('update_page').average_score = average

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
