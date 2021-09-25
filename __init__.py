from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'SecretKeyPlaceholder'  # Change this
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gingeralerts.db'

    db.init_app(app)
    from .models import User, Client, Appointment  # Statement IS used, it's where the db gets its tables

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirects to auth.login whenever someone isn't authenticated
    login_manager.init_app(app)

    @login_manager.user_loader  # Associate the cookie with the User
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


db.create_all(app=create_app())
