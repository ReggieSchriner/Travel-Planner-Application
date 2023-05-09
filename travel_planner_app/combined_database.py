import sqlalchemy
from sqlalchemy import Table, create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Persisted = declarative_base()


class Deals(Persisted):
    __tablename__ = 'Deals'
    deal_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('Venues.venue_id'))
    operator_id = Column(Integer, ForeignKey('Operators.operator_id'))
    venue = relationship("Venues", back_populates="deals")
    operator = relationship("Operators", back_populates="deals")


class Venues(Persisted):
    __tablename__ = 'Venues'
    venue_id = Column(Integer, primary_key=True)
    venue_name = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    type = Column(String(256), nullable=False)
    venue_score = Column(Integer)
    updated_venue_score = Column(Integer)
    deals = relationship("Deals", back_populates="venue")
    forecasts = relationship("Forecasts", back_populates="venue")


class City(Persisted):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    name = Column(String(256))
    country = Column(String(256))
    long = Column(Integer)  # divide by 10,0000 to get decimal.
    lat = Column(Integer)  # ^
    venues = relationship('Venue', uselist=True, back_populates='cities')


class WeatherCondition(Persisted):
    __tablename__ = 'weather_conditions'
    weather_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.venue_id', ondelete='CASCADE'), nullable=False)
    venue = relationship('Venue', uselist=True, back_populates='weather_conditions')
    condition_code = Column(Integer)
    continuous_range = Column(String(256))
    direction = Column(String(256))
    threshold = Column(Integer)


class Operators(Persisted):
    __tablename__ = 'Operators'
    operator_id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    rate_my_pilot_score = Column(Float, nullable=False)
    deals = relationship("Deals", back_populates="operator")


class Forecasts(Persisted):
    __tablename__ = 'Forecasts'
    forecast_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('Venues.venue_id'))
    date_time = Column(String(256), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    rain = Column(Float, nullable=False)
    venue = relationship("Venues", back_populates="forecasts")


class OperatorScores(Persisted):
    __tablename__ = 'OperatorScores'
    score_id = Column(Integer, primary_key=True)
    operator_id = Column(Integer, ForeignKey('Operators.operator_id'))
    score = Column(Integer)


class Credentials(Persisted):
    __tablename__ = 'Credentials'
    credentials_id = Column(Integer, primary_key=True)
    authority = Column(String(256), nullable=False)
    port = Column(Integer, nullable=False)
    database = Column(String(256), nullable=False)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    weatherauthority = Column(String(256), nullable=False)
    weatherport = Column(Integer, nullable=False)
    apikey = Column(String(256), nullable=False)


class ItineraryEntries(Persisted):
    __tablename__ = 'ItineraryEntries'
    entry_id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, nullable=False)
    itinerary_selected = Column(sqlalchemy.Boolean, nullable=False)
    day = Column(Integer, nullable=False)
    city = Column(String(256), nullable=False)
    venue = Column(String(256), nullable=False)


OperatorAirport = Table('OperatorAirport', Persisted.metadata,
                        Column('operator_id', Integer, ForeignKey('operators.operator_id'), primary_key=True),
                        Column('airport_id', Integer, ForeignKey('airports.airport_id'), primary_key=True),
                        Column('name', Integer),
                        )

OperatorAirplane = Table('OperatorAirplane', Persisted.metadata,
                         Column('operator_id', Integer, ForeignKey('operators.operator_id'), primary_key=True),
                         Column('airplane_id', Integer, ForeignKey('airplanes.airplane_id'), primary_key=True),
                         Column('name', Integer),
                         )


class Airplane(Persisted):
    __tablename__ = 'airplanes'
    airplane_id = Column(Integer, primary_key=True)
    airplane_name = Column(String(256), nullable=False)
    airplane_range = Column(Integer)
    Operator = relationship('Operator', uselist=False, secondary=OperatorAirplane, back_populates='Airplane')


class Airport(Persisted):
    __tablename__ = 'airports'
    airport_id = Column(Integer, primary_key=True)
    airport_name = Column(String(256), nullable=False)
    longitude = Column(Float(precision='4,2'))
    latitude = Column(Float(precision='4,2'))
    airport_ICAO = Column(String(256))
    Operator = relationship('Operator', uselist=True, secondary=OperatorAirport, back_populates='Airport')


class Operator(Persisted):
    __tablename__ = 'operators'
    operator_id = Column(Integer, primary_key=True)
    operator_name = Column(String(256), nullable=False)
    operator_rmp_score = Column(Integer)
    Airport = relationship('Airport', uselist=True, secondary=OperatorAirport, back_populates='Operator')
    Airplane = relationship('Airplane', uselist=False, secondary=OperatorAirplane, back_populates='Operator')


class DealsDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def drop_all_tables(self):
        Persisted.metadata.drop_all(self.engine)

    def create_session(self):
        return self.Session()
