from sqlalchemy import Column, Unicode, Integer, ForeignKey, Boolean, Date, String, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from .base import BaseMixin
from .. import db

Base = declarative_base()


class Candidate(db.Model, BaseMixin, Base):
    __tablename__ = 'Candidate'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), nullable=False)
    address = Column(Unicode(200))
    gender = Column(Boolean)
    date_of_birth = Column(Date)
    phone = Column(String(20))
    email = Column(String(50), unique=True)
    identity_no = Column(Unicode(), nullable=False)
    identity_issued_date = Column(Date)
    identity_issued_place = Column(Unicode)
    avatar = Column(URLType)
    scan_front = Column(URLType)
    scan_back = Column(URLType)
    note = Column(Unicode)
    email = Column(Integer, nullable=False)
    collaborator_id = Column(Unicode(20), ForeignKey('User.id'))
    collaborator = relationship('User')

    def __init__(self, **kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def all():
        return Candidate.query

    @staticmethod
    def filter_collaborator(user_id):
        # Nếu là admin user_id = None
        return Candidate.query.filter(or_(Candidate.collaborator_id == user_id, user_id == None)).order_by(
                Candidate.id.desc())

    @staticmethod
    def filter_by_identity_no_and_collaborator(user_id, identity):
        return Candidate.query.filter(
                and_(Candidate.collaborator_id == user_id, Candidate.identity_no == identity)).one_or_none()

    @staticmethod
    def filter_by_id_and_collaborator(user_id, id):
        return Candidate.query.filter(
                and_(Candidate.collaborator_id == user_id, Candidate.id == id)).one_or_none()

    @staticmethod
    def get(id):
        return Candidate.query.get(id)
