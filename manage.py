# all the imports
#import sqlite3
#import conf
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from helpers import jsonify
from sqlalchemy import desc
from database import db_session
from models import User, Projects, Comments, Participants, Category
from forms import RegistrationForm,AddProjectForm,LoginForm,CommentForm

from flask.ext.gravatar import Gravatar
#from contextlib import closing



# create our little application :)
app = Flask(__name__)
app.config.from_object('conf')

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)

@app.before_request
def before_request():
    g.user=getattr(g,'user',None)
    if 'auth' in session:
        g.user = db_session.query(User).filter(User.name==session['auth']).first()
    

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    query=db_session.query(Projects).order_by(desc('date_created')).limit(14).offset(0)
    #query=abort(404)
    app.logger.debug(g.user)
    return render_template('index.html',content=query)

@app.route('/ajax/<int:proj_id>', methods=['POST','GET'])
@app.route('/ajax', methods=['POST','GET'])
def ajax(*args, **kwargs):
    #app. logger.debug('ajax:',someth)
    #if request.method == 'POST':
        #app.logger.debug(request.form.get('lat'))
        #app.logger.debug(request.form.get('lng'))
    if request.method == 'GET':
        query=db_session.query(Projects).order_by(desc('date_created'))
        #jsony(query)
        #qqq = query.all()
        projs=[]
        for qq in query.all():
            #for q in qq:
            projs.append(qq.json())
        if args:
            query=db_session.query(Projects).get(args[0])
            projs=query.json()
        return jsonify(result = projs)
    return jsonify(status='success') 

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/user')
def user():
     return render_template('user.html',user=g.user)

@app.route('/cat/<category>')
def cat():
    query=db_session.query(Projects).order_by(desc('date_created')).limit(14).offset(0)
    return render_template('index.html',content=query)

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
    cats = db_session.query(Category).all()
    if request.method == 'POST' and form.validate():
        #try:
            proj = Projects(form.title.data,
                    form.description.data,
                    form.httext.data,
                    g.user,
                    form.loc.data,
                    form.lat.data,
                    form.lng.data,
                    form.image_link.data)
            #app.logger.debug(str(proj.__dict__))
            for cat in form.cat.data.split(','):
                proj.cat.append(Category(title=cat))
            db_session.add(proj)
            db_session.commit()
            flash('Project added')
        #except:
            #app.logger.debug('Cant add project')
            return redirect('/')

    return render_template('add.html', form=form, cats=cats)



@app.route('/projects/<int:proj_id>', methods=['POST','GET'])
def project_index(proj_id):
    form = CommentForm(request.form)
    proj = db_session.query(Projects).filter_by(id=proj_id).first()
    css='icon-ok-sign'
    if g.user in proj.get_users():
        css='icon-remove-sign'
    if request.method == 'POST' and form.validate():
        comm = Comments(form.comment.data,
                g.user,
                proj)
        db_session.add(comm)
        db_session.commit()
        flash('Comment added')
        return redirect(url_for('project_index',proj_id=proj_id))
    if proj is None:
        abort(404)
    #app.logger.debug(proj.get_users())
    return render_template('project.html',
                        query=proj,
                        form=form,
                        css=css)

#!!login requied
@app.route('/projects/add/<int:proj_id>', methods=['POST','GET'])
def part_add(proj_id):
    if request.method == 'GET' and g.user:
        #app.logger.debug(proj.participants)
        data = request.form.get('data')
        proj = db_session.query(Projects).get(proj_id)
        if g.user not in proj.get_users():
            proj.inns_now +=1
            part = Participants(g.user,
                proj)
            db_session.add(part)
            db_session.commit()
            flash('You are going to go')
        else:
            proj.inns_now -=1
            part = db_session.query(Participants).filter_by(user=g.user).delete()
            db_session.commit()
            app.logger.debug(part)
            flash('You are not going')

    """
    comment = Comment.query.get_or_404(comment_id)
    comment.permissions.delete.test(403)

    db.session.delete(comment)
    db.session.commit()

    signals.comment_deleted.send(comment.post)

    return jsonify(success=True,
                   comment_id=comment_id)
                   """

    return redirect('/projects/%s' % proj_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #check email,login
        user = User(form.username.data, form.email.data,
                    form.password.data, form.image.data)
        db_session.add(user)
        db_session.commit()

        flash('Thanks for registering')
        session['auth']=form.username.data
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Mak e seperate gef - log the user in for register cookie
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = db_session.query(User).filter(User.name == form.username.data).first()
        if form.validate() and user:
            #app.logger.debug(user.get_name())
                if user.authentificate(form.username.data,form.password.data):
                    flash('You were logged in')
                    session['auth']=user.get_name()
                    #app.logger.debug(g.user)
                    return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('auth', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


