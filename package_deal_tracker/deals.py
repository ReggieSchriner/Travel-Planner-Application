from sqlalchemy import Table
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
    score = Column(Integer, nullable=False)
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
    date = Column(String(256), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    precipitation = Column(Float, nullable=False)
    venue = relationship("Venues", back_populates="forecasts")

class OperatorScores(Persisted):
    __tablename__ = 'OperatorScores'
    score_id = Column(Integer, primary_key=True)
    operator_id = Column(Integer, ForeignKey('Operators.operator_id'))

class VenueScore(Persisted):
    __tablename__ = 'VenueScores'
    score_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('Venues.venue_id'))

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

    def create_session(self):
        return self.Session()
