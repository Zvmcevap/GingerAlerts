from flask import Blueprint, render_template
from flask_login import login_required, current_user

appointments_bp = Blueprint('appointments', __name__,
                        template_folder='templates',
                        static_folder='static'
                        )


@appointments_bp.route('/appointments')
@login_required
def clients():
    return render_template('appointments.html')
