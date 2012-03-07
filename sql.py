# __main__.py
import os
import sqlalchemy as sa
 
from models import *
 
os.environ['PYTHONINSPECT'] = 'True'
engine = sa.create_engine('sqlite:///sql.db', echo=True)
Base.metadata.create_all(engine)
Session = sa.orm.sessionmaker(bind=engine)
session = Session()

session.query(User).all()
jack = User('Jack','email@dsa.com','pass')
session.add(jack)
proj = Projects('title','data',jack,'image')
session.add(proj)
session.commit()
#session.query(User).all()
#session.query(Projects).all()
