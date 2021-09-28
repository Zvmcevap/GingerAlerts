from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Client
from app.forms import AddClientForm

clients_bp = Blueprint('clients_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@clients_bp.route('/clients')
@login_required
def clients():
    client_list = Client.query.filter(Client.user == current_user).all()
    return render_template('clients.html', client_list=client_list)


@clients_bp.route('/add_client', methods=['GET'])
@login_required
def add_client():
    client_form = AddClientForm()
    return render_template('add_client.html', client_form=client_form)


@clients_bp.route('/add_client', methods=['POST'])
@login_required
def add_client_post():
    client_form = AddClientForm()

    client_name = client_form.name.data
    client_phone = client_form.phone.data
    client_same_day_sms = client_form.same_day_sms.data
    client_day_before_sms = client_form.day_before_sms.data


    if client_form.validate_on_submit():
        client = Client.query.filter((Client.name == client_name) | (Client.phone == client_phone)).first()
        if client:
            flash('Ime ali telefonska že v imeniku!')
            return redirect(url_for('clients_bp.add_client'))

        new_client = Client(
            name=client_name,
            phone=client_phone,
            same_day_sms=client_same_day_sms,
            day_before_sms=client_day_before_sms,
            user=current_user
        )
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('clients_bp.clients'))

    return render_template('add_client.html', client_form=client_form)
