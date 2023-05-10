import json
from json import dumps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from mysql.connector import ProgrammingError
from sqlalchemy.exc import SQLAlchemyError

import rest
from travel_planner_app import combined_installer
from travel_planner_app.combined_database import Venues, Airport, City, Reviews

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'
COUNT = 5


class CredentialsWindow(Screen):
    Screen.current = 'credentials'

    def __init__(self, **kwargs):
        super().__init__()
        self.geocoding_rest_connection = None
        self.forecast_rest_connection = None

    def on_start(self):
        self.add_credentials()

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
            self.root.ids.authority.text = authority
            self.root.ids.port.text = port
            self.root.ids.database.text = database
            self.root.ids.username.text = username
            self.root.ids.password.text = ''
            self.root.ids.weatherauthority.text = weatherauthority
            self.root.ids.weatherport.text = weatherport
            self.root.ids.apikey.text = ''

        except IndexError:
            print('JSON file was not set up correctly.')

    def submit_credentials(self):
        running_app = App.get_running_app()
        try:
            correct_screen = self.root.get_screen('credentials').ids
            url = running_app.construct_url({"appid": f"{correct_screen.apikey.text}", "units": "imperial"})
            if url is None:
                correct_screen.message.text = 'Please enter a valid api key'
            attributes = [correct_screen.authority.text, correct_screen.port.text, correct_screen.database.text,
                          correct_screen.username.text, correct_screen.password.text,
                          correct_screen.weatherauthority.text, correct_screen.weatherport.text,
                          correct_screen.apikey.text]
            if any(attribute.isspace() or attribute == '' for attribute in attributes):
                correct_screen.message.text = 'Fill in all text boxes'
                print(correct_screen.message.text)
                correct_screen.authority.text, correct_screen.port.text, correct_screen.database.text, \
                correct_screen.username.text, correct_screen.password.text, \
                correct_screen.weatherauthority.text, correct_screen.weatherport.text, \
                correct_screen.apikey.text = '', '', '', '', '', '', '', ''
                self.canvas.ask_update()
            else:
                correct_screen.error.text = 'Success!'
                addition = combined_installer.Credentials(authority=attributes[0], port=attributes[1],
                                                          database=attributes[2],
                                                          username=attributes[3], password=attributes[4],
                                                          weatherauthority=attributes[5], weatherport=attributes[6],
                                                          apikey=attributes[7])
                self.forecast_rest_connection = rest.RESTConnection(correct_screen.weatherauthority.text,
                                                                    correct_screen.weatherport.text, '/data/2.5',
                                                                    correct_screen.apikey.text)
                self.geocoding_rest_connection = rest.RESTConnection(correct_screen.weatherauthority.text,
                                                                     correct_screen.weatherport.text, '/geo/1.0',
                                                                     correct_screen.apikey.text)

                self.forecast_rest_connection.send_request('weather', {'q': 'Lincoln'}, None, None, ConnectionError,
                                                           ConnectionError)
                running_app = App.get_running_app()
                running_app.commit(addition)
            correct_screen.authority.text, correct_screen.port.text, correct_screen.database.text, \
            correct_screen.username.text, correct_screen.password.text, \
            correct_screen.weatherauthority.text, correct_screen.weatherport.text, \
            correct_screen.apikey.text = '', '', '', '', '', '', '', ''
            print(url)
            return url

        except ValueError:
            print('port is invalid')
        except ProgrammingError:
            print('Incorrect database credentials. Please try again.')
        except SQLAlchemyError as sqlerror:
            print('An error occurred while connecting to the database:\n' + str(sqlerror))
        except ConnectionError:
            print('Cannot connect to OpenWeather API. Please try again.')


class LoadingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_next_screen, 2)

    def switch_to_next_screen(self, *args):
        self.manager.current = 'main_menu'


class MainMenu(Screen):
    Screen.current = 'menu_menu'


class ValidateLocationsPage(Screen):
    Screen.current = 'validate_page'

    def __init__(self, **kwargs):
        super().__init__()
        self.number_of_unvalidated_locations = None

    def locations_not_validated(self):
        if self.session is not None:
            airports_not_validated = self.session.query(Airport).filter_by(validated=False).all()
            cities_not_validated = self.session.query(City).filter_by(validated=False).all()
            self.number_of_unvalidated_locations = airports_not_validated + cities_not_validated

    def reviews_to_examine(self):
        if self.session is not None:
            review_to_examine = self.session.query(Reviews).filter_by(accepted=False).all()
            self.session.query(Venues).filter_by(review_to_examine).all()


class UpdateRatingsPage(Screen):
    Screen.current = 'update_ratings'
    rated_venue1 = StringProperty('')
    rated_venue2 = StringProperty('')
    average_score = StringProperty('')

    def update_ratings(self):
        venues = self.session.query(Venues)
        venue1 = ' '
        venue2 = ' '
        number_of_venues = 0
        average_number = 0
        average_score = ' '
        accepted_venues = []
        rejected_venues = []
        clear = None

        for venue in venues:
            if venue.updated_venue_score is not None:
                venue1 += f'{venue.venue_name} gets a score of {venue.venue_score}\n'
                venue2 += f'{venue.venue_name} gets a score of {venue.updated_venue_score}\n'
        self.root.get_screen('update_page').show_venue_with_rating = venue1
        self.root.get_screen('update_page').show_another_venue_with_rating = venue2
        self.average_score()

        for venue in venues:
            number_of_venues += 1
            average_number += int(venue.venue_score)
        average_score += f'{average_number / number_of_venues}'
        self.root.get_screen('update_page').average_score = average_score

        split_accepted_venues = accepted_venues.split(' ')
        split_rejected_venues = rejected_venues.split(' ')

        for value in split_accepted_venues:
            accepted_venues.append(value)
        for variable in split_rejected_venues:
            rejected_venues.append(variable)

        for venue in venues:
            for k in accepted_venues:
                if venue.venue_name == k:
                    score = venue.updated_venue_score
                    name = str(k)
                    score_string = f'{score}'
                    self.session.query(Venues).filter(Venues.venue_name == name).update({"venue_score": score_string})
                    self.session.commit()

                    self.session.query(Venues).filter(Venues.venue_name == name).update(
                        {"updated_venue_score": clear})
                    self.session.commit()
                    print('The venues have been submitted')
                elif venue.venue_name in rejected_venues:
                    venue_name = venue.venue_name
                    self.session.query(Venues).filter(Venues.venue_name == venue_name).update(
                        {"updated_venue_score": clear})
                    self.session.commit()


class WindowManager(ScreenManager):
    pass


class ItineraryPage(Screen):
    Screen.current = 'itinerary_page'


class TravelPlannerApp(App):

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.rest_connection = None

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
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
