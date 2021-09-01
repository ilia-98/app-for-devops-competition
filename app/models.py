from flask_login import UserMixin
from dataclasses import dataclass
from sqlalchemy import Column, Integer, Text, String, Float, ForeignKey, Boolean, Date, DateTime, Interval
from sqlalchemy.orm import relationship, backref

from app.database import Base


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(Text)

    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        return f'{self.message}'


@dataclass
class CarBrands(Base):
    __tablename__ = 'car_brands'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    body_type = Column(String(100))

    def __init__(self, name=None, body_type=None):
        self.name = name
        self.body_type = body_type

    def __repr__(self):
        return f'{self.name}'

    def as_dict(self):
        return {
            'id': self.id,
            'registration_number': self.name,
            'year': self.body_type
        }


@dataclass
class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('car_brands.id'))
    registration_number = Column(String(100))
    year = Column(Integer)
    mileage = Column(Integer)
    price = Column(Float)
    rental_day_price = Column(Float)
    status = Column(Boolean, default=True)

    brand = relationship('CarBrands', backref=backref('cars', lazy=True))

    def __init__(self, registration_number=None, year=None, mileage=None, price=None,
                 rental_day_price=None, status=None, brand=None):
        self.registration_number = registration_number
        self.year = year
        self.mileage = mileage
        self.price = price
        self.rental_day_price = rental_day_price
        self.status = status
        self.brand = brand

    def __repr__(self):
        return f'{self.brand.name} {self.registration_number}'

    def as_dict(self):
        return {
            'id': self.id,
            'registration_number': self.registration_number,
            'year': self.year,
            'mileage': self.mileage,
            'price': self.price,
            'rental_day_price': self.rental_day_price,
            'status': self.status,
            'brand': self.brand.as_dict()
        }


@dataclass
class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    gender = Column(Boolean, default=True)
    birth_date = Column(Date)
    address = Column(String(100))
    phone_number = Column(String(100))
    passport = Column(String(100))

    def __init__(self, full_name=None, gender=None, birth_date=None, address=None, phone_number=None, passport=None):
        self.full_name = full_name
        self.gender = gender
        self.birth_date = birth_date
        self.address = address
        self.phone_number = phone_number
        self.passport = passport

    def __repr__(self):
        return f'{self.full_name}'

    def as_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'address': self.address,
            'phone_number': self.phone_number,
            'passport': self.passport
        }


@dataclass
class Rental(Base):
    __tablename__ = 'rental'
    id = Column(Integer, primary_key=True)
    issue_date = Column(DateTime)
    rental_period = Column(Integer)
    return_date = Column(DateTime)
    car_id = Column(Integer, ForeignKey('cars.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    rental_price = Column(Integer)
    employee = Column(String(100))

    car = relationship('Cars', backref=backref('rentals', lazy=True))
    client = relationship('Clients', backref=backref('rentals', lazy=True))

    def __init__(self, issue_date=None, rental_period=None, return_date=None, car=None,
                 client=None, rental_price=None, employee=None):
        self.issue_date = issue_date
        self.rental_period = rental_period
        self.return_date = return_date
        self.car = car
        self.client = client
        self.rental_price = rental_price
        self.employee = employee

    def as_dict(self):
        return {
            'id': self.id,
            'issue_date': self.issue_date,
            'rental_period': self.rental_period,
            'return_date': self.return_date,
            'car': self.car.as_dict(),
            'client': self.client.as_dict(),
            'rental_price': self.rental_price,
            'employee': self.employee
        }


class Employee(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        try:
            return str(f'{self.id}|{self.username}|{self.password}')
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f'{self.username}'
