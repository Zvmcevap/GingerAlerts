from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from datetime import datetime
from app.forms import LoginForm, RegisterForm


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

        print(name_email, password)

        # When a valid form is submitted check the data against the database
        user = User.query.filter((User.name == name_email) | (User.email == name_email)).first()

        print(user)

        if not user:
            flash('Incorrect login information', 'invalid_login_details')
            return redirect(url_for('auth_bp.login', login_form=login_form))

        if check_password_hash(user.password, password):
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
    password = register_form.name.data
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
