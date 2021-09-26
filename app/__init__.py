from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False, static_url_path='/app/static/')

    app.config.from_object(config.Config)
    db.init_app(app)

    with app.app_context():
        # Create database from models
        from .models import User
        db.init_app(app)

        # set up LoginManager to manage ..erm.. logins
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'  # Redirects to auth.login whenever someone isn't authenticated
        login_manager.init_app(app)

        @login_manager.user_loader  # Associate the cookie with the User
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Import and register all the blueprints
        from app.auth.routes import auth_bp
        app.register_blueprint(auth_bp)

        from app.home.routes import home_bp
        app.register_blueprint(home_bp)

        from app.clients.routes import clients_bp
        app.register_blueprint(clients_bp)

        from app.calendar.routes import calendar_bp
        app.register_blueprint(calendar_bp)

        from app.appointments.routes import appointments_bp
        app.register_blueprint(appointments_bp)

        # Create database
        db.create_all()

        return app
