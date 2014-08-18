from flask import render_template

from hbapp import pages
from hbapp.home import home_bp


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/page/<path:path>')
def flatpage(path):
    page = pages.get_or_404(path)
    return render_template('flatpage.html', page=page)
