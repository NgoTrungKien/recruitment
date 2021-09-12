from sqlalchemy import Unicode, String, Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

from .base import BaseMixin
from .. import db

Base = declarative_base()


class Company(db.Model, BaseMixin, Base):
    __tablename__ = 'Company'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False, unique=True)
    address = Column(Unicode(200), nullable=False)
    phone = Column(String)
    email = Column(String)  # EmailType)
    website = Column(String)  # URLType)
    logo = Column(String)  # URLType)
    active = Column(Boolean, default=True)

    def __init__(self, name, address, phone, email, website, logo):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.website = website
        self.logo = logo

    @staticmethod
    def get(id):
        return Company.query.get(id)

    @staticmethod
    def filter(name):
        return Company.query.filter(Company.name == name).one_or_none()

    @staticmethod
    def all():
        return Company.query.filter(Company.active == True)
