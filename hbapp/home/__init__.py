from flask import Blueprint


home_bp = Blueprint('home', __name__)

import hbapp.home.views  # noqa
