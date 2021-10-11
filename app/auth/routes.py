from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Client, Appointment, SmsTemplate, SentSms
from datetime import datetime
from app.forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeNameEmailForm

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@auth_bp.route('/login', methods=['GET'])
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form=login_form)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    login_form = LoginForm()
    if login_form.validate_on_submit():

        name_email = login_form.name_email.data
        password = login_form.password.data
        remember = login_form.remember.data

        # When a valid form is submitted check the data against the database
        user = User.query.filter((User.name == name_email) | (User.email == name_email)).first()

        if not user:
            flash('Incorrect login information', 'invalid_login_details')
            return redirect(url_for('auth_bp.login', login_form=login_form))

        if not check_password_hash(user.password, password):
            flash('Incorrect login information', 'invalid_login_details')
            return redirect(url_for('auth_bp.login', login_form=login_form))

        # If all succeeds login le user
        login_user(user, remember=remember)
        return redirect(url_for('home_bp.index'))

    # If there is invalid input in the form itself
    return render_template('login.html', login_form=login_form)


@auth_bp.route('/signup', methods=['GET'])
def signup():
    register_form = RegisterForm()
    return render_template('signup.html', register_form=register_form)


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    register_form = RegisterForm()

    email = register_form.email.data
    name = register_form.name.data
    password = register_form.password.data
    remember = register_form.remember.data

    if register_form.validate_on_submit():

        user = User.query.filter((User.name == name) | (User.email == email)).first()
        if user:
            flash('Name or email already taken', 'name_not_unique')
            return redirect(url_for('auth_bp.signup'))

        else:
            time_of_creation = datetime.now()
            new_user = User(
                email=email,
                name=name,
                created_at=time_of_creation,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)

            # Make custom SMS template
            sms_template = db.session.query(SmsTemplate).filter(SmsTemplate.id == 1).first()
            template = sms_template.template
            template = template.replace('{moje_ime}', str(new_user.name))
            new_sms_template = SmsTemplate(
                template=template
            )
            db.session.add(new_sms_template)
            new_user.sms_template = new_sms_template

            db.session.commit()

            login_user(new_user, remember=remember)
            return redirect(url_for('home_bp.index'))

    # If there is invalid input from user render this
    return render_template('signup.html', register_form=register_form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.id == current_user.id).first()
    sms_template = SmsTemplate.query.filter(SmsTemplate.id == user.sms_template_id).first()
    sent_texts = SentSms.query.join(Appointment).join(Client).filter(Client.user_id == user.id).all()

    return render_template('profile.html', sms_template=sms_template, sent_texts=sent_texts)


@auth_bp.route('/delete_profile')
@login_required
def delete_profile():
    appointments = db.session.query(Appointment).join(Client).filter(Client.user_id == current_user.id).all()
    clients = Client.query.filter(Client.user_id == current_user.id).all()

    for appointment in appointments:
        db.session.delete(appointment)
    for client in clients:
        db.session.delete(client)
    User.query.filter(User.id == current_user.id).delete()
    db.session.commit()
    logout_user()
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/update_profile', methods=['GET'])
@login_required
def update_profile():
    register_form = RegisterForm()
    register_form.name.data = current_user.name
    register_form.email.data = current_user.email

    return render_template('signup.html', register_form=register_form, update=True)


@auth_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile_post():
    register_form = ChangeNameEmailForm()

    email = register_form.email.data
    name = register_form.name.data

    user = User.query.filter(((User.name == name) & (User.name != current_user.name)) | (
            (User.email == email) & (User.email != current_user.email))).first()
    if user:
        flash('Name or email already taken', 'name_not_unique')
        return redirect(url_for('auth_bp.update_profile'))
    if register_form.validate_on_submit():
        user = User.query.filter(User.id == current_user.id).first()
        if name:
            user.name = name
        if email:
            user.email = email

        db.session.commit()
        login_user(user)

        return redirect(url_for('auth_bp.profile'))

    flash('WHATDAFAK')
    return render_template('signup.html', register_form=register_form, update=True)


@auth_bp.route('/approve_sms/<user_id>', methods=['GET'])
@login_required
def approve_sms(user_id):
    if current_user.id == 1:
        user = User.query.filter(User.id == user_id).first()
        user.send_SMS = True
        db.session.commit()

        return redirect(url_for('home_bp.index'))
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/disapprove_sms/<user_id>', methods=['GET'])
@login_required
def disapprove_sms(user_id):
    if current_user.id == 1:
        user = User.query.filter(User.id == user_id).first()
        user.send_SMS = False
        db.session.commit()

        return redirect(url_for('home_bp.index'))
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/change_password', methods=['GET'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()

    return render_template('change_password.html', change_password_form=change_password_form)


@auth_bp.route('/change_password', methods=['POST'])
@login_required
def change_password_post():
    change_password_form = ChangePasswordForm()
    user = User.query.filter(User.id == current_user.id).first()

    old_password = change_password_form.old_password.data
    new_password = change_password_form.new_password.data

    if change_password_form.validate_on_submit():
        if not check_password_hash(user.password, old_password):
            flash('Staro geslo je bilo napačno', 'invalid_login_details')
            return redirect(url_for('auth_bp.change_password', change_password_form=change_password_form))

        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        login_user(user)

        return redirect(url_for('auth_bp.profile'))

    return render_template('change_password.html', change_password_form=change_password_form)
