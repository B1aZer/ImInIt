# -*- coding: utf-8 -*-
#from sqlalchemy import db.Column, db.Integer, db.String, db.DateTime, db.ForeignKey, db.Table, select, func
#from sqlalchemy.orm import db.relationship, db.backref, db.column_property
#from database import db.Model
from datetime import datetime,timedelta
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(80))
    twit_id =  db.Column(db.String)
    twit_token =  db.Column(db.String)
    fb_id =  db.Column(db.String)
    fb_token =  db.Column(db.String)
    projects = db.relationship('Projects')
    comments = db.relationship('Comments')
    participant = db.relationship('Participants')
    #participant = db.relationship("Participants", uselist=False, db.backref="users")

    def __init__(self, name=None, email=None, password=None, image = None, twit_id = None, twit_token = None, fb_id = None, fb_token = None):
        self.name = name
        self.email = email
        self.password = password
        self.image = image
        self.twit_id = twit_id
        self.twit_token = twit_token
        self.fb_id = fb_id
        self.fb_token = fb_token

    def __repr__(self):
        return "%s" % self.name

    def _get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def authentificate(self,name,passw):
        if (self.name == name and self.password == passw):
            return self

association_table = db.Table('association', db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    cat = db.relationship('Category', secondary=association_table, backref = db.backref('projects'))
    types=db.Column(db.Text)
    title = db.Column(db.String(50))
    description = db.Column(db.String(120))
    html = db.Column(db.Text)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)
    date_target = db.Column(db.DateTime,  default=datetime.utcnow)
    location = db.Column(db.String)
    lat = db.Column(db.Float, default=0)
    lng = db.Column(db.Float, default=0)
    inns_now = db.Column(db.Integer, default=0)
    inns_target = db.Column(db.Integer, default=1, nullable=False)
    image_link =  db.Column(db.String(220))
    video_link =  db.Column(db.String(220))
    comments = db.relationship('Comments')
    participants = db.relationship('Participants')

    def __init__(self, title=None, desc=None, dt=None, ge=None, html=None, user=None, loc=None, types='me', lat=0, lng=0, image=None):
        self.title = title
        self.description = desc
        self.date_target = dt
        self.inns_target = ge
        self.html=html
        self.user=user
        self.location=loc
        self.types = types
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
                    types=self.types,
                    lat=self.lat,
                    lng=self.lng,
                    image=self.image_link)
    def get_users(self):
        lst=[]
        for usr in self.participants:
            lst.append(usr.user)
        return lst

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column (db.String(220))
    date_created =  db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer,
                db.ForeignKey('users.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer,
                db.ForeignKey('projects.id', ondelete='CASCADE'))
    user = db.relationship('User')
    project = db.relationship('Projects')

    def __init__(self, content=None, user=None, project=None):
        self.content = content
        self.user = user
        self.project=project

class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column (db.String)
    kind = db.Column (db.String)
    date_created =  db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer,
                db.ForeignKey('users.id', ondelete='CASCADE'))
    reciver_id = db.Column(db.Integer,
                db.ForeignKey('users.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer,
                db.ForeignKey('projects.id', ondelete='CASCADE'))
    project = db.relationship('Projects')
    author = db.relationship("User",
                    primaryjoin="User.id==Messages.author_id",
                    backref="sent_messages")
    reciever = db.relationship("User",
                    primaryjoin="User.id==Messages.reciver_id",
                    backref="my_messages")

class Participants(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer,primary_key = True)
    project_id = db.Column(db.Integer,
                db.ForeignKey('projects.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer,
         db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User')
    #child = db.relationship("Child", uselist=False, db.backref="parent")
    #project = db.relationship('Projects', secondary=association_table)
    project = db.relationship('Projects')
    #project = db.relationship(Projects, secondary=association_table)

    def __init__ (self, user=None, proj=None):
        self.user=user
        self.project=proj

    def __str__(self):
         return self.user.name


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(120))
    num_projects = db.Column(db.Integer, default = 0)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "%s" % self.title

    def __str__(self):
        return self.title

    def num_proj(self):
        return self.session.query.projects.count()


