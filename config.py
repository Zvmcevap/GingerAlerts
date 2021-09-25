import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-so-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'ginger-alerts.db')

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
