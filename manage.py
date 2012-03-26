# -*- coding: utf-8 -*-
import os
from application import app, create_db, drop_db

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    #create_db()
    #drop_db()


