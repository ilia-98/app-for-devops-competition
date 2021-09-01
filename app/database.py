from app import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date



engine = create_engine(Settings.DB_CONN_STRING)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import app.models as models
    Base.metadata.create_all(bind=engine)
    cars = models.Cars.query.all()
    if cars:
        return
    cars = [
        models.Cars('А226АК01', 2010, 90000, 690000, 500, True, models.CarBrands('Toyota Corolla', 'Седан')),
        models.Cars('Е900ВК27', 1998, 210000, 300000, 300, False, models.CarBrands('Honda Civic', 'Хэтчбек')),
        models.Cars('Р038СУ777', 2016, 61000, 2050000, 900, True, models.CarBrands('BMW 5-Series', 'Универсал')),
        models.Cars('М595КЕ46', 2013, 110000, 570000, 450, True, models.CarBrands('Ford Fiesta', 'Хэтчбек')),
        models.Cars('С204ЕМ23', 2015, 130000, 1800000, 850, True, models.CarBrands('Audi A6', 'Седан'))
    ]
    for car in cars:
        db_session.add(car)
        db_session.flush()
        db_session.refresh(car)
    clients = [
        models.Clients('Зайцев Осип Юлианович', True, date(1976, 4, 24), 'ул.Новая 23, кв 34', '+7(111)230-57-44', '8181 323321'),
        models.Clients('Савельев Наум Валерьевич', True, date(1982, 8, 10), 'ул.Северная 62, кв 112', '+7(181)267-84-23', '9163 736542'),
        models.Clients('Ширяева Надежда Владимировна', False, date(1986, 2, 17), 'ул.Ленина 4, кв 12', '+7(649)214-94-04', '1675 235153')
    ]
    for client in clients:
        db_session.add(client)
        db_session.flush()
        db_session.refresh(client)
    rentals = [
        models.Rental(datetime(2021, 5, 23, 14, 34), 5, datetime(2021, 5, 27, 17, 21), cars[0], clients[1], 2500, 'DOMEN\\manager'),
        models.Rental(datetime(2021, 7, 29, 11, 43), 11, None, cars[1], clients[2], 3300, 'DOMEN\\manager')
    ]
    for rental in rentals:
        db_session.add(rental)
        db_session.flush()
        db_session.refresh(rental)
    db_session.commit()

