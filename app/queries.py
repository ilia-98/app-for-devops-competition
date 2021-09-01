from flask_login import current_user
from sqlalchemy.sql.functions import now

from app import utils
from app.database import db_session
from app.models import Rental, Clients, Cars, CarBrands


def get_rental():
    active_rental = db_session.query(Rental).filter(Rental.return_date == None).all()
    finished_rental = db_session.query(Rental).filter(Rental.return_date != None).all()
    # db_session.query(Rental).join(Rental.car).filter(Cars.status == False).all()
    return {'active_rental': active_rental, 'finished_rental': finished_rental}


def add_rental(data):
    if data.get('is_new_client', 'true') == 'true':
        client_attrs = {
            'full_name': data.get('full_name'),
            'gender': bool(int(data.get('gender'))),
            'birth_date': utils.to_date(data.get('birth_date')),
            'address': data.get('address'),
            'phone_number': data.get('phone_number'),
            'passport': data.get('passport')
        }

        for key, value in client_attrs.items():
            if key == 'gender':
                continue
            if not value:
                db_session.rollback()
                return key, 'Проверьте введенные данные'

        client = Clients(**client_attrs)
        db_session.add(client)
        db_session.flush()
        db_session.refresh(client)
    else:
        client_id = data.get('client_id')
        client = db_session.query(Clients).filter(Clients.id == client_id).first()

    car_id = data.get('car_id')
    car = db_session.query(Cars).filter(Cars.id == car_id).first()
    if not car:
        db_session.rollback()
        return 'car_id', 'Проверьте введенные данные'
    car.status = False

    if not data.get('issue_date'):
        return 'issue_date', 'Проверьте введенные данные'
    if not data.get('issue_time'):
        return 'issue_time', 'Проверьте введенные данные'

    rental_attrs = {
        'issue_date': utils.to_datetime(data['issue_date'], data['issue_time']),
        'rental_period': utils.to_int(data.get('rental_period')),
        'rental_price': utils.to_int(data.get('rental_price')),
        'employee': current_user.username,
        'car': car,
        'client': client
    }

    for key, value in rental_attrs.items():
        if not value:
            db_session.rollback()
            return key, 'Проверьте введенные данные'

    rental = Rental(**rental_attrs)
    db_session.add(rental)
    db_session.commit()
    return None, 'ok'


def finish_rental(id):
    if not id:
        return 'error'
    rental = db_session.query(Rental).filter(Rental.id == id).first()
    rental.car.status = True
    rental.return_date = now()
    db_session.commit()
    return 'ok'


def get_clients():
    clients = Clients.query.all()
    return clients


def get_cars():
    cars = Cars.query.all()
    return cars


def add_car(data):
    if data.get('is_new_brand', 'true') == 'true':
        brand_attrs = {
            'name': data.get('name'),
            'body_type': data.get('body_type')
        }
        for key, value in brand_attrs.items():
            if not value:
                return key, 'Проверьте введенные данные'
        brand = CarBrands(**brand_attrs)
        db_session.add(brand)
        db_session.flush()
        db_session.refresh(brand)
    else:
        brand_id = data.get('brand_id')
        brand = db_session.query(CarBrands).filter(CarBrands.id == brand_id).first()

    car_attrs = {
        'registration_number': data.get('registration_number'),
        'year': utils.to_int(data.get('year')),
        'mileage': utils.to_int(data.get('mileage')),
        'price': utils.to_float(data.get('price')),
        'rental_day_price': utils.to_float(data.get('rental_day_price')),
        'status': True,
        'brand': brand
    }
    for key, value in car_attrs.items():
        if not value:
            db_session.rollback()
            return key, 'Проверьте введенные данные'
    car = Cars(**car_attrs)
    db_session.add(car)
    db_session.commit()
    return None, 'ok'