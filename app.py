from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    nwuser = User.query.filter_by(name=name).first()
    if not nwuser:
        nwuser = User(name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return nwuser
    else:
        print('User Name Taken')


def new_client(name, phone, c_user):
    nw_client = Client(name=name, phone=phone, user=c_user)
    db.session.add(nw_client)
    db.session.commit()


# Start of app
client_list = {
    'Beno Zupanc': '041932204',
    'Nika Lemut': '0038631759981',
    'Matic Kavas Kavko': '+38640756449'
}
user = new_user('Beno', 'prdeno')
if not user:
    user = User.query.filter_by(name='Beno').first()
    print(user)


for client in client_list:
    new_client(client, client_list[client], user)


# Flask Application
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
