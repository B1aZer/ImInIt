from wtforms import Form, BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class AddProjectForm(Form):
    title = TextField('Title', [validators.Length(min=1, max=25)])
    description = TextField('Description', [validators.Length(min=6, max=35)])
    user = TextField('Owner')
    image_link = TextField('Image Link')
