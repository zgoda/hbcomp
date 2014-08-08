import os

from flask import Flask, send_from_directory, g
from flask.ext.login import LoginManager, current_user


login_manager = LoginManager()


def make_app():
    app = Flask(__name__)

    # configure application
    app.config.from_object('hbapp.config')

    # init extensions
    from hbapp.models import db
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.select'
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'warning'

    # register blueprints
    from hbapp.home import home_bp
    from hbapp.profile import profile_bp
    from hbapp.comp import comp_bp
    from hbapp.auth import auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(comp_bp, url_prefix='/comp')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    if app.config['DEBUG']:
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static'),
                'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.before_request
    def before_request():
        g.user = current_user

    # we're ready
    return app


@login_manager.user_loader
def get_user(userid):
    from hbapp.models import User
    return User.query.get(userid)
