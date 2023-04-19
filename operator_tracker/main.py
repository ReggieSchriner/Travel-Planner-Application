from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from operatorapp import OperatorDatabase, Airplane, Airport, Operator


class OperatorApp(App):
    def __init__(self, **kwargs):
        super(OperatorApp, self).__init__(**kwargs)
        url = OperatorDatabase.construct_mysql_url('localhost', 3306, 'operatorapp', 'root', 'cse1208')
        self.operator_database = OperatorDatabase(url)
        self.session = self.operator_database.create_session()

    def create_airplane(self, airplane_name, airplane_range):
        try:
            new_airplane = Airplane(airplane_name=airplane_name, airplane_range=airplane_range)
            self.session.add(new_airplane)
            self.session.commit()
            print('Airplane was successfully added!')

        except NoResultFound as exception:
            self.root.ids.message.text = f'Genre cannot be found: {exception}'

        except MultipleResultsFound as exception:
            self.root.ids.message.text = f'Multiple genres with the same name are found: {exception}'

    def create_airport(self, airport_name, longitude, latitude, airport_ICAO):
        try:
            new_airport = Airport(airport_name=airport_name, longitude=longitude, latitude=latitude,
                                  airport_ICAO=airport_ICAO)
            self.session.add(new_airport)
            self.session.commit()
            print('Airport was successfully added!')

        except NoResultFound as exception:
            self.root.ids.message.text = f'Genre cannot be found: {exception}'

        except MultipleResultsFound as exception:
            self.root.ids.message.text = f'Multiple genres with the same name are found: {exception}'

    def create_operator(self, operator_name, operator_rmp_score):
        try:
            new_operator = Operator(operator_name=operator_name, operator_rmp_score=operator_rmp_score)
            self.session.add(new_operator)
            self.session.commit()
            print('Operator was successfully added!')

        except NoResultFound as exception:
            self.root.ids.message.text = f'Genre cannot be found: {exception}'

        except MultipleResultsFound as exception:
            self.root.ids.message.text = f'Multiple genres with the same name are found: {exception}'

    def edit_operator(self, update_operator_name, update_operator_rmp_score):
        try:
            new_operator = Operator(operator_name=update_operator_name, operator_rmp_score=update_operator_rmp_score)
            self.session.add(new_operator)
            self.session.commit()
            print('Operator was successfully updated!')

        except NoResultFound as exception:
            self.root.ids.message.text = f'Genre cannot be found: {exception}'

        except MultipleResultsFound as exception:
            self.root.ids.message.text = f'Multiple genres with the same name are found: {exception}'


class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    pass


class FourthWindow(Screen):
    pass


class FifthWindow(Screen):
    pass


class SixthWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('operator.kv')


class Main(App):
    def build(self):
        return kv


if __name__ == '__main__':
    app = OperatorApp()
    app.run()
