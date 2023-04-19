from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from operatorapp import OperatorDatabase, Airport, Airplane, Operator


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


def main():
    try:
        url = OperatorDatabase.construct_mysql_url('localhost', 3306, 'operatorapp', 'root', 'cse1208')
        operator_database = OperatorDatabase(url)
        operator_database.ensure_tables_exist()
        print('Tables created.')
        session = operator_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
