from . import db
from models import User, Client, Appointment
from datetime import datetime


def new_client(name, phone, c_user):
    nw_client = Client(name=name, phone=phone, user=c_user)
    db.session.add(nw_client)
    db.session.commit()


def delete_from_database(id):
    db.session.remove(id)
    db.session.commit()


def new_appointment(client_model, date_and_time):
    appointment = Appointment(client=client_model, time_of_appointment=date_and_time)
    db.session.add(appointment)
    db.session.commit()


def query_clients(current_user):
    q_clients = Client.query.filter_by(user=current_user).all()
    return q_clients


def query_todays_appointments(current_user):
    today = datetime.now().date()
    todays_appointments = Appointment.query\
        .filter((db.func.DATE(Appointment.time_of_appointment) == today) & (Appointment.client.user == current_user))
    return todays_appointments
