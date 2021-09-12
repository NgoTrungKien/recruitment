import os
from urllib import parse

class Config(object):
    # Security Key
    SECRET_KEY = os.environ.get('SECRET_KEY') or '08172019'

    # SQL Connection
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_DATABASE_URI = "sqlite:///job_board.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
