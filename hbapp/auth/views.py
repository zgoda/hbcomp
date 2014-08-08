from flask import render_template, session, request, flash, redirect, url_for
from flask.ext.login import logout_user, login_required

from hbapp.auth import auth_bp
from hbapp.auth.utils import login_success
from hbapp.auth.service import services


@auth_bp.route('/select', endpoint='select')
def select_provider():
    session['next'] = request.args.get('next')
    return render_template('auth/select.html')


@auth_bp.route('/login/<provider>', endpoint='login')
def remote_login(provider):
    if provider == 'local':
        return local_login_callback(request.args.get('email', None))
    if not provider in services:
        flash('Service "%(provider)s" is not supported' % {'provider': provider}, category='error')
        return redirect(url_for('auth.select'))
    view_name = 'auth.callback-%s' % provider
    callback = url_for(view_name, _external=True)
    service = services[provider]
    return service.authorize(callback=callback)


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
    return redirect(url_for('main'))
