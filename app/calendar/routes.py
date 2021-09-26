from flask import Blueprint, render_template
from flask_login import login_required, current_user

calendar_bp = Blueprint('calendar_bp', __name__,
                     template_folder='templates',
                     static_folder='static'
                     )


@calendar_bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')
