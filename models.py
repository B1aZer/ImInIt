from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime,timedelta


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    date_joined = Column(DateTime, default=datetime.utcnow)
    password = Column(String(80))
    projects = relationship('Projects')
    
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
    
    def _get_password(self):
        return self.password
    
    def get_name(self):
        return self.name

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cat_id = Column(Integer, ForeignKey('category.id'))
    user = relationship('User')
    cat = relationship('Category')
    title = Column(String(50))
    description = Column(String(120))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_target = Column(DateTime, default=datetime.utcnow)
    inns_now = Column(Integer, default=0)
    inns_target = Column(Integer, default=100, nullable=False)
    image_link =  Column(String(220))

    def __init__(self, title=None, desc=None, user=None, image=None):
        self.title = title
        self.description = desc
        self.user=user
        self.image_link=image
    
    def __repr__(self):
        return '<Proj %r>' % (self.title)
    




class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(String(120))
    projects = relationship('Projects')


