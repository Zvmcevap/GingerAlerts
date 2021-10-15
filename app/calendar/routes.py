from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Client, Appointment

calendar_bp = Blueprint('calendar_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/calendar/static'
                        )


@calendar_bp.route('/calendar')
@login_required
def calendar():
    appointments = db.session.query(Appointment).join(Client).filter(Client.user == current_user).all()
    calendar_appointments = []
    for app in appointments:
        app_dict = {
            'start': app.time_of_appointment.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': app.time_of_appointment.strftime('%Y-%m-%dT%H:%M:%S'),
            'name': app.client.name,
            'url': url_for('appointments_bp.an_appointment', appointment_id=app.id)
        }
        calendar_appointments.append(app_dict)

    return render_template('calendar.html', appointment_list=appointments,
                           calendar_appointments=calendar_appointments)
