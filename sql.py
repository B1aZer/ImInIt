# -*- coding: utf-8 -*-
# __main__.py
import os
import sqlalchemy as sa
 
from models import *
 
os.environ['PYTHONINSPECT'] = 'True'
engine = sa.create_engine('sqlite:///sql.db',convert_unicode=True)
Base.metadata.create_all(engine)
Session = sa.orm.sessionmaker(bind=engine)
db_session = Session()

db_session.query(User).all()
jack = User('jonny','email@dsa.com','qwe123','http://inamge_here')
db_session.add(jack)
httext = " New Goal: $48,000"
mata = Category(title='mata')
proj1 = Projects('title','Testing mode is on',httext,jack,'pruevo','55.74845417947296','37.56036176835937','http://s3.amazonaws.com/ksr/projects/73316/photo-full.jpg')
proj2 = Projects('title2','Testing mode is on',httext,jack,'pruevo','55.74845417947296','37.56036176835937','http://s3.amazonaws.com/ksr/projects/73316/photo-full.jpg')
#proj.cat = mata
db_session.add(proj1)
db_session.add(proj2)
db_session.commit()
q1 = db_session.query(Category)
#session.query(User).all()
#session.query(Projects).all()
