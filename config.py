import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Potejto#"1323))(Poutatoučćč'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ginger-alerts.db'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
