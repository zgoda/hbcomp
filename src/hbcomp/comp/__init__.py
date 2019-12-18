from flask import Blueprint

comp_bp = Blueprint('comp', __name__)

from . import views  # noqa: F401
