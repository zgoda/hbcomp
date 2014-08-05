from flask import render_template

from hbapp.home import home_bp


@home_bp.route('/')
def index():
    return render_template('index.html')
