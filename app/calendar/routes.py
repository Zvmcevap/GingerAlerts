from flask import Blueprint, render_template
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

    return render_template('calendar.html', appointment_list=appointments)
