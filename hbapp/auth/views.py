from flask import render_template, session, request, flash, redirect, url_for, current_app, abort
from flask.ext.login import logout_user, login_required

from hbapp.auth import auth_bp
from hbapp.auth.utils import login_success
from hbapp.auth.service import services, google


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
    if not provider in services:
        flash('Service "%(provider)s" is not supported' % dict(provider=provider), category='error')
        return redirect(url_for('auth.select'))
    view_name = 'auth.callback-%s' % provider
    callback = url_for(view_name, _external=True)
    service = services[provider]
    return service.authorize(callback=callback)


@auth_bp.route('/callback/google', endpoint='callback-google')
@google.authorized_handler
def google_remote_login_callback(resp):  # pragma: no cover
    if resp is None:
        flash('Access denied, reason: %(reason)s error: %s(error)s' % request.args, category='error')
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
    session.pop('access_token')
    return redirect(url_for('main'))
