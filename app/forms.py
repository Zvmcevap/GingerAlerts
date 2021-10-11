from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextField, SelectField
from wtforms.validators import InputRequired, Email, Length, Regexp
from wtforms.fields.html5 import TelField, DateField, TimeField
from datetime import datetime
from wtforms.widgets import TextArea


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

    submit = SubmitField('Shrani')


class LoginForm(FlaskForm):
    name_email = StringField('Ime ali Email', validators=[
        InputRequired(message='Potreben vnos.'),
        Length(3, 50, message='Med 3 in 50 črk.')
    ])
    password = PasswordField('Geslo', validators=[InputRequired(message='Potreben vnos.'),
                                                  Length(6, 50, message='Med 6 in 50 znakov.')])
    remember = BooleanField('Zapomni se me', default=False)

    submit = SubmitField('Shrani')


class AddClientForm(FlaskForm):
    name = StringField('Ime stranke', validators=[InputRequired(), Length(3, 50, message='Med 3 in 50 črk.')])
    phone = TelField('Telefonska številka',
                     validators=[InputRequired(message='Potreben vnos.'),
                                 Length(8, 8,
                                        message='Točno 8 mest mora biti dolga telefonska številka. A la "41333222".'),
                                 Regexp(message='Telefonska številka je.. ŠTEVILKA..', regex='^[0-9]*$')
                                 ]
                     )
    now_sms = BooleanField('SMS obvestilo takoj ob naročilu termina', default=False)
    same_day_sms = BooleanField('SMS obvestilo isti dan', default=False)
    day_before_sms = BooleanField('SMS obvestilo dan prej', default=False)

    submit = SubmitField('Shrani')


class AddAppointmentForm(FlaskForm):
    client_name = SelectMultipleField('Stranka',
                                      id="select",
                                      choices=[],
                                      validators=[InputRequired()],
                                      coerce=int
                                      )
    date_of_appointment = DateField('Datum', format='%Y-%m-%d', default=datetime.today(), validators=[InputRequired()])
    time_of_appointment = TimeField('Čas', format='%H:%M', default=datetime.now().time(), validators=[InputRequired()])

    now_sms = BooleanField('SMS obvestilo takoj ob naročilu termina', default=False)
    same_day_sms = BooleanField('SMS obvestilo isti dan', default=False)
    day_before_sms = BooleanField('SMS obvestilo dan prej', default=False)

    submit = SubmitField('Shrani')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Staro Geslo', validators=[InputRequired(),
                                                            Length(6, 50, message='Med 6 in 50 znakov.')
                                                            ])
    new_password = PasswordField('Novo Geslo', validators=[InputRequired(),
                                                           Length(6, 50, message='Med 6 in 50 znakov.')
                                                           ])
    submit = SubmitField('Shrani')


class ChangeNameEmailForm(FlaskForm):
    name = StringField('Ime', validators=[InputRequired(message='Potreben vnos.'),
                                          Length(3, 20, message='Med 3 in 20.')
                                          ])
    email = StringField('Email', validators=[InputRequired(message='Potreben vnos.'),
                                             Email(message='Vsaj podobno emailu.')
                                             ])
    submit = SubmitField('Shrani')


class SmsTemplateForm(FlaskForm):
    client = SelectMultipleField('Za koga se uporabi ta SMS: ',
                                 id="select",
                                 choices=[],
                                 coerce=int
                                 )
    template = TextField('SMS besedilo',
                         widget=TextArea(),
                         validators=[InputRequired(message='Ne more biti prazen SMS, kako bi to zgledal?')])

    submit = SubmitField('Shrani')
