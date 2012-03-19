from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
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
    comments = relationship('Comments')
    participant = relationship('Participants')
    #participant = relationship("Participants", uselist=False, backref="users")
    
    def __init__(self, name=None, email=None, password=None, image = None):
        self.name = name
        self.email = email
        self.password = password
        self.image = image

    def __repr__(self):
        return "%s" % self.name
    
    def _get_password(self):
        return self.password
    
    def get_name(self):
        return self.name
    
    def authentificate(self,name,passw):
        if (self.name == name and self.password == passw):
            return self


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cat_id = Column(Integer, ForeignKey('category.id'))
    user = relationship('User')
    cat = relationship('Category')
    title = Column(String(50))
    description = Column(String(120))
    html = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_target = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    lat = Column(Integer)
    lng = Column(Integer)
    inns_now = Column(Integer, default=0)
    inns_target = Column(Integer, default=100, nullable=False)
    image_link =  Column(String(220))
    video_link =  Column(String(220))
    comments = relationship('Comments')
    participants = relationship('Participants')

    def __init__(self, title=None, desc=None, html=None, user=None, loc=None, lat=None, lng=None, image=None):
        self.title = title
        self.description = desc
        self.html=html
        self.user=user
        self.location=loc
        self.lat=lat
        self.lng=lng
        self.image_link=image
    
    def __str__(self):
        return self.title

    #def __unicode__(self):
        #return self.title

    def __repr__(self):
        return "%s" % self.title

    def json(self):
        """
        Returns dict of safe attributes for passing into 
        a JSON request.
        """
        
        return dict(proj_id=self.id,
                    title=self.title,
                    description=self.description,
                    user=self.user.name,
                    lat=self.lat,
                    lng=self.lng,
                    image=self.image_link)
    def get_users(self):
        lst=[]
        for usr in self.participants:
            lst.append(usr.user)
        return lst

"""
association_table = Table('association', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('participant_id', Integer, ForeignKey('participants.id'))
)
"""


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer,primary_key = True)
    content = Column (String(220))
    date_created =  Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer,
                ForeignKey('users.id', ondelete='CASCADE'))
    project_id = Column(Integer,
                ForeignKey('projects.id', ondelete='CASCADE'))
    user = relationship('User')
    project = relationship('Projects')

    def __init__(self, content=None, user=None, project=None):
        self.content = content
        self.user = user
        self.project=project

class Participants(Base):
    __tablename__ = 'participants'
    id = Column(Integer,primary_key = True)
    project_id = Column(Integer,
                ForeignKey('projects.id', ondelete='CASCADE'))
    user_id = Column(Integer,
         ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User')
    #child = relationship("Child", uselist=False, backref="parent")
    #project = relationship('Projects', secondary=association_table)
    project = relationship('Projects')
    #project = relationship(Projects, secondary=association_table)
    
    def __init__ (self, user=None, proj=None):
        self.user=user
        self.project=proj

    def __str__(self):
        return self.user.name

 


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(String(120))
    projects = relationship('Projects')


