from flask import Blueprint, render_template
from flask_login import login_required, current_user


clients_bp = Blueprint('clients_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@clients_bp.route('/clients')
@login_required
def clients():
    return render_template('clients.html')
