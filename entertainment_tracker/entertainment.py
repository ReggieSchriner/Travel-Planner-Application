from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class City(Persisted):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    name = Column(String(256))
    country = Column(String(256))
    long = Column(Integer) # divide by 10,0000 to get decimal.
    lat = Column(Integer) # ^
    venues = relationship('Venue', uselist=True, back_populates='cities')
    

class Venue(Persisted):
    __tablename__ = 'venues'
    venue_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.city_id', ondelete='CASCADE'), nullable=False)
    city = relationship('City', uselist=True, back_populates='venues')
    name = Column(String(256))
    type = Column(String(256))


class WeatherCondition(Persisted):
    __tablename__ = 'weather_conditions'
    venue_id = Column(Integer, ForeignKey('venues.venue_id', ondelete='CASCADE'), nullable=False)
    venue = relationship('Venue', uselist=True, back_populates='weather_conditions')
    condition_code = Column(Integer)
    continuous_range = Column(String(256))
    direction = Column(String(256))
    threshold = Column(Integer)


class EntertainmentDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
