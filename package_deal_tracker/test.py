from unittest import TestCase
from kivy.app import App

class TestVenuePage(TestCase):
    def test_add_venue(self):
        app = App.get_running_app()
