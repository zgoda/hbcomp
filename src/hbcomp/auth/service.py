from flask import session

from ..ext import oauth


google = oauth.remote_app('google', app_key='GOOGLE')


services = {
    'google': google,
}


@google.tokengetter
def get_access_token():
    return session.get('access_token')
