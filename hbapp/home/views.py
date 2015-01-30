from flask import render_template

from ..home import home_bp
from ..ext import pages
from ..models import Competition


@home_bp.route('/')
def index():
    ctx = {
        'recent': Competition.recent(),
        'upcoming': Competition.upcoming(),
    }
    return render_template('index.html', **ctx)


@home_bp.route('/page/<path:path>')
def flatpage(path):
    page = pages.get_or_404(path)
    return render_template('flatpage.html', page=page)
