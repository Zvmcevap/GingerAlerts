import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # set a secret key in environment or use the test one
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-so-secret-key'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Use Heroku postgres database or create an sqlite db on root folder at start
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'ginger-alerts.db')
