from kivy.app import App
from kivy.core.window import Window  # For inspection.
from kivy.lang import Builder
from kivy.modules import inspector  # For inspection.
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from deals import DealsDatabase, Forecasts, Venues, Operators
import tracker_installer
import mysql.connector


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    def add_venue(self):
        attributes = [self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text]
        if any(attribute.isspace() or attribute == '' for attribute in attributes) or (
                -90 > int(attributes[1]) < 90) or (-180 > int(attributes[2]) < 180):
            self.ids.message.text = 'Invalid input'
        else:
            self.ids.message.text = 'Success!'
            addition = tracker_installer.Venues(name=attributes[0], latitude=attributes[1], longitude=attributes[2],
                                                type=attributes[3])
            app = App.get_running_app()
            app.commit(addition)
        self.ids.name.text, self.ids.latitude.text, self.ids.longitude.text, self.ids.type.text = '', '', '', ''


class ScreenThree(Screen):
    def add_operator(self):
        attributes = [self.ids.name.text, self.ids.score.text]
        if any(attribute.isspace() or attribute == '' for attribute in attributes):
            self.ids.message.text = 'Invalid input'
        else:
            self.ids.message.text = 'Success!'
            addition = tracker_installer.Operators(name=attributes[0], rate_my_pilot_score=attributes[1])
            app = App.get_running_app()
            app.commit(addition)
        self.ids.name.text, self.ids.score.text = '', ''


class ScreenFour(Screen):
    def on_enter(self):
        self.ids.operators.clear_widgets()
        spinner = Spinner(text='Select an operator', values=[])
        spinner.id = 'operators'
        app = App.get_running_app()
        operators = app.get_operators()
        for operator in operators:
            spinner.values.append(str(operator).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
        spinner.bind(text=self.submit_operator)
        self.ids.operators.add_widget(spinner)

    def submit_operator(self, spinner, text):
        attributes = [self.ids.new_name.text, self.ids.score.text]
        app = App.get_running_app()

        existing_operator = app.session.query(Operators).filter_by(name=attributes[0]).first()

        if any(attribute.isspace() or attribute == '' for attribute in attributes) or existing_operator:
            self.ids.message.text = 'Invalid input'
        else:
            self.ids.message.text = 'Success!'
            selection = spinner.text
            operator = app.session.query(Operators).filter_by(name=selection).first()

            operator.name = attributes[0]
            operator.rate_my_pilot_score = attributes[1]

            app.session.commit()

        self.ids.new_name.text, self.ids.score.text = '', ''


class ScreenFive(Screen):
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
        venue_spinner.bind(text=self.get_forecast)
        self.ids.date.clear_widgets()
        date_spinner = Spinner(text='Select a date', values=[])
        date_spinner.id = 'dates'
        dates = app.get_dates()
        for date in dates:
            if date not in seen_values:
                date_spinner.values.append(str(date).replace('(', '').replace(')', '').replace("'", '').replace(',', ''))
                seen_values.add(date)
        date_spinner.bind(text=self.get_forecast)
        self.ids.date.add_widget(date_spinner)
        self.ids.venues.add_widget(venue_spinner)

    def get_forecast(self, instance, value):
        app = App.get_running_app()
        venue_spinner = self.ids.venues.children[0]
        date_spinner = self.ids.date.children[0]
        venue = venue_spinner.text
        date = date_spinner.text
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


class WindowManager(ScreenManager):
    pass


class PackageDealTracker(App):
    def __init__(self, **kwargs):
        super(PackageDealTracker, self).__init__(**kwargs)
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_d', 'root', 'cse1208')
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
        connection = mysql.connector.connect(host='localhost', port=3306, database='deals_d', user='root',
                                             password='cse1208')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def build(self):
        inspector.create_inspector(Window, self)
        kv = Builder.load_file('PackageDealTracker.kv')
        return kv


if __name__ == "__main__":
    PackageDealTracker().run()
