from flask import Blueprint


profile_bp = Blueprint('profile', __name__)

import hbapp.profile.views  # noqa
