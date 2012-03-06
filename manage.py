# all the imports
#import sqlite3
#import conf
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from sqlalchemy import desc
from database import db_session
from models import User, Projects
from forms import RegistrationForm,AddProjectForm
#from contextlib import closing


# create our little application :)
app = Flask(__name__)
app.config.from_object('conf')

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def show_entries():
    #query=[Projects.query.all()]
    query=db_session.query(Projects).order_by(desc('date_created')).all()
    return render_template('content.html',content=query)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        db_session.commit()

        flash('Thanks for registering')
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/add', methods=['POST','GET'])
def add_entry():
    """
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    """
    form = AddProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        proj = Projects(form.title.data, form.description.data,None,
                        form.image_link.data)
        db_session.add(proj)
        db_session.commit()
        flash('Project added')
        return redirect('/')

    return render_template('add.html', form=form)


'''
def connect_db():
     return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

'''

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
'''

if __name__ == '__main__':
    app.run()


