import binascii
import hashlib
import os

from flask_login import UserMixin
from numpy import unicode
from sqlalchemy import Column, Unicode, String, Binary
from sqlalchemy.orm import relationship

from .base import BaseMixin
from .. import db, login


class User(db.Model, UserMixin, BaseMixin):
    __tablename__ = 'User'

    id = Column(Unicode(20), primary_key=True)
    name = Column(String(200))
    email = Column(String(50), unique=True)
    password = Column(Binary)
    candidates = relationship('Candidate', lazy='select')

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = User.hash_pass(password)

    def __repr__(self):
        return str(self.name)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def hash_pass(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash)  # return bytes

    def verify_pass(self, provided_password):
        """Verify a stored password against one provided by user"""
        stored_password = self.password.decode('ascii')
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    @staticmethod
    def filter(email):
        return User.query.filter_by(email=email).one_or_none()

    @staticmethod
    def get(id):
        return User.query.get(id)


@login.user_loader
def getuser(id):
    return User.query.get(id)
