from flask import render_template, session, request, flash, redirect, url_for, current_app, abort
from flask_login import logout_user, login_required
from flask_babel import gettext as _

from ..auth import auth_bp
from ..auth.utils import login_success
from ..auth.service import services, google


@auth_bp.route('/select', endpoint='select')
def select_provider():
    session['next'] = request.args.get('next')
    return render_template('auth/select.html')


@auth_bp.route('/login/<provider>', endpoint='login')
def remote_login(provider):
    if provider == 'local':
        if not current_app.config['DEBUG']:
            abort(404)
        return local_login_callback(request.args.get('email', None))
    if provider not in services:
        flash(_('Service "%(provider)s" is not supported', provider=provider), category='error')
        return redirect(url_for('auth.select'))
    view_name = 'auth.callback-%s' % provider
    callback = url_for(view_name, _external=True)
    service = services[provider]
    return service.authorize(callback=callback)


@auth_bp.route('/callback/google', endpoint='callback-google')
@google.authorized_handler
def google_remote_login_callback(resp):  # pragma: no cover
    if resp is None:
        flash(_('Access denied, reason: %(reason)s error: %s(error)s', **request.args), category='error')
        redirect(url_for('home'))
    access_token = resp.get('access_token')
    if access_token:
        session['access_token'] = (access_token, '')
        me = google.get('userinfo')
        return login_success(me.data['email'], access_token, me.data['id'], 'google')
    return redirect(url_for('auth.select'))


def local_login_callback(resp):
    if resp is not None:
        email = resp
    else:
        email = 'user@example.com'
    return login_success(email, 'dummy', 'dummy', 'local handler', nick='example user')


@login_required
@auth_bp.route('/logout', endpoint='logout')
def logout():
    logout_user()
    session.pop('access_token', None)
    flash(_('You have been logged out'), category='warning')
    return redirect(url_for('home.index'))