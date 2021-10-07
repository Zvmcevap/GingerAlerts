from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@home_bp.route('/')
def index():
    user = User.query.filter(User.id == current_user.id).first()
    users_list = User.query.all()

    return render_template('index.html', user=user, users_list=users_list)
