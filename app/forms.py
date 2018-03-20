from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import current_app as app
import requests


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

    def validate_form(self):

        validate_url = app.config['API_URL'] + '/login'

        params = {
            'email': self.email,
            'password': self.password
        }

        r = requests.post(validate_url, params)

        return r.json()



class RegistrationForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_form(self):

        validate_url = app.config['API_URL'] + '/registration'

        params = {
            'email': self.email,
            'password': self.password
        }

        r = requests.post(validate_url, params)

        return r.json()