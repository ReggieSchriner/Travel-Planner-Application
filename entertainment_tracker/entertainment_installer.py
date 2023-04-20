from sys import stderr

from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from entertainment import EntertainmentDatabase, City, Venue, WeatherCondition


def add_starter_data(session):
    omaha = City(name='Omaha', country='United States', lat=412565, long=959345)
    cafe = Venue(name='Garden Cafe', city=omaha, type='Indoor Restaurant')
    movie_theater = Venue(name='AMC', city=omaha, type='Indoor Theater')
    arena = Venue(name='Baxter Arena', city=omaha, type='Indoor Sports Arena')

    new_york = City(name='New York', country='United States', lat=407128, long=740060)
    restaurant = Venue(name='Fogo De Chao', city=new_york, type='Indoor Restaurant')
    theater = Venue(name='drive-in', city=new_york, type='Outdoor Theater')
    stadium = Venue(name='UBS Arena', city=new_york, type='Outdoor Sports Arena')

    snow = WeatherCondition(condition_code=622, venue=cafe)
    thunder = WeatherCondition(condition_code=202, venue=stadium)
    drizzle = WeatherCondition(condition_code=312, venue=theater)
    rain = WeatherCondition(condition_code=504)
    atmosphere = WeatherCondition(condition_code=781, venue=movie_theater)
    clear = WeatherCondition(condition_code=800)
    clouds = WeatherCondition(condition_code=804)
    wind = WeatherCondition(continuous_range='Wind Speed', direction='above', threshold=24)

    session.add(omaha)
    session.add(cafe)
    session.add(movie_theater)
    session.add(arena)
    session.add(new_york)
    session.add(restaurant)
    session.add(theater)
    session.add(stadium)
    session.add(snow)
    session.add(thunder)
    session.add(drizzle)
    session.add(rain)
    session.add(atmosphere)
    session.add(clear)
    session.add(clouds)
    session.add(wind)


def main():
    try:
        url = EntertainmentDatabase.construct_mysql_url('localhost', 3306, 'movies', 'root', 'cse')
        entertainment_database = EntertainmentDatabase(url)
        EntertainmentDatabase.ensure_tables_exist()
        print('Tables created.')
        session = entertainment_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()