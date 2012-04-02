# -*- coding: utf-8 -*-
# all the imports
#import sqlite3
#import conf
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from helpers import jsonify
#from sqlalchemy import db.desc, func
from models import User, Projects, Comments, Participants, Category
from forms import RegistrationForm,AddProjectForm,LoginForm,CommentForm
from functools import wraps
import helpers

from flask.ext.gravatar import Gravatar
from flask.ext.oauth import OAuth
from flaskext.babel import Babel
from extensions import db


# create our little application :)
app = Flask(__name__)
app.config.from_pyfile('config.py')

oauth = OAuth()
babel = Babel(app)

db.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='160705233955349',
    consumer_secret='4f4fa3aedb2cba7a35267cba7bd3a883',
)
twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='h2H3rxB5DogKqj9XpJ7Q',
    consumer_secret='FjBx1RI0HsRTev3m8FKPigcejMszFlSoEWGmVz75U'
)


@app.template_filter()
def timesince(value):
    return helpers.timesince(value)

@app.template_filter()
def timebefore(value):
    return helpers.timebefore(value)

def create_db():
    with app.test_request_context():
        db.create_all()

def drop_db():
    with app.test_request_context():
        db.drop_all()

@app.before_request
def before_request():
    g.user=getattr(g,'user',None)
    if 'auth' in session:
        g.user = db.session.query(User).filter(User.name==session['auth']).first()

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/fb')
def fb_login():
    return facebook.authorize(callback=url_for('fb_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/tw')
def tw_login():
    return twitter.authorize(callback=url_for('tw_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/fb_authorized')
@facebook.authorized_handler
def fb_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(next_url)
    return str(resp)
    me = facebook.get('/me')
    user = User.query.filter_by(name=me.data['name']).first()
    if not user:
        user = User(me.data['name'],fb_id=me.data['id'],fb_token=(
        resp['access_token'],
        ''
        ))
        db.session.add(user)
        db.session.commit()
        session['auth'] = me.data['name']
        flash('Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next')))
        return redirect(next_url)
    session['auth'] = me.data['name']
    return redirect(next_url)

@app.route('/tw_authorized')
@twitter.authorized_handler
def tw_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    #user = User.query.filter_by(twitter_id=resp['user_id'].first())
    user = User.query.filter_by(name=resp['screen_name']).first()
    if not user:
        user = User(resp['screen_name'],twit_id=resp['user_id'],twit_token=(
        resp['oauth_token'],
        resp['oauth_token_secret']
        ))
        db.session.add(user)
        db.session.commit()
        session['auth']=resp['screen_name']
        flash('Signed in as %s' % resp['screen_name'])
        return redirect(next_url)
    #td I can login as twitter name!!
    session['auth']=resp['screen_name']
    flash('User exist: %s' % resp['screen_name'])
    return redirect(next_url)



@facebook.tokengetter
def get_facebook_oauth_token():
    #return session.get('facebook_token')
    return getattr(g.user,'facebook_token',None)

@twitter.tokengetter
def get_twitter_token():
    #return session.get('twitter_token')
    return getattr(g.user,'twit_token',None)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
def index():
    page = int(request.args.get('p') or 1)
    #query=db.session.query(Projects).order_by(db.desc('date_created')).limit(14).offset(0)
    query=Projects.query.order_by(db.desc('date_created')).paginate(page,14)
    #cats = db.session.query(Category.title, db.func.count(Category.projects)). \
            #join(Category.projects).group_by(Category.title)
            #order_by(db.desc(db.func.count(Category.projects)))
    cats = db.session.query(Category.title, db.func.count(Category.title)) \
            .join(Category.projects) \
            .group_by(Category.title) \
            .order_by(db.desc(db.func.count(Category.title))) \
            .limit(14).all()
    return render_template('index.html',content=query, cats = cats)

@app.route('/cat/<category>')
def cat(category):
    page = int(request.args.get('p') or 1)
    query=Projects.query. \
            filter(Projects.cat.any(Category.title == category)). \
            order_by(db.desc('date_created')).paginate(page,14)
    return render_template('index.html',content=query)

@app.route('/ajax/<int:proj_id>', methods=['POST','GET'])
@app.route('/ajax', methods=['POST','GET'])
def ajax(*args, **kwargs):
    #app. logger.debug('ajax:',someth)
    #if request.method == 'POST':
        #app.logger.debug(request.form.get('lat'))
        #app.logger.debug(request.form.get('lng'))
    if request.method == 'GET':
        query=db.session.query(Projects).order_by(db.desc('date_created'))
        #jsony(query)
        #qqq = query.all()
        projs=[]
        for qq in query.all():
            #for q in qq:
            projs.append(qq.json())
        if args:
            query=db.session.query(Projects).get(args[0])
            projs=query.json()
        return jsonify(result = projs)
    return jsonify(status='success')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/tmp')
def tmp():
    return render_template('base.html')

@app.route('/user')
def user():
     return render_template('user.html',user=g.user)



@app.route('/add', methods=['POST','GET'])
@login_required
def add_entry():

    form = AddProjectForm(request.form)
    cats = db.session.query(Category).all()
    cats = [cat.title for cat in cats]
    if request.method == 'POST' and form.validate():
        #try:
            proj = Projects(form.title.data,
                    form.description.data,
                    form.date_end.data,
                    form.goal_end.data,
                    form.httext.data,
                    g.user,
                    form.loc.data,
                    form.types.data,
                    form.lat.data,
                    form.lng.data,
                    form.image_link.data)
            #app.logger.debug(str(proj.__dict__))

            for cat in form.cat.data.split(','):
                if cat:
                    cat = cat.strip()
                    #category = db.session.query(Category).filter_by(title=cat).first()
                    #if not category:
                        #category = Category(title=cat)
                    category = db.session.query(Category).filter_by(title=cat).first() \
                        or Category(title=cat)
                    proj.cat.append(category)

            db.session.add(proj)
            db.session.commit()
            flash('Project added')
        #except:
            #app.logger.debug('Cant add project')
            return redirect('/')

    return render_template('add.html', form=form, cats=cats)



@app.route('/projects/<int:proj_id>', methods=['POST','GET'])
def project_index(proj_id):
    form = CommentForm(request.form)
    proj = db.session.query(Projects).filter_by(id=proj_id).first()
    css='icon-ok-sign'
    if g.user in proj.get_users():
        css='icon-remove-sign'
    if request.method == 'POST' and form.validate():
        comm = Comments(form.comment.data,
                g.user,
                proj)
        db.session.add(comm)
        db.session.commit()
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
        proj = db.session.query(Projects).get(proj_id)
        if g.user not in proj.get_users():
            proj.inns_now +=1
            part = Participants(g.user,
                proj)
            db.session.add(part)
            db.session.commit()
            flash('You are going to go')
        else:
            proj.inns_now -=1
            part = db.session.query(Participants).filter_by(user=g.user).delete()
            db.session.commit()
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
    reg_form = RegistrationForm(request.form)
    log_form = LoginForm(request.form)
    if request.method == 'POST' and reg_form.validate():
        #check email,login
        user = User(reg_form.username.data, reg_form.email.data,
                    reg_form.password.data, reg_form.image.data)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering')
        session['auth']=reg_form.username.data
        return redirect('/')
    return render_template('login.html',log_form=log_form, reg_form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.args.get('next'):
        session['next']=request.args.get('next')
    log_form = LoginForm(request.form)
    reg_form = RegistrationForm(request.form)
    if request.method == 'POST':
        user = db.session.query(User).filter(User.name == log_form.user.data).first()
        if log_form.validate() and user:
            #app.logger.debug(user.get_name())
                if user.authentificate(log_form.user.data,log_form.passw.data):
                    flash('You were logged in')
                    session['auth']=user.get_name()
                    return redirect(session.pop('next',None) or url_for('index'))
                else:
                    flash('Creditnails not correct')
        if not user:
            flash('Sorry! No such user')
    return render_template('login.html', log_form=log_form, reg_form=reg_form )

@app.route('/logout')
def logout():
    session.pop('auth', None)
    flash('You were logged out')
    return redirect(url_for('index'))
