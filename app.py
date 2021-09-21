from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from twilio.rest import Client

#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gingeralert.db'
db = SQLAlchemy(app)


# Database creation
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    clients = db.relationship('Client', backref=db.backref('user'))


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(13))

    appointments = db.relationship('Appointment', backref='client')


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    time_of_appointment = db.Column(db.DateTime, nullable=False, default=datetime.now())


db.create_all()


# Database Functions
def new_user(name, password):
    nw_user = User.query.filter_by(name=name).first()
    if not nw_user:
        nw_user = User(name=name, password=password)
        db.session.add(nw_user)
        db.session.commit()
        return nw_user
    else:
        print('User Name Taken')


def new_client(name, phone, c_user):
    nw_client = Client(name=name, phone=phone, user=c_user)
    db.session.add(nw_client)
    db.session.commit()


def new_appointment(client_model, dateandtime):
    appointment = Appointment(client=client_model, time_of_appointment=dateandtime)
    db.session.add(appointment)
    db.session.commit()


def query_clients(current_user):
    q_clients = Client.query.filter_by(user=current_user).all()
    return q_clients


def query_todays_appointments(current_user):
    today = datetime.now().date()
    todays_appointments = Appointment.query\
        .filter((db.func.DATE(Appointment.time_of_appointment) == today) & (user == current_user))
    return todays_appointments


# User placdržač
user = new_user('Beno', 'prdeno')
if not user:
    user = User.query.filter_by(name='Beno').first()
    print(user.name)


todaysapps = query_todays_appointments(user)
for a in todaysapps:
    print(a.client.name, a.time_of_appointment)


# Flask Application
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
