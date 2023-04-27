from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (400, 650)


class HomeScreen(Screen):
    pass


class CityScreen(Screen):
    name = ''
    country = ''
    lat = ''
    long = ''

    def save_city_inputs(self):
        name = self.ids.name.text
        country = self.ids.country.text
        lat = self.ids.lat.text
        long = self.ids.long.text

        if len(name) > 0:
            self.name = name
        if len(country) > 0:
            self.country = country
        if len(lat) > 0:
            self.lat = lat
        if len(long) > 0:
            self.long = long


class VenueScreen(Screen):
    venue_name = ''
    city = ''
    type = ''

    def save_venue_inputs(self):
        self.venue_name = self.ids.venue_name.text
        self.city = self.ids.city.text
        self.type = self.ids.type.text
        print(self.city + self.venue_name)


class WeatherScreen(Screen):
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


class WindowManager(ScreenManager):
    pass


class EntertainmentApp(App):
    advancing = BooleanProperty(True)


kv = Builder.load_file('entertainment.kv')

if __name__ == '__main__':
    app = EntertainmentApp()
    app.run()
