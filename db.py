# -*- coding: utf-8 -*-
from application import app, create_db, drop_db

if __name__ == '__main__':
    drop_db()  
    create_db()
