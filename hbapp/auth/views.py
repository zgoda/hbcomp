from flask import render_template, session, request

from hbapp.auth import auth_bp


@auth_bp.route('/select', endpoint='select')
def select_provider():
    session['next'] = request.args.get('next')
    return render_template('auth/select.html')
