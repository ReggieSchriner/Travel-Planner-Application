from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
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
    name = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    type = Column(String(256), nullable=False)
    score = Column(Integer)
    deals = relationship("Deals", back_populates="venue")
    forecasts = relationship("Forecasts", back_populates="venue")


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


class VenueScores(Persisted):
    __tablename__ = 'VenueScores'
    score_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('Venues.venue_id'))
    score = Column(Integer, nullable=False)


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

    def create_session(self):
        return self.Session()
