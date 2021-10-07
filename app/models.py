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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    now_sms = db.Column(db.Boolean, default=False)
    same_day_sms = db.Column(db.Boolean, default=False)
    day_before_sms = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='clients', passive_deletes=True)
    appointments = db.relationship('Appointment', back_populates='client', passive_deletes=True)

    def __repr__(self):
        return f'Stranka: ime:{self.name} telefonska:{self.phone}'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    time_of_appointment = db.Column(db.DateTime, nullable=False, default=datetime.now(), index=True)

    now_sms = db.Column(db.Boolean, default=False)
    same_day_sms = db.Column(db.Boolean, default=False)
    day_before_sms = db.Column(db.Boolean, default=False)

    client = db.relationship('Client', back_populates='appointments', passive_deletes=True)

    unsent_texts = db.relationship('UnsentSms', back_populates='appointment', passive_deletes=True)
    sent_texts = db.relationship('SentSms', back_populates='appointment')

    def __repr__(self):
        return f'Termin: stranka:{self.client.name} čas:{self.time_of_appointment}'


class UnsentSms(db.Model):
    __tablename__ = 'unsentsmses'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False)
    sms_type_id = db.Column(db.Integer, db.ForeignKey('smstypes.id'), nullable=False)

    appointment = db.relationship('Appointment', back_populates='unsent_texts', passive_deletes=True)
    type = db.relationship('SmsType', back_populates='unsent')

    def __repr__(self):
        return f'Neposlan Sms: id:{self.id}  id_termina:{self.appointment_id}'


class SentSms(db.Model):
    __tablename__ = 'sentsmses'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    sms_type_id = db.Column(db.Integer, db.ForeignKey('smstypes.id'), nullable=False)
    sent_at_datetime = db.Column(db.DateTime, default=datetime.now(), index=True)

    appointment = db.relationship('Appointment', back_populates='sent_texts')
    type = db.relationship('SmsType', back_populates='sent')

    def __repr__(self):
        return f'Poslan Sms: id:{self.id} id termina:{self.appointment_id}, Poslan ob: {self.sent_at_datetime}'


class SmsType(db.Model):
    __tablename__ = 'smstypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    unsent = db.relationship('UnsentSms', back_populates='type')
    sent = db.relationship('SentSms', back_populates='type')
