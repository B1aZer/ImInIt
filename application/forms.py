from wtforms import Form, BooleanField, TextField, IntegerField, PasswordField, HiddenField, DateField, TextAreaField, SubmitField, validators
from flaskext.wtf import URL,Optional,required,NumberRange, Regexp
from flask import current_app

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.Required()])
    image = TextField('Image URL')

class AddProjectForm(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description', [validators.Length(min=15)])
    cat = TextField('Category')
    loc = TextField('Location')
    date_end=DateField('Ending Date')
    goal_end = IntegerField('Goal')
    image_link = TextField('Image Link', validators=[
                                        URL(),Optional()])
    video_link = TextField('Video Link', validators=[
                                        URL(),Optional()])
    httext = TextAreaField('html_text')
    lat= HiddenField(default=0, validators= [Regexp('\d')])
    lng= HiddenField(default=0, validators= [Regexp('\d')])
    mark_location = BooleanField('Choose location on map')

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')

class CommentForm(Form):

    comment = TextAreaField(validators=[
                            required("Comment is required")])
