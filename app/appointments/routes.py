from flask import Blueprint, render_template, json
from flask_login import login_required, current_user
from app import db
from app.forms import AddAppointmentForm
from app.models import Appointment, Client

appointments_bp = Blueprint('appointments_bp', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/appointments/static/'
                            )


@appointments_bp.route('/appointments')
@login_required
def appointments():

    appointment_list = db.session.query(Appointment).filter(Client.user == current_user).all()
    print(appointment_list)

    return render_template('appointments.html', appointment_list=appointment_list)


@appointments_bp.route('/add_appointment', methods=['GET'])
@login_required
def add_appointment():
    client = Client.query.filter(Client.user == current_user).first()
    client_names = []
    clients = Client.query.filter(Client.user == current_user).all()
    for c in clients:
        client_names.append(c.name)
    print(client_names)

    appointment_form = AddAppointmentForm()
    return render_template('add_appointments.html',
                           appointment_form=appointment_form,
                           client=client,
                           client_names=json.dumps(client_names)
                           )


@appointments_bp.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment_post():
    client = Client.query.first()
    appointment_form = AddAppointmentForm()
    client_name = appointment_form.client_name.data
    app_date = appointment_form.date_of_appointment.data
    app_time = appointment_form.time_of_appointment.data

    print(app_date, app_time, client_name, client.name)

    return render_template('add_appointments.html', appointment_form=appointment_form, client=client)
