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

@app.before_request
def before_request():
    g.user = None
    if 'auth' in session:
        g.user = db_session.query(User).filter(User.name==session['auth']).first()
    

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def show_entries():
    query=db_session.query(Projects).order_by(desc('date_created')).all()
    #query=abort(404)
    app.logger.debug(query)
    return render_template('content.html',content=query)

@app.route('/projects/<int:proj_id>')
def project_index(proj_id):
    return render_template('project.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #check email,login
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
        #try:
            proj = Projects(form.title.data, form.description.data,g.user,
                        form.image_link.data)
            app.logger.debug(str(proj.__dict__))
            db_session.add(proj)
            db_session.commit()
            flash('Project added')
        #except:
            #app.logger.debug('Cant add project')
            return redirect('/')

    return render_template('add.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    #Make seperate gef - log the user in for register cookie
    error = None
    if request.method == 'POST':
        user = db_session.query(User).filter(User.name == request.form['username']).first()
        if user:
            app.logger.debug(user.get_name())
            if request.form['username'] != user.get_name():
                error = 'Invalid username'
            elif request.form['password'] != user._get_password():
                error = 'Invalid password'
            else:
                session['auth'] = user.get_name()
                flash('You were logged in')
                g.user=user
                app.logger.debug(g.user)
                return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('auth', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.debug = True
    app.run()


