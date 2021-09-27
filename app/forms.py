from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length


# Python Classes to create html forms with Flask-WTF
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(3, 20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 20)])
    remember = BooleanField('Remember me', default=False)
    recaptcha = RecaptchaField()

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name_email = StringField('Name or Email', validators=[InputRequired(), Length(3, 20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 20)])
    remember = BooleanField('Remember me', default=False)

    submit = SubmitField('Submit')
