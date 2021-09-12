from sqlalchemy import Column, Unicode, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .base import BaseMixin
from .. import db

Base = declarative_base()


class Project(db.Model, BaseMixin, Base):
    __tablename__ = 'Project'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(200), nullable=False)
    content = Column(Unicode(), nullable=False)
    demand_qty = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'))
    company = relationship('Company')

    def __init__(self, title, content, demand_qty, company):
        self.title = title
        self.content = content
        self.demand_qty = demand_qty
        self.company = company

    @staticmethod
    def all():
        return Project.query

    @staticmethod
    def get(id):
        return Project.query.get(id)
