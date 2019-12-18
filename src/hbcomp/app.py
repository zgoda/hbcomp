import os

from flask import Flask, request, send_from_directory
from flask_babel import lazy_gettext as _

from .auth import auth_bp
from .comp import comp_bp
from .ext import babel, db, login_manager
from .home import home_bp
from .models import User
from .profile import profile_bp
from .utils import pagination

__all__ = ['create_app']


def create_app():
    app = Flask(__name__.split('.')[0])
    configure_app(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_templates(app)
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
            return send_from_directory(
                os.path.join(app.root_path, 'static'), 'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )


def configure_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(comp_bp, url_prefix='/comp')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def configure_extensions(app):
    db.init_app(app)

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


def configure_templates(app):
    app.jinja_env.globals.update({
        'url_for_other_page': pagination.url_for_other_page,
    })


def configure_logging(app):
    pass


def configure_error_handlers(app):
    pass
