from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random


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


def query_todays_appointments():
    today = datetime.now().date()
    todays_apps = Appointment.query.filter(db.func.DATE(Appointment.time_of_appointment) == today)
    return todays_apps


# Client list for testing
client_list = {
    'Beno Zupanc': '041932204',
    'Nika Lemut': '0038631759981',
    'Matic Kavas Kavko': '+38640756449'
}

todays_apps = query_todays_appointments()

for a in todays_apps:
    print(a.client.name, a.time_of_appointment)

# User shenanigans for testing
user = new_user('Beno', 'prdeno')
if not user:
    user = User.query.filter_by(name='Beno').first()
    print(user.name)


# Add the list for testing
"""
for client in client_list:
    new_client(client, client_list[client], user)
"""

# Query client list for testing
clients = query_clients(user)
for c in clients:
    print(c.id, c.name, c.phone, c.user.name)

"""
# Make random appointments for testing
now = datetime.now()
for c in clients:
    app_time = now + timedelta(days=random.randint(0, 10))
    new_appointment(c, app_time)
"""



# Flask Application
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
