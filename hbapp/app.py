import os

from flask import Flask, request, send_from_directory, g
from flask_login import current_user
from flask_babel import lazy_gettext as _

from .models import User
from .ext import db, login_manager, oauth, babel, pages, bootstrap


__all__ = ['create_app']


def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_hooks(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)
    return app


def configure_app(app):
    app.config.from_object('hbapp.config')
    if os.environ.get('HB_CONFIG'):
        app.config.from_envvar('HB_CONFIG')
    if app.config['DEBUG']:
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(os.path.join(app.root_path, 'static'),
                'favicon.ico', mimetype='image/vnd.microsoft.icon')


def configure_hooks(app):
    @app.before_request
    def before_request():
        g.user = current_user


def configure_blueprints(app):
    from hbapp.home import home_bp
    app.register_blueprint(home_bp)
    from hbapp.profile import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')
    from hbapp.comp import comp_bp
    app.register_blueprint(comp_bp, url_prefix='/comp')
    from hbapp.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


def configure_extensions(app):
    db.init_app(app)

    oauth.init_app(app)

    bootstrap.init_app(app)

    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES', ['pl', 'en'])
        return request.accept_languages.best_match(accept_languages)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _('Please log in to access this page')
    login_manager.login_message_category = 'warning'

    pages.init_app(app)
    pages.get('foo')  # preload all pages


def configure_logging(app):
    pass


def configure_error_handlers(app):
    pass
