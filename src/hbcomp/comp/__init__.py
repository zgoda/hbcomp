from flask import Blueprint


comp_bp = Blueprint('comp', __name__)

import hbapp.comp.views  # noqa
