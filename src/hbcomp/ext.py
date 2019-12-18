from flask_babel import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_bootstrap import Bootstrap
from flask_flatpages import FlatPages
from flask_oauthlib.client import OAuth

db = SQLAlchemy()

login_manager = LoginManager()

oauth = OAuth()

pages = FlatPages()

babel = Babel()

bootstrap = Bootstrap()
