from flask import (
    flash, redirect, render_template, request, session, url_for,
)
from flask_babel import gettext as _
from flask_login import login_required, logout_user

from ..utils.http import next_redirect
from . import auth_bp


@auth_bp.route('/login')
def login():
    session['next'] = request.args.get('next')
    return render_template('auth/select.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('You have been logged out'), category='success')
    return redirect(next_redirect(url_for('home.index')))
