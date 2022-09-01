from datetime import timedelta

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/estudiantes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True
    FLASK_DEBUG = 'development'
    SECRET_KEY = 'sdfksdj156165gnsdfnsdonfs'
    TEMPLATES_FOLDER = 'templates'
    PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

    