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
    appointment_list = db.session.query(Appointment).join(Client).filter(Client.user == current_user).order_by(
        Appointment.time_of_appointment).all()
 
    # Sorting appointment dates into groups of years, months and days

    appointment_years = set()

    test_dict = {}
    for app in appointment_list:
        date = app.time_of_appointment
        year = date.year
        month = date.month
        day = date.day
        if year not in test_dict:
            test_dict[year] = []
        test_dict[year].append([month, day])


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
    print(schedule)
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
        appointment_form.client_name.data = [int(client_id)]

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
