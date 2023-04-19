from datetime import datetime, date, timedelta
from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from deals import Venues, DealsDatabase, Operators, Deals, Forecasts


def add_starter_data(session):
    # create venues
    olive_garden = Venues(name='Olive Garden', latitude=1, longitude=1, type='Restaurant')
    marcus_grand_cinema = Venues(name='Marcus Grand Cinema', latitude=1, longitude=1, type='Theater')
    pinnacle_bank_arena = Venues(name='Pinnacle Bank Arena', latitude=1, longitude=1, type='Sports Arena')
    session.add_all([olive_garden, marcus_grand_cinema, pinnacle_bank_arena])
    session.commit()

    # create forecasts
    today = str(datetime.today().date())
    tomorrow = str(date.today() + timedelta(days=1))
    olive_garden_forecast_1 = Forecasts(venue=olive_garden, date=today, temperature=70, humidity=50, wind_speed=10, feels_like=75, precipitation=0)
    olive_garden_forecast_2 = Forecasts(venue=olive_garden, date=tomorrow, temperature=80, humidity=60, wind_speed=5, feels_like=85, precipitation=0)
    marcus_grand_cinema_forecast_1 = Forecasts(venue=marcus_grand_cinema, date=today, temperature=72, humidity=45, wind_speed=12, feels_like=78, precipitation=0)
    marcus_grand_cinema_forecast_2 = Forecasts(venue=marcus_grand_cinema, date=tomorrow, temperature=75, humidity=50, wind_speed=10, feels_like=80, precipitation=0)
    pinnacle_bank_arena_forecast_1 = Forecasts(venue=pinnacle_bank_arena, date=today, temperature=65, humidity=40, wind_speed=15, feels_like=70, precipitation=0)
    pinnacle_bank_arena_forecast_2 = Forecasts(venue=pinnacle_bank_arena, date=tomorrow, temperature=70, humidity=45, wind_speed=13, feels_like=75, precipitation=0)
    session.add_all([olive_garden_forecast_1, olive_garden_forecast_2, marcus_grand_cinema_forecast_1, marcus_grand_cinema_forecast_2, pinnacle_bank_arena_forecast_1, pinnacle_bank_arena_forecast_2])
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
    olive_garden_deal2 = Deals(venue=olive_garden, operator= operator_2)
    session.add_all([olive_garden_deal, marcus_grand_cinema_deal, pinnacle_bank_arena_deal, olive_garden_deal2])
    session.commit()


def main():
    try:
        url = DealsDatabase.construct_mysql_url('localhost', 3306, 'deals_d', 'root', 'cse1208')
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
