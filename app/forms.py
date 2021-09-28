from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, Regexp
from wtforms.fields.html5 import TelField


# Python Classes to create html forms with Flask-WTF
class RegisterForm(FlaskForm):
    name = StringField('Ime', validators=[InputRequired(message='Potreben vnos.'),
                                          Length(3, 20, message='Med 3 in 20.')
                                          ])
    email = StringField('Email', validators=[InputRequired(message='Potreben vnos.'),
                                             Email(message='Vsaj podobno emailu.')
                                             ])
    password = PasswordField('Geslo', validators=[InputRequired(),
                                                  Length(6, 50, message='Med 6 in 50 znakov.')

                                                  ])
    remember = BooleanField('Zapomni se me', default=False)
    recaptcha = RecaptchaField()

    submit = SubmitField('Vpis')


class LoginForm(FlaskForm):
    name_email = StringField('Ime ali Email', validators=[
        InputRequired(message='Potreben vnos.'),
        Length(3, 50, message='Med 3 in 50 črk.')
    ])
    password = PasswordField('Geslo', validators=[InputRequired(message='Potreben vnos.'),
                                                  Length(6, 50, message='Med 6 in 50 znakov.')])
    remember = BooleanField('Zapomni se me', default=False)

    submit = SubmitField('Vpis')


class AddClientForm(FlaskForm):
    name = StringField('Ime stranke', validators=[InputRequired(), Length(3, 50, message='Med 3 in 50 črk.')])
    phone = TelField('Telefonska številka',
                     validators=[InputRequired(message='Potreben vnos.'),
                                 Length(8, 8, message='Točno 8 mest mora biti dolga telefonska številka. A la "41333222".'),
                                 Regexp(message='Telefonska številka je.. ŠTEVILKA..', regex='^[0-9]*$')
                                 ]
                     )
    same_day_sms = BooleanField('SMS obvestilo isti dan', default=False)
    day_before_sms = BooleanField('SMS obvestilo dan prej', default=False)

    submit = SubmitField('Shrani')
