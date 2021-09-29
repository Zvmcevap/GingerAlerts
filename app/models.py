from app import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    email = db.Column(db.String(100), unique=True)
    send_SMS = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    clients = db.relationship('Client', back_populates='user')

    def __repr__(self):
        return f'User: id:{self.id} name:{self.name} email:{self.email} registered{self.created_at} SMS-able{self.send_SMS} '


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    same_day_sms = db.Column(db.Boolean, default=False)
    day_before_sms = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='clients')
    appointments = db.relationship('Appointment', back_populates='client')

    def __repr__(self):
        return f'Stranka: ime:{self.name} telefonska:{self.phone}'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    time_of_appointment = db.Column(db.DateTime, nullable=False, default=datetime.now(), index=True)

    client = db.relationship('Client', back_populates='appointments')

    def __repr__(self):
        return f'Naročila: stranka:{self.client.name} čas:{self.time_of_appointment}'
