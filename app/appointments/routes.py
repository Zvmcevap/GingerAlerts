from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from sqlalchemy import func
from app.forms import AddAppointmentForm
from app.models import Appointment, Client, UnsentSms, SentSms
from datetime import datetime
import calendar

appointments_bp = Blueprint('appointments_bp', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/appointments/static/'
                            )


@appointments_bp.route('/appointments')
@login_required
def appointments():
    print(datetime.today())
    appointment_list = db.session.query(Appointment).join(Client).filter(
        (Client.user == current_user) & (func.date(Appointment.time_of_appointment) >= datetime.now().date())
    ).order_by(
        Appointment.time_of_appointment).all()

    # Sorting appointment dates into groups of years, months and days

    appointment_years = set()
    appointment_months = set()
    appointment_days = set()
    schedule = {}

    for appointment in appointment_list:
        appointment_years.add(appointment.time_of_appointment.year)
        appointment_days.add(appointment.time_of_appointment.day)
        appointment_months.add(appointment.time_of_appointment.month)

    # Yo dawg, heard you like for loops... will hopefully find some other way to do this... eventually
    for year in sorted(appointment_years):
        m = {}
        for month in sorted(appointment_months):
            d = set()
            for day in sorted(appointment_days):
                for appointment in appointment_list:
                    if appointment.time_of_appointment.year == year and appointment.time_of_appointment.month == month \
                            and appointment.time_of_appointment.day == day:
                        if year not in schedule.keys() or month not in m.keys() or day not in d:
                            d.add(day)
                            m[calendar.month_name[month]] = sorted(d)
                            schedule[year] = m

    return render_template('timeline.html',
                           appointment_list=appointment_list,
                           schedule=schedule
                           )


@appointments_bp.route('/add_appointment', defaults={'client_id': None}, methods=['GET'])
@appointments_bp.route('/add_appointment/<client_id>', methods=['GET'])
@login_required
def add_appointment(client_id):
    # Make the appointment form and add choices
    appointment_form = AddAppointmentForm()
    appointment_form.client_name.choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    # If a client is passed in add it as the default option
    if client_id:
        client = Client.query.filter(Client.id == client_id).first()
        appointment_form.client_name.data = [client.id]
        appointment_form.now_sms.data = client.now_sms
        appointment_form.same_day_sms.data = client.same_day_sms
        appointment_form.day_before_sms.data = client.day_before_sms

    return render_template('add_appointments.html',
                           appointment_form=appointment_form,
                           client=client_id
                           )


@appointments_bp.route('/add_appointment', defaults={'client_id': None}, methods=['POST'])
@appointments_bp.route('/add_appointment/<client_id>', methods=['POST'])
@login_required
def add_appointment_post(client_id):
    # Make the appointment form and create client list of choices
    appointment_form = AddAppointmentForm()

    appointment_form.client_name.choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    if client_id:
        appointment_form.client_name.data = [int(client_id)]

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
            new_now_sms = SentSms(appointment=new_appointment, sms_type_id=1)
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


@appointments_bp.route('/update_appointment/<appointment_id>', methods=['GET'])
@login_required
def update_appointment(appointment_id):
    # Make the appointment form and add choices
    appointment_form = AddAppointmentForm()
    appointment_form.client_name.choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    # Set forms values to the updating appointment
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    appointment_form.client_name.data = [appointment.client.id]
    appointment_form.time_of_appointment.data = appointment.time_of_appointment.time()
    appointment_form.date_of_appointment.data = appointment.time_of_appointment.date()
    appointment_form.now_sms.data = appointment.now_sms
    appointment_form.same_day_sms.data = appointment.same_day_sms
    appointment_form.day_before_sms.data = appointment.day_before_sms

    return render_template('add_appointments.html',
                           appointment_form=appointment_form,
                           appointment=appointment
                           )


@appointments_bp.route('/update_appointment/<appointment_id>', methods=['POST'])
@login_required
def update_appointment_post(appointment_id):
    updated_appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    # Make the appointment form and add choices
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

    # Validate the data, update appointment in db
    if appointment_form.validate_on_submit():
        client = Client.query.filter(Client.id == client_id).first()
        update_appointment.client = client
        updated_appointment.time_of_appointment = app_datetime
        updated_appointment.now_sms = now_sms
        updated_appointment.same_day_sms = same_day_sms
        updated_appointment.day_before_sms = yesterday_sms

        # check and update appointment in the unsent sms table
        unsent_now_sms = UnsentSms.query.filter(
            (UnsentSms.appointment_id == updated_appointment.id) & (UnsentSms.sms_type_id == 1)).first()
        unsent_same_day_sms = UnsentSms.query.filter(
            (UnsentSms.appointment_id == updated_appointment.id) & (UnsentSms.sms_type_id == 2)).first()
        unsent_day_before_sms = UnsentSms.query.filter(
            (UnsentSms.appointment_id == updated_appointment.id) & (UnsentSms.sms_type_id == 3)).first()

        if now_sms and not unsent_now_sms:
            new_now_sms = UnsentSms(appointment=updated_appointment, sms_type_id=1)
            db.session.add(new_now_sms)
        elif unsent_now_sms and not now_sms:
            db.session.delete(unsent_now_sms)

        if same_day_sms and not unsent_same_day_sms:
            new_same_day_sms = UnsentSms(appointment=updated_appointment, sms_type_id=2)
            db.session.add(new_same_day_sms)
        elif not same_day_sms and unsent_same_day_sms:
            db.session.delete(unsent_same_day_sms)

        if yesterday_sms and not unsent_same_day_sms:
            new_yesterday_sms = UnsentSms(appointment=updated_appointment, sms_type_id=3)
            db.session.add(new_yesterday_sms)
        elif not yesterday_sms and unsent_day_before_sms:
            db.session.delete(unsent_day_before_sms)
        db.session.commit()

        return redirect(url_for('appointments_bp.appointments'))

    flash(message='Spet neki narobe... Kajs nardila?????')
    return render_template('add_appointments.html', appointment_form=appointment_form, appointment=updated_appointment)


@appointments_bp.route('/an_appointment/<appointment_id>', methods=['GET'])
@login_required
def an_appointment(appointment_id):
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    unsent_sms = UnsentSms.query.filter(UnsentSms.appointment_id == appointment.id).all()
    sent_sms = SentSms.query.filter(SentSms.appointment_id == appointment.id).all()
    return render_template('an_appointment.html', appointment=appointment, sent_sms=sent_sms, unsent_sms=unsent_sms)


@appointments_bp.route('/delete_appointment/<appointment_id>', methods=['GET'])
@login_required
def delete_appointment(appointment_id):
    db.session.query(Appointment).filter(Appointment.id == appointment_id).delete()
    db.session.commit()

    return redirect(url_for('appointments_bp.appointments'))
