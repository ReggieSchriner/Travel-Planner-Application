from datetime import datetime
from unittest import TestCase

from kivy.uix.spinner import Spinner, SpinnerOption
from requests import patch

from package_deal_tracker.database import Venues, DealsDatabase, Operators, Forecasts, OperatorScores, VenueScores, \
    Deals
from package_deal_tracker.main import NewVenue, AddEditOperator, EditOperator, CheckForecast, SubmitReview
from kivy.app import App


class TestAddVenue(TestCase):
    def setUp(self):
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_test', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()
        App.get_running_app = lambda: self
        self.venue = Venues(name='Olive Garden', latitude=1, longitude=1, type='Restaurant', score=10)

    def test_add_venue_to_database(self):
        new_venue = NewVenue()
        new_venue.add_venue(self.venue)
        added_venue = self.session.query(Venues).filter_by(name='Olive Garden').first()
        self.assertIsNotNone(added_venue)
        self.assertEqual(added_venue.name, 'Olive Garden')
        self.assertEqual(added_venue.latitude, 1)
        self.assertEqual(added_venue.longitude, 1)
        self.assertEqual(added_venue.type, 'Restaurant')
        self.assertEqual(added_venue.score, 10)


class TestAddEditOperator(TestCase):
    def setUp(self):
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_test', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()
        App.get_running_app = lambda: self
        self.operator = Operators(name='Test Operator', rate_my_pilot_score=5)

    def test_add_operator_to_database(self):
        add_edit_operator = AddEditOperator()
        add_edit_operator.add_operator(self.operator)
        added_operator = self.session.query(Operators).filter_by(name='Test Operator').first()
        self.assertIsNotNone(added_operator)
        self.assertEqual(added_operator.name, 'Test Operator')
        self.assertEqual(added_operator.rate_my_pilot_score, 5)


class TestCheckForecast(TestCase):
    def setUp(self):
        # Set up the App instance
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_test', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()
        self.app = App()
        App.get_running_app = lambda: self.app
        self.check_forecast = CheckForecast()

        # Add a mock implementation of the execute_query method to the app object
        self.app.execute_query = lambda query: [[0]]
    def test_get_forecast(self):
        # Set up test data
        venue = 'Test Venue'
        date = '2022-01-01'

        self.session.query(Forecasts).filter(Forecasts.forecast_id == 100).delete()
        self.session.commit()

        # Insert test data into the Forecasts table
        forecast_id = 100
        venue_id = 1
        date_time = f"{date} 12:00:00"
        temperature = 70.0
        feels_like = 75.0
        humidity = 50.0
        wind_speed = 10.0
        rain = 20.0
        forecast = Forecasts(forecast_id=forecast_id, venue_id=venue_id, date_time=date_time,
                             temperature=temperature, feels_like=feels_like, humidity=humidity,
                             wind_speed=wind_speed, rain=rain)
        self.session.add(forecast)
        self.session.commit()

        # Create dummy objects for the venue and date values
        venue_spinner = type('', (), {'text': venue})()
        date_spinner = type('', (), {'text': date})()

        # Set up the expected forecast as a dictionary with the test data values
        expected_forecast = {
            "date_time": date_time,
            "temperature": temperature,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain": rain
        }

        # Call the get_forecast method on an instance of the CheckForecast class and pass in the test data, dummy objects, and app object
        forecast = self.check_forecast.get_forecast(date=date, venue=venue, venue_spinner=venue_spinner, date_spinner=date_spinner, app=self.app, forecast={
            "date_time": date_time,
            "temperature": temperature,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain": rain
        })

        # Check if the returned forecast matches the expected forecast
        self.assertEqual(forecast, expected_forecast)
