# configuration
import os

DATABASE_URL = 'postgresql://postgres:qwe123asd123@localhost/postgres'
#SQLALCHEMY_DATABASE_URI= 'sqlite:///sql.db'
SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or DATABASE_URL
DEBUG = True
SECRET_KEY = os.urandom(24)

