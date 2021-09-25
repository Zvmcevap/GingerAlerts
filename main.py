from flask import Blueprint, render_template
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def clients():
    return render_template('clients.html', name=current_user.name)


@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')


@main.route('/appointments')
@login_required
def appointments():
    return render_template('appointments.html')
