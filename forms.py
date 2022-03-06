from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, validators
from wtforms.validators import InputRequired

class RegisterUserForm(FlaskForm):
    '''Form to register a new User'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class UserForm(FlaskForm):

    '''Form to create a new user'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()]) 


