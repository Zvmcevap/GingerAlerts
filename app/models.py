from app import db
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    email = db.Column(db.String(100), unique=True)
    send_SMS = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    sms_template_id = db.Column(db.ForeignKey('smstemplates.id'), nullable=False, default=1)

    clients = db.relationship('Client', back_populates='user')
    sms_template = db.relationship('SmsTemplate', back_populates='users')

    def __repr__(self):
        return f'User: id:{self.id} name:{self.name} email:{self.email} registered{self.created_at} sending{self.send_SMS} '


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    now_sms = db.Column(db.Boolean, default=False)
    same_day_sms = db.Column(db.Boolean, default=False)
    day_before_sms = db.Column(db.Boolean, default=False)
    sms_template_id = db.Column(db.ForeignKey('smstemplates.id'), nullable=True)

    user = db.relationship('User', back_populates='clients')
    appointments = db.relationship('Appointment', back_populates='client')
    sms_template = db.relationship('SmsTemplate', back_populates='clients')

    def __repr__(self):
        return f'Stranka: ime:{self.name} telefonska:{self.phone}'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    time_of_appointment = db.Column(db.DateTime, nullable=False, default=datetime.now(), index=True)

    now_sms = db.Column(db.Integer, default=0)
    same_day_sms = db.Column(db.Integer, default=0)
    day_before_sms = db.Column(db.Integer, default=0)

    client = db.relationship('Client', back_populates='appointments')

    sent_texts = db.relationship('SentSms', back_populates='appointment')

    def __repr__(self):
        return f'Termin: stranka:{self.client.name} čas:{self.time_of_appointment}'


class SentSms(db.Model):
    __tablename__ = 'sentsmses'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    sms_type_id = db.Column(db.Integer, db.ForeignKey('smstypes.id'), nullable=False)
    sent_at_datetime = db.Column(db.DateTime, default=datetime.now(), index=True)
    sms_text = db.Column(db.Text, nullable=False)

    appointment = db.relationship('Appointment', back_populates='sent_texts')
    type = db.relationship('SmsType', back_populates='sent')

    def __repr__(self):
        return f'Poslan Sms: id:{self.id} id termina:{self.appointment_id}, Poslan ob: {self.sent_at_datetime}'


class SmsType(db.Model):
    __tablename__ = 'smstypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    sent = db.relationship('SentSms', back_populates='type')


class SmsTemplate(db.Model):
    __tablename__ = 'smstemplates'
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.Text, nullable=False)

    users = db.relationship('User', back_populates='sms_template')
    clients = db.relationship('Client', back_populates='sms_template')


class MyModelView(ModelView):
    def is_accessible(self):
        user = User.query.filter(User.id == current_user.id).first()
        if user.admin:
            return True
        else:
            return False
