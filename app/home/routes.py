from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Client, SmsTemplate, SentSms, Appointment
from app.forms import SmsTemplateForm
from app import db
from sqlalchemy import func


home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/home/static/'
                    )


@home_bp.route('/')
def index():
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.id).first()
    else:
        user = None

    return render_template('index.html', user=user)


@home_bp.route('/change_sms_template', defaults={'client_id': None}, methods=['GET'])
@home_bp.route('/change_sms_template/<client_id>', methods=['GET'])
@login_required
def change_sms_template(client_id):
    client = None
    sms_template_form = SmsTemplateForm()
    user = User.query.filter(User.id == current_user.id).first()
    sms_template = SmsTemplate.query.filter(user.sms_template_id == SmsTemplate.id).first()

    choices = db.session.query(
        Client.id,
        Client.name + " " + Client.phone).filter(
        Client.user == current_user
    ).order_by(func.lower(Client.name)).all()

    sms_template_form.client.choices = choices

    if client_id:
        client = Client.query.filter(Client.id == client_id).first()
        sms_template_form.client.data = [client.id]
        if client.sms_template:
            sms_template = SmsTemplate.query.join(Client).filter(SmsTemplate.id == client.sms_template_id).first()

    sms_template_form.template.data = sms_template.template

    return render_template('change_sms_template.html',
                           sms_template_form=sms_template_form,
                           client=client
                           )


@home_bp.route('/change_sms_template', defaults={'client_id': None}, methods=['POST'])
@home_bp.route('/change_sms_template/<client_id>', methods=['POST'])
@login_required
def change_sms_template_post(client_id):
    sms_template_form = SmsTemplateForm()
    template = sms_template_form.template.data
    client_ids = sms_template_form.client.data

    if client_ids:
        clients = db.session.query(Client).filter(Client.id.in_(client_ids)).all()
        new_template = SmsTemplate(
            template=template
        )
        db.session.add(new_template)
        for client in clients:
            client.sms_template = new_template
        db.session.commit()

        return redirect(url_for('clients_bp.clients'))

    user = User.query.filter(User.id == current_user.id).first()
    sms_template = SmsTemplate.query.filter(SmsTemplate.id == user.sms_template_id).first()
    sms_template.template = template
    db.session.commit()

    return redirect(url_for('home_bp.index'))


@home_bp.route('/reset_sms_template', defaults={'client_id': None}, methods=['GET'])
@home_bp.route('/reset_sms_template/<client_id>', methods=['GET'])
@login_required
def reset_sms_template(client_id):
    if client_id:
        client = Client.query.filter(Client.id == client_id).first()
        client.sms_template_id = None
        db.session.commit()
        return redirect(url_for('clients_bp.a_client', client_id=client_id))

    user = User.query.filter(User.id == current_user.id).first()
    user_template = SmsTemplate.query.filter(SmsTemplate.id == user.sms_template_id).first()
    factory_sms_template = db.session.query(SmsTemplate).filter(SmsTemplate.id == 1).first()
    template = factory_sms_template.template
    template = template.replace('{moje_ime}', str(user.name))

    user_template.template = template
    db.session.commit()

    return redirect(url_for('auth_bp.profile', sms_template=user_template))


@home_bp.route('/sent_sms/<sms_id>', methods=['GET'])
@login_required
def sent_sms(sms_id):
    sms = SentSms.query.filter(SentSms.id == sms_id).first()
    appointment = Appointment.query.filter(Appointment.id == sms.appointment_id).first()
    client = Client.query.filter(Client.id == appointment.client_id).first()

    return render_template('sent_text.html', appointment=appointment, sent_sms=sms, client=client)
