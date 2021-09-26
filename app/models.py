from app import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    email = db.Column(db.String(100), unique=True)
    send_SMS = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'User: id:{self.id} name:{self.name} email:{self.email} registered{self.created_at} SMS-able{self.send_SMS} '


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    receive_today_SMS = db.Column(db.Boolean, default=False)
    receive_tomorrow_SMS = db.Column(db.Boolean, default=False)

    appointments = db.relationship('Appointment', backref='client')

    def __repr__(self):
        return f'Stranka: ime:{self.name} telefonska:{self.phone}'


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    time_of_appointment = db.Column(db.DateTime, nullable=False, default=datetime.now(), index=True)

    def __repr__(self):
        return f'Naročila: stranka:{self.client.name} čas:{self.time_of_appointment}'
