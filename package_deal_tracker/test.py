from unittest import TestCase
from package_deal_tracker.database import Venues, DealsDatabase, Operators
from package_deal_tracker.main import NewVenue, AddEditOperator, EditOperator
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

class TestEditOperator(TestCase):
    def setUp(self):
        # Set up the App instance
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_test', 'root', 'cse1208')
        self.deals_database = DealsDatabase(url)
        self.session = self.deals_database.create_session()
        App.get_running_app = lambda: self
        self.edit_operator = EditOperator()

    def test_submit_operator(self):
        # Set up test data
        operator = Operators(name='Test Operator Edit', rate_my_pilot_score=10)
        self.session.add(operator)
        self.session.commit()

        # Call the submit_operator method with the test operator
        self.edit_operator.submit_operator(operator=operator, name='Test Operator Edit', new_name='new name', score=1.0)

        # Check that the operator was added to the database
        edited_operator = self.session.query(Operators).filter_by(name='new name').first()
        self.assertIsNotNone(edited_operator)

        # Check that the entered data matches the data in the database
        self.assertEqual(edited_operator.name, 'new name')
        self.assertEqual(edited_operator.rate_my_pilot_score, 1.0)
