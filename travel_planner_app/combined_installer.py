from datetime import datetime, date, timedelta
from sys import stderr
from sqlalchemy.exc import SQLAlchemyError
from combined_database import Venues, DealsDatabase, Operators, Deals, Forecasts, VenueScores, OperatorScores, \
    Credentials
from travel_planner_app.combined_database import Airport, Airplane, Operator


def add_starter_data(session):
    ORD = Airport(airport_name="ORD")
    SAN = Airport(airport_name="SAN")
    LAX = Airport(airport_name="LAX")
    DEN = Airport(airport_name="DEN")
    Bobcat = Airplane(airplane_name="Bobcat")
    Coronado = Airplane(airplane_name="Coronado")
    Dragon = Airplane(airplane_name="Dragon")
    Windy = Airplane(airplane_name="Windy")
    session.add(ORD)
    session.add(SAN)
    session.add(LAX)
    session.add(DEN)
    session.add(Bobcat)
    session.add(Coronado)
    session.add(Dragon)
    session.add(Windy)

    airport_one = Airport(airport_name='ORD', longitude=1.25530, latitude=2.64220, airport_ICAO='STCB')
    session.add(airport_one)
    airport_two = Airport(airport_name='SAN', longitude=1.022553, latitude=2.64220, airport_ICAO='AMDK')
    session.add(airport_two)
    operator_one = Operator(operator_name='Thunderbird', operator_rmp_score=9,
                            Airport=[ORD, SAN, LAX], Airplane=Bobcat)
    session.add(operator_one)
    operator_two = Operator(operator_name='Lightning', operator_rmp_score=2,
                            Airport=[ORD, DEN, LAX], Airplane=Dragon)
    session.add(operator_two)

    airplane_one = Airplane(airplane_name='Bobcat', airplane_range=700)
    session.add(airplane_one)
    airplane_two = Airplane(airplane_name='Windy', airplane_range=600)
    session.add(airplane_two)

    # create venues
    olive_garden = Venues(name='Olive Garden', latitude=1, longitude=1, type='Restaurant', score=10)
    marcus_grand_cinema = Venues(name='Marcus Grand Cinema', latitude=1, longitude=1, type='Theater', score=8)
    pinnacle_bank_arena = Venues(name='Pinnacle Bank Arena', latitude=1, longitude=1, type='Sports Arena', score=7)
    session.add_all([olive_garden, marcus_grand_cinema, pinnacle_bank_arena])
    session.commit()

    # create forecasts
    today = str(datetime.today().date())
    tomorrow = str(datetime.today() + timedelta(days=1))
    olive_garden_forecast_1 = Forecasts(venue=olive_garden, date_time=today, temperature=70, humidity=50, wind_speed=10,
                                        feels_like=75, rain=0)
    olive_garden_forecast_2 = Forecasts(venue=olive_garden, date_time=tomorrow, temperature=80, humidity=60,
                                        wind_speed=5, feels_like=85, rain=0)
    marcus_grand_cinema_forecast_1 = Forecasts(venue=marcus_grand_cinema, date_time=today, temperature=72, humidity=45,
                                               wind_speed=12, feels_like=78, rain=0)
    marcus_grand_cinema_forecast_2 = Forecasts(venue=marcus_grand_cinema, date_time=tomorrow, temperature=75,
                                               humidity=50, wind_speed=10, feels_like=80, rain=0)
    pinnacle_bank_arena_forecast_1 = Forecasts(venue=pinnacle_bank_arena, date_time=today, temperature=65, humidity=40,
                                               wind_speed=15, feels_like=70, rain=0)
    pinnacle_bank_arena_forecast_2 = Forecasts(venue=pinnacle_bank_arena, date_time=tomorrow, temperature=70,
                                               humidity=45, wind_speed=13, feels_like=75, rain=0)
    session.add_all([olive_garden_forecast_1, olive_garden_forecast_2, marcus_grand_cinema_forecast_1,
                     marcus_grand_cinema_forecast_2, pinnacle_bank_arena_forecast_1, pinnacle_bank_arena_forecast_2])
    session.commit()

    # create operators
    operator_1 = Operators(name='Operator 1', rate_my_pilot_score=4)
    operator_2 = Operators(name='Operator 2', rate_my_pilot_score=5)
    session.add_all([operator_1, operator_2])
    session.commit()

    # create deals
    olive_garden_deal = Deals(venue=olive_garden, operator=operator_1)
    marcus_grand_cinema_deal = Deals(venue=marcus_grand_cinema, operator=operator_1)
    pinnacle_bank_arena_deal = Deals(venue=pinnacle_bank_arena, operator=operator_2)
    olive_garden_deal2 = Deals(venue=olive_garden, operator=operator_2)
    session.add_all([olive_garden_deal, marcus_grand_cinema_deal, pinnacle_bank_arena_deal, olive_garden_deal2])
    session.commit()

    # create venue scores
    olive_garden_score = VenueScores(venue_id=1, score=1)
    marcus_grand_cinema_score = VenueScores(venue_id=2, score=2)
    pinnacle_bank_arena_score = VenueScores(venue_id=3, score=3)
    session.add_all([olive_garden_score, marcus_grand_cinema_score, pinnacle_bank_arena_score])
    session.commit()

    # create operator scores
    operator_1_score = OperatorScores(score=1, score_id=1, operator_id=1)
    operator_2_score = OperatorScores(score=2, score_id=2, operator_id=2)
    session.add_all([operator_1_score, operator_2_score])
    session.commit()

    # create credentials
    zridha = Credentials(username="zridha")
    ale = Credentials(username="ale")
    pfletcher = Credentials(username="pfletcher")
    session.add(zridha)
    session.add(ale)
    session.add(pfletcher)

    credentials_one = Credentials(authority='TCP', port=3306,
                                  database='combined_database', username=zridha,
                                  password='cse1208', weatherauthority='api.openweathermap.org',
                                  weatherport=443, apikey='3b759f91eadebc002f273c0a447b7ded')
    session.add(credentials_one)
    credentials_two = Credentials(authority='TCP', port=3306,
                                  database='combined_database', username=ale,
                                  password='cse1208', weatherauthority='api.openweathermap.org',
                                  weatherport=443, apikey='3b759f91eadebc002f273c0a447b7ded')
    session.add(credentials_two)
    credentials_three = Credentials(authority='TCP', port=3306,
                                    database='combined_database', username=pfletcher,
                                    password='cse1208', weatherauthority='api.openweathermap.org',
                                    weatherport=443, apikey='3b759f91eadebc002f273c0a447b7ded')
    session.add(credentials_three)


def main():
    try:
        url = DealsDatabase.construct_mysql_url('cse.unl.edu', 3306, 'zridha', 'zridha', 'q2H-sn')
        package_deal_database = DealsDatabase(url)
        package_deal_database.ensure_tables_exist()
        print('Tables created.')
        session = package_deal_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
