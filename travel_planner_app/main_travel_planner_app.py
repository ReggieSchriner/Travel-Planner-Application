import json
from json import dumps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window  # For inspection
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from lazr.restfulclient.errors import HTTPError
from mysql.connector import OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError

import rest
from travel_planner_app import combined_installer
from travel_planner_app.combined_database import Venues, DealsDatabase, Airport, City, Reviews

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'
COUNT = 5


class CredentialsWindow(Screen):
    Screen.current = 'credentials'


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
        self.unvalidated_locations = None

    def unvalidated_locations(self):
        if self.session is not None:
            unvalidated_airports = self.session.query(Airport).filter_by(validated=False).all()
            unvalidated_cities = self.session.query(City).filter_by(validated=False).all()
            self.unvalidated_locations = unvalidated_airports + unvalidated_cities
            layout = self.root.get_screen('validate_page').ids
            if len(self.unvalidated_locations) > 0:
                for unvalidated_locations in self.unvalidated_locations:
                    checkbox = CheckBox(size_hint_y=None, height=48, group='unvalidated_location_checkboxes')
                    checkbox.id = unvalidated_locations.name
                    label = Label(text=unvalidated_locations.name, color=[0, 0, 0, 1], size_hint_y=None)
                    layout.add_widget(label)
                    layout.add_widget(checkbox)

    def reviews_to_examine(self):
        if self.session is not None:
            review_to_examine = self.session.query(Reviews).filter_by(accepted=False).all()
            self.session.query(Venues).filter_by(review_to_examine).all()
        else:
            print('There is no session')

    def validate_city(self, city):
        geo_data = {
            'latitude': [],
            'longitude': [],
            'name': []
        }
        if len(geo_data['name']) > 0:
            for i in range(len(geo_data['name'])):
                if geo_data['name'][i] == city.name and self.is_location_near(geo_data['latitude'][i],
                                                                              geo_data['longitude'][i], city.latitude,
                                                                              city.longitude):
                    city.validated = True
                    self.popup_message.text = 'City successfully validated'
        else:
            print('City has been deleted')
            self.session.delete(city)
        self.session.commit()

    # def validate_airport is not complete
    def validate_location(self):
        for widget in self.root.get_screen('validate_page').ids.children:
            if isinstance(widget, CheckBox):
                if widget.active is True:
                    airport = self.session.query(Airport).filter_by(name=widget.id).first()
                    city = self.session.query(City).filter_by(name=widget.id).first()
                    if city:
                        self.unvalidated_locations.remove(city)
                    else:
                        self.unvalidated_locations.remove(airport)
                    self.session.commit()
                    self.unvalidated_locations()


class UpdateRatingsPage(Screen):
    Screen.current = 'update_ratings'
    rated_venue1 = StringProperty('')
    rated_venue2 = StringProperty('')
    average_score = StringProperty('')


class ScreenManager(ScreenManager):
    pass


class ItineraryPage(Screen):
    Screen.current = 'itinerary_page'


class TravelPlannerApp(App):
    def __init__(self, **kwargs):
        self.manager = None
        self.unvalidated_locations = None
        url = DealsDatabase.construct_mysql_url('cse.unl.edu', 3306, 'zridha', 'zridha', 'q2H-sn')
        self.combined_database = DealsDatabase(url)
        self.session = self.combined_database.create_session()
        super().__init__()
        self.session = None
        self.rest_connection = None
        self.popup_message = Label(text='', color='black')
        self.popup = Popup(content=self.popup_message, size=(400, 400), background='white', size_hint=(None, None))
        self.forecast_rest_connection = None
        self.geocoding_rest_connection = None

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file("travel_planner.kv")
        return kv

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
            # for some reason, these won't work:
            # self.root.ids.authority.text = authority
            # self.root.ids.port.text = port
            # self.root.ids.database.text = database
            # self.root.ids.username.text = username
            # self.root.ids.password.text = ''
            # self.root.ids.weatherauthority.text = weatherauthority
            # self.root.ids.weatherport.text = weatherport
            # self.root.ids.apikey.text = ''

        except KeyError:
            print('The field you called in json does not exist.')
        except IndexError:
            print('JSON file was not set up correctly.')

    def submit_credentials(self):
        running_app = App.get_running_app()
        try:
            layout = self.root.get_screen('credentials').ids
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
            print('port is invalid')
        except OperationalError:
            print('Unable to establish a connection to the database. Please try again.')
        except ProgrammingError:
            print('Incorrect database credentials. Please try again.')
        except SQLAlchemyError as sqlerror:
            print('An error occurred while connecting to the database:\n' + str(sqlerror))
        except ConnectionError:
            print('Cannot connect to OpenWeather API. Please try again.')
        except HTTPError as error:
            if error.response.status_code == 401:
                print('Invalid API key')
            else:
                print('Error connecting to OpenWeather API')

    def average_score(self):
        venues = self.session.query(Venues)
        count_of_venues = 0
        average_number = 0
        the_average = ' '
        for venue in venues:
            count_of_venues += 1
            average_number += int(venue.venue_score)
        the_average += f'{average_number / count_of_venues}'
        self.root.get_screen('update_page').average_score = the_average

    def update_ratings(self):
        venues = self.session.query(Venues)
        rated_venue1 = ' '
        rated_venue2 = ' '

        for venue in venues:
            if venue.updated_venue_score is not None:
                rated_venue1 += f'{venue.venue_name} gets a score of {venue.venue_score}\n'
                rated_venue2 += f'{venue.venue_name} gets a score of {venue.updated_venue_score}\n'
        self.root.get_screen('update_page').show_venue_with_rating = rated_venue1
        self.root.get_screen('update_page').show_another_venue_with_rating = rated_venue2
        self.average_score()

    def manage_scores(self, accepted_venues_list, rejected_venues_list):
        first_accepted_venues_list = accepted_venues_list.split(' ')
        first_rejected_venues_list = rejected_venues_list.split(' ')
        accepted_venues_list = []
        rejected_venues_list = []
        for i in first_accepted_venues_list:
            accepted_venues_list.append(i)
        for j in first_rejected_venues_list:
            rejected_venues_list.append(j)
        venues = self.session.query(Venues)
        for venue in venues:
            for k in accepted_venues_list:
                reset = None
                if venue.venue_name == k:
                    score = venue.updated_venue_score
                    name = str(k)
                    string1 = f'{venue.venue_score}'
                    string2 = f'{score}'
                    print(string1, string2, score)
                    self.session.query(Venues).filter(Venues.venue_name == name).update({"venue_score": string2})
                    self.session.commit()

                    self.session.query(Venues).filter(Venues.venue_name == name).update(
                        {"updated_venue_score": reset})
                    self.session.commit()
                    print('The venues have been accepted!')
                    self.average_score()
                elif venue.venue_name in rejected_venues_list:
                    l = venue.venue_name
                    reset_again = None
                    print(l)
                    self.session.query(Venues).filter(Venues.venue_name == l).update(
                        {"updated_venue_score": reset_again})
                    self.session.commit()
                    print('done')

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
