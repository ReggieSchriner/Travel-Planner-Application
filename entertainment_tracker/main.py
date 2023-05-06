from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from entertainment import EntertainmentDatabase, City, Venue, WeatherCondition
import mysql.connector

Window.size = (400, 650)


class HomeScreen(Screen):
    pass


class CityScreen(Screen):
    open_popup = True
    name = StringProperty('')

    def save_city_inputs(self):
        app = App.get_running_app()
        name = self.ids.name.text
        self.name = name
        country = self.ids.country.text
        lat = self.ids.lat.text
        long = self.ids.long.text

        if any(attribute.isspace() or attribute == '' for attribute in [name, country, lat, long]):
            self.ids.error.text = 'Please fill in all the blanks'
            self.open_popup = False
        else:
            self.ids.error.text = ''
            self.open_popup = True
            lat = int(float(lat) * 10000)
            long = int(float(long) * 10000)
            self.name = name
            # addition = City(name=name, country=country, lat=int(lat), long=int(long))
            # app.commit(addition)

    def show_popup(self):
        popup = CityPopup(self)
        popup.open()


class CityPopup(Popup):
    def __init__(self, obj, **kwargs):
        super(CityPopup, self).__init__(**kwargs)
        self.obj = obj


venue = ''


class VenueScreen(Screen):
    open_weather_screen = True

    def save_venue_inputs(self):
        app = App.get_running_app()
        venue_name = self.ids.venue_name.text
        city = self.ids.city.text
        venue_type = self.ids.type.text

        if any(attribute.isspace() or attribute == '' for attribute in [venue_name, city, type]):
            self.ids.error.text = 'Please fill in all of the blanks.'
            self.open_weather_screen = False
        else:
            open_weather_screen = True
            self.ids.error.text = ''
            # addition = Venue(name=venue_name, city=city, type=type)
            # app.commit(addition)


class WeatherScreen(Screen):
    venue = None
    thunderstorm = ''
    drizzle = ''
    rain = ''
    snow = ''
    atmosphere = ''
    clear = ''
    clouds = ''

    temp_bound = ''
    temp = None
    humidity_bound = ''
    humidity = None
    wind_speed = None

    def save_weather_inputs(self):
        self.thunderstorm = self.ids.thunderstorm.state
        self.drizzle = self.ids.drizzle.state
        self.rain = self.ids.rain.state
        self.snow = self.ids.snow.state
        self.atmosphere = self.ids.atmosphere.state
        self.clear = self.ids.clear_weather.state
        self.clouds = self.ids.clouds.state

        if len(self.ids.temp.text) > 0:
            self.temp_bound = self.ids.temp_bound.text
            self.temp = int(self.ids.temp.text)
        else:
            self.temp = None

        if len(self.ids.humidity.text) > 0:
            self.humidity_bound = self.ids.humidity_bound.text
            self.humidity = int(self.ids.humidity.text)
        else:
            self.humidity = None

        if len(self.ids.wind_speed.text) > 0:
            self.wind_speed = int(self.ids.wind_speed.text)
        else:
            self.wind_speed = None

        if self.thunderstorm == 'down':
            # addition = WeatherCondition(condition_code=2, venue=)
            pass
        elif self.drizzle == 'down':
            pass
        elif self.rain == 'down':
            pass
        elif self.snow == 'down':
            pass
        elif self.atmosphere == 'down':
            pass
        elif self.clear == 'down':
            pass
        elif self.clouds == 'down':
            pass


class WindowManager(ScreenManager):
    pass


class EntertainmentApp(App):
    advancing = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(EntertainmentApp, self).__init__(**kwargs)
        url = EntertainmentDatabase.construct_mysql_url('localhost', 3306, 'package_deals', 'root', 'cse1208')
        self.entertainment_database = EntertainmentDatabase(url)
        self.session = self.entertainment_database.create_session()

    def commit_to_db(self, addition):
        self.session.add(addition)
        self.session.commit()


if __name__ == '__main__':
    app = EntertainmentApp()
    app.run()
