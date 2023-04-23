from kivy.app import App
from kivy.core.window import Window  # For inspection.
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection.
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from deals import DealsDatabase, Forecasts, Venues, Operators, VenueScores, OperatorScores
import installer
import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.logger import Logger
from datetime import datetime, timedelta
from api_key import API_KEY
from rest import RESTConnection
from json import dumps



class MainMenu(Screen):
    pass


class NewVenue(Screen):
    def add_venue(self):
        app = App.get_running_app()
        attributes = [self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text]
        existing_venue = app.session.query(Venues).filter_by(name=attributes[0]).first()
        if any(attribute.isspace() or attribute == '' for attribute in attributes):
            self.ids.message.text = 'Fill in all text boxes'
            self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text = '', '', '', ''
        elif (-90 > float(attributes[1]) < 90) or (-180 > float(attributes[2]) < 180):
            self.ids.message.text = 'Invalid longitude or latitude'
            self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text = '', '', '', ''
        elif existing_venue:
            self.ids.message.text = 'The given venue already exists'
            self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text = '', '', '', ''
        else:
            self.ids.message.text = 'Success!'
            addition = installer.Venues(name=attributes[0], latitude=attributes[1], longitude=attributes[2],
                                        type=attributes[3])
            app = App.get_running_app()
            app.commit(addition)
        self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text = '', '', '', ''


class AddEditOperator(Screen):
    def add_operator(self):
        attributes = [self.ids.name.text, self.ids.score.text]

        if any(attribute.isspace() or attribute == '' for attribute in attributes):
            self.ids.message.text = 'Fill in all text boxes'
            self.ids.new_name.text, self.ids.score.text = '', ''
        else:
            self.ids.message.text = 'Success!'
            addition = installer.Operators(name=attributes[0], rate_my_pilot_score=attributes[1])
            app = App.get_running_app()
            app.commit(addition)
        self.ids.name.text, self.ids.score.text = '', ''


class EditOperator(Screen):
    def on_enter(self):
        self.ids.operators.clear_widgets()
        spinner = Spinner(text='Select an operator', values=[])
        spinner.id = 'operators'
        app = App.get_running_app()
        operators = app.get_operators()
        for operator in operators:
            spinner.values.append(str(operator).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
        self.ids.operators.add_widget(spinner)

    def submit_operator(self):
        attributes = [self.ids.new_name.text, self.ids.score.text]
        app = App.get_running_app()
        spinner = self.ids.operators.children[0]

        existing_operator = app.session.query(Operators).filter_by(name=attributes[0]).first()

        if any(attribute.isspace() or attribute == '' for attribute in attributes):
            self.ids.message.text = 'Fill in all text boxes'
            self.ids.new_name.text, self.ids.score.text = '', ''
        elif existing_operator:
            self.ids.message.text = 'The entered operator already exists'
            self.ids.new_name.text, self.ids.score.text = '', ''
        else:
            self.ids.message.text = 'Success!'
            selection = spinner.text
            operator = app.session.query(Operators).filter_by(name=selection).first()

            operator.name = attributes[0]
            operator.rate_my_pilot_score = attributes[1]

            app.session.commit()

        self.ids.new_name.text, self.ids.score.text = '', ''


class CheckForecast(Screen):
    def on_enter(self):
        self.ids.venues.clear_widgets()
        venue_spinner = Spinner(text='Select a venue', values=[])
        venue_spinner.id = 'venues'
        app = App.get_running_app()
        venues = app.get_venues()
        seen_values = set()
        for venue in venues:
            if venue not in seen_values:
                venue_spinner.values.append(str(venue).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
                seen_values.add(venue)
        self.ids.date.clear_widgets()
        date_spinner = Spinner(text='Select a date', values=[])
        date_spinner.id = 'dates'
        today = datetime.today().date()
        dates = [today + timedelta(days=i) for i in range(5)]
        for date in dates:
            date_spinner.values.append(str(date).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
        self.ids.date.add_widget(date_spinner)
        self.ids.venues.add_widget(venue_spinner)

    def get_forecast(self):
        app = App.get_running_app()
        venue_spinner = self.ids.venues.children[0]
        date_spinner = self.ids.date.children[0]
        venue = venue_spinner.text
        date = str(date_spinner.text)
        query = f"SELECT venue_id FROM Venues WHERE name='{venue}'"
        result = app.execute_query(query)
        if result:
            venue_id = result[0][0]
            if venue != 'Select a venue' and date != 'Select a date':
                query = f"SELECT * FROM Forecasts WHERE venue_id={venue_id} AND date='{date}'"
                result = app.execute_query(query)
                if result:
                    forecast = result[0]
                    date = forecast[2]
                    temp = forecast[3]
                    humidity = forecast[4]
                    wind = forecast[5]
                    feels = forecast[6]
                    precip = forecast[7]
                    self.ids.forecast.text = f'Date:{date}, temperature (F):{temp}, humidity (%):{humidity}, wind speed (mph):{wind}, feels like (F):{feels}, precipitation (%): {precip}'
                else:
                    self.ids.forecast.text = 'No forecast for that day and venue.'


class SubmitReview(Screen):
    def on_enter(self):
        self.ids.venues.clear_widgets()
        venue_spinner = Spinner(text='Select a venue', values=[])
        venue_spinner.id = 'venues'
        app = App.get_running_app()
        venues = app.get_venues()
        seen_values = set()
        for venue in venues:
            if venue not in seen_values:
                venue_spinner.values.append(str(venue).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
                seen_values.add(venue)
        self.ids.operators.clear_widgets()
        operator_spinner = Spinner(text='Select an operator', values=[])
        operator_spinner.id = 'operators'
        app = App.get_running_app()
        operators = app.get_operators()
        for operator in operators:
            operator_spinner.values.append(str(operator).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
        self.ids.venues.add_widget(venue_spinner)
        self.ids.operators.add_widget(operator_spinner)

    def submit_scores(self):
        app = App.get_running_app()
        venue_spinner = self.ids.venues.children[0]
        venue_selection = venue_spinner.text
        venue_score = self.ids.venue_score.text
        operator_spinner = self.ids.operators.children[0]
        operator_selection = operator_spinner.text
        operator_score = self.ids.operator_score.text
        venue_scores_length = 0
        operator_scores_length = 0
        venue_score_total = 0
        operator_score_total = 0

        if venue_selection != 'Select a venue':
            if venue_score.isspace() or venue_score == '':
                self.ids.message.text = 'Please enter a venue score'
            else:
                venue = app.session.query(Venues).filter_by(name=venue_selection).first()
                venue_id = venue.venue_id
                score = venue_score
                last_id = int(app.session.query(VenueScores.score_id).order_by(VenueScores.score_id.desc()).first()[0])
                score_id = last_id + 1
                addition = installer.VenueScores(score=score, venue_id=venue_id, score_id=score_id)
                app.commit(addition)
                app.session.commit()
                self.ids.message.text = 'Success!'
                self.ids.venue_score.text = ''
                query = app.session.query(VenueScores.score).filter(VenueScores.venue_id == venue_id)
                venue_scores = query.all()
                for score, in venue_scores:
                    venue_score_total += score
                    venue_scores_length += 1
                average_score = (venue_score_total//venue_scores_length)
                venue.score = average_score
                app.session.commit()

        if operator_selection != 'Select an operator':
            if operator_score.isspace() or operator_score == '':
                self.ids.message.text = 'Please enter an operator score'
            else:
                operator = app.session.query(Operators).filter_by(name=operator_selection).first()
                operator_id = operator.operator_id
                score = operator_score
                last_id = int(app.session.query(OperatorScores.score_id).order_by(OperatorScores.score_id.desc()).first()[0])
                score_id = last_id + 1
                addition = installer.OperatorScores(score=score, operator_id=operator_id, score_id=score_id)
                app.commit(addition)
                app.session.commit()
                self.ids.message.text = 'Success!'
                self.ids.operator_score.text = ''
                query = app.session.query(OperatorScores.score).filter(OperatorScores.operator_id == operator_id)
                operator_scores = query.all()
                for score, in operator_scores:
                    operator_score_total += score
                    operator_scores_length += 1
                average_score = (operator_score_total//operator_scores_length)
                operator.rate_my_pilot_score = average_score
                app.session.commit()

class WindowManager(ScreenManager):
    pass


class PackageDealTracker(App):
    def __init__(self, **kwargs):
        super(PackageDealTracker, self).__init__(**kwargs)
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'package_deals', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()

    def commit(self, addition):
        self.session.add(addition)
        self.session.commit()

    def pull_operator(self, operator):
        query = self.session.query(Operators)
        return query

    def get_venues(self):
        query = self.session.query(Venues.name)
        return query

    def get_dates(self):
        query = self.session.query(Forecasts.date)
        return query

    def get_operators(self):
        query = self.session.query(Operators.name)
        return query

    def execute_query(self, query):
        connection = mysql.connector.connect(host='localhost', port=3306, database='package_deals', user='root',
                                             password='cse1208')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    records = ListProperty([])

    def load_records(self):
        self.records = []
        connection = RESTConnection('api.openweathermap.org', 443, '/data/2.5')
        connection.send_request(
            'forecast',
            {
                'appid': API_KEY,
                'lat': UNL_LATITUDE,
                'lon': UNL_LONGITUDE,
                'units': UNITS,
            },
            None,
            self.on_records_loaded,
            self.on_records_not_loaded,
            self.on_records_not_loaded
        )

    def on_records_loaded(self, _, response):
        print(dumps(response, indent=4, sort_keys=True))
        self.records = [format_forecast_record(response)]

    def on_records_not_loaded(self, _, error):
        self.records = ['[Failed to load records]']
        Logger.error(f'{self.__class__.__name__}: {error}')

    def to_human_readable_time(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%A %I:%M %p')

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file('PackageDealTracker.kv')
        return kv

UNL_LATITUDE = 40.8207
UNL_LONGITUDE = -96.7005
UNITS = 'imperial'


class Record(Label):
    pass


class Records(BoxLayout):
    records = ListProperty([])

    def rebuild(self):
        self.clear_widgets()
        for record in self.records:
            self.add_widget(Record(text=record))

    def on_records(self, _, __):
        self.rebuild()



if __name__ == "__main__":
    PackageDealTracker().run()
