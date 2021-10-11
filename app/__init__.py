from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_twilio import Twilio
import config


db = SQLAlchemy()
migrate = Migrate()
twilio = Twilio()


def create_app():
    app = Flask(__name__, instance_relative_config=False, static_url_path='/app/static/')

    app.config.from_object(config.Config)

    with app.app_context():
        # Create database from models
        from .models import User, SmsType, SmsTemplate
        db.init_app(app)
        db.app = app
        migrate.init_app(app, db)
        twilio.init_app(app)
        twilio.app = app

        # set up LoginManager to manage ..erm.. logins
        login_manager = LoginManager()
        login_manager.login_view = 'auth_bp.login'  # Redirects to auth.login whenever someone isn't authenticated
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

        # Create database start Scheduler
        db.create_all()

        # Add the 3 types of SMS to the smstypes table
        if not SmsTemplate.query.all():
            default_template = SmsTemplate(
                template='Živijo {ime_stranke}! {čas_termina} bla bla bla, test test, Lep pozdrav {moje_ime}'
            )
            db.session.add(default_template)
            db.session.commit()

        if not User.query.all():
            time_of_creation = datetime.now()
            new_user = User(
                email='zupanc.beno@gmail.com',
                name='Beno',
                created_at=time_of_creation,
                password=generate_password_hash('Kajmak19', method='sha256'),
                admin=True,
                send_SMS=True
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
        if not SmsType.query.all():
            now_sms = SmsType(name='Takojšnje SMS obvestilo:')
            same_day_sms = SmsType(name='SMS obvestilo na isti dan:')
            yesterday_sms = SmsType(name='SMS obvestilo dan prej:')
            db.session.add(now_sms)
            db.session.add(same_day_sms)
            db.session.add(yesterday_sms)
            db.session.commit()

        return app
