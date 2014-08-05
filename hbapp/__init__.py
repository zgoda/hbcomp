import os

from flask import Flask, send_from_directory

from hbapp.home import home_bp
from hbapp.auth import auth_bp


def make_app():
    app = Flask(__name__)

    # configure application
    app.config.from_object('hbapp.config')

    # init extensions
    from hbapp.models import db
    db.init_app(app)

    # register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    if app.config['DEBUG']:
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static'),
                'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # we're ready
    return app
