from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Client, Appointment, SentSms, UnsentSms
from app.forms import AddClientForm

clients_bp = Blueprint('clients_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/clients/static/'
                       )


@clients_bp.route('/clients')
@login_required
def clients():
    client_list = db.session.query(Client).filter(Client.user == current_user).order_by(Client.name).all()

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
    client_now_sms = client_form.now_sms.data
    client_same_day_sms = client_form.same_day_sms.data
    client_day_before_sms = client_form.day_before_sms.data

    if client_form.validate_on_submit():
        client = Client.query.filter((Client.name == client_name) | (Client.phone == client_phone)).first()
        if client:
            flash('Ime ali telefonska že v imeniku!')
            return redirect(url_for('clients_bp.add_client'))

        new_client = Client(
            name=client_name,
            phone="+386" + client_phone,
            now_sms=client_now_sms,
            same_day_sms=client_same_day_sms,
            day_before_sms=client_day_before_sms,
            user=current_user
        )
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('clients_bp.clients'))

    return render_template('add_client.html', client_form=client_form)


@clients_bp.route('/delete_client/<client_id>')
@login_required
def delete_client(client_id):
    Client.query.filter(Client.id == int(client_id)).delete()
    db.session.commit()
    return redirect(url_for('clients_bp.clients'))


@clients_bp.route('/update_client/<client_id>', methods=['GET'])
@login_required
def update_client(client_id):
    client = Client.query.filter(Client.id == int(client_id)).first()
    client_form = AddClientForm()

    client_form.name.data = client.name
    client_form.phone.data = client.phone[4:]
    client_form.now_sms.data = client.now_sms
    client_form.same_day_sms.data = client.same_day_sms
    client_form.day_before_sms.data = client.day_before_sms

    return render_template('add_client.html', client_form=client_form, client=client)


@clients_bp.route('/update_client/<client_id>', methods=['POST'])
@login_required
def update_client_post(client_id):
    client_form = AddClientForm()

    client_name = client_form.name.data
    client_phone = client_form.phone.data
    client_now_sms = client_form.now_sms.data
    client_same_day_sms = client_form.same_day_sms.data
    client_day_before_sms = client_form.day_before_sms.data

    if client_form.validate_on_submit():
        client = Client.query.filter((Client.name == client_name) | (Client.phone == client_phone)).first()

        if client and client.id != int(client_id):
            flash('Ime ali telefonska zasedena pri drugi stranki!')
            return redirect(url_for('clients_bp.update_client'))

        updated_client = Client.query.filter(Client.id == int(client_id)).first()

        updated_client.name = client_name
        updated_client.phone = "+386" + client_phone
        updated_client.now_sms = client_now_sms
        updated_client.same_day_sms = client_same_day_sms
        updated_client.day_before_sms = client_day_before_sms

        db.session.commit()

        return redirect(url_for('clients_bp.clients'))


@clients_bp.route('/a_client/<client_id>', methods=['GET'])
@login_required
def a_client(client_id):
    client = Client.query.filter(Client.id == client_id).first()
    appointment_list = Appointment.query.filter(Appointment.client == client).order_by(
        Appointment.time_of_appointment).all()

    sent_texts = db.session.query(SentSms).join(Appointment).filter(Appointment.client == client).all()

    return render_template('a_client.html', client=client, appointment_list=appointment_list, sent_texts=sent_texts)
