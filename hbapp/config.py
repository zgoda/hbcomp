DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'

try:
    from config_local import *  # NOQA
except ImportError:
    pass
