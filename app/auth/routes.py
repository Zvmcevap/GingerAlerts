from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    name_email = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter((User.name == name_email) | (User.email == name_email)).first()

    if not user or not check_password_hash(user.password, password):
        flash(message='Invalid name or password!')
        return redirect(url_for('auth_bp.login'))

    login_user(user, remember=remember)
    return redirect(url_for('clients_bp.clients'))


@auth_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if len(name) < 3:
        flash(message='Name too short.')
        return redirect(url_for('auth_bp.signup'))

    if len(password) < 8:
        flash(message='Password too short')
        return redirect(url_for('auth_bp.signup'))

    user = User.query.filter((User.name == name) | (User.email == email)).first()

    if user:
        flash(message='Name or email already taken')
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
        return redirect(url_for('clients_bp.clients'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))
