from datetime import datetime

from sqlalchemy import Column, Unicode, Integer, ForeignKey, Boolean, Date, String, and_, or_, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from .base import BaseMixin
from .. import db

Base = declarative_base()


class Recruitment(db.Model, BaseMixin, Base):
    __tablename__ = 'Recruitment'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('Candidate.id'))
    candidate = relationship('Candidate')
    project_id = Column(Integer, ForeignKey('Project.id'))
    project = relationship('Project')
    create_datetime = Column(DateTime, default=datetime.now())

    def __init__(self, candidate, project):
        self.candidate = candidate
        self.project = project

    @staticmethod
    def filter(candidate_id, project_id):
        return Recruitment.query \
            .filter(and_(Recruitment.candidate_id == candidate_id, Recruitment.project_id == project_id)) \
            .one_or_none()
