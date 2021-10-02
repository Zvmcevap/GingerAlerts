from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from sqlalchemy import func
from app.forms import AddAppointmentForm
from app.models import Appointment, Client, UnsentSms, SentSms
from datetime import datetime

appointments_bp = Blueprint('appointments_bp', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/appointments/static/'
                            )


@appointments_bp.route('/appointments')
@login_required
def appointments():
    appointment_list = db.session.query(Appointment).join(Client).filter(Client.user == current_user).order_by(
        Appointment.time_of_appointment).all()

    return render_template('appointments.html', appointment_list=appointment_list)


@appointments_bp.route('/add_appointment/<client>', defaults={'client': None}, methods=['GET'])
@login_required
def add_appointment(client):
    # Make the appointment form and add choices
    appointment_form = AddAppointmentForm()
    appointment_form.client_name.choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    # If a client is passed in add it as the default option
    if client:
        appointment_form.client_name.default = [client.id]

    return render_template('add_appointments.html',
                           appointment_form=appointment_form,
                           client=client
                           )


@appointments_bp.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment_post():
    # Make the appointment form and create client list of choices
    appointment_form = AddAppointmentForm()
    appointment_form.client_name.choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    # Get the form data
    client_id = appointment_form.client_name.data[0]

    app_date = appointment_form.date_of_appointment.data
    app_time = appointment_form.time_of_appointment.data

    now_sms = appointment_form.now_sms.data
    same_day_sms = appointment_form.same_day_sms.data
    yesterday_sms = appointment_form.day_before_sms.data

    app_datetime = datetime.combine(app_date, app_time)

    # Validate the data, add appointment to db
    if appointment_form.validate_on_submit():
        client = Client.query.filter(Client.id == client_id).first()
        new_appointment = Appointment(client=client,
                                      time_of_appointment=app_datetime,
                                      now_sms=now_sms,
                                      same_day_sms=same_day_sms,
                                      day_before_sms=yesterday_sms  # Yes, yes I know... naming things.....
                                      )
        db.session.add(new_appointment)

        # add appointment to the unsent sms table
        if now_sms:  # This one is placeholder until the sms implementation!!!!
            new_now_sms = UnsentSms(appointment=new_appointment, sms_type_id=1)
            db.session.add(new_now_sms)
        if same_day_sms:
            new_same_day_sms = UnsentSms(appointment=new_appointment, sms_type_id=2)
            db.session.add(new_same_day_sms)
        if yesterday_sms:
            new_yesterday_sms = UnsentSms(appointment=new_appointment, sms_type_id=3)
            db.session.add(new_yesterday_sms)
        db.session.commit()


        return redirect(url_for('appointments_bp.appointments'))

    flash(message='Neki narobe, nevek kaj točno.. probi magar šenkrat ane, al neki')
    return render_template('add_appointments.html', appointment_form=appointment_form)
