from flask import session
from flask import current_app as app

from flask.ext.oauthlib.client import OAuth


oauth = OAuth(app)


google = oauth.remote_app('google', app_key='GOOGLE')


services = {
    'google': google,
}


@google.tokengetter
def get_access_token():
    return session.get('access_token')
