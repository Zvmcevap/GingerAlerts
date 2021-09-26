from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/appointments')
@login_required
def appointments():
    return render_template('appointments.html')
