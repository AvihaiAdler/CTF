from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login')


class SearchBar(FlaskForm):
    search_string = StringField('Search_String', description='Song name')
    submit = SubmitField('Search')

