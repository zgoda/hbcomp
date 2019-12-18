from flask_babel import Babel
from flask_flatpages import FlatPages
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from .utils.sqla import Model

db = SQLAlchemy(model_class=Model)
login_manager = LoginManager()
babel = Babel()
csrf = CSRFProtect()
pages = FlatPages()
