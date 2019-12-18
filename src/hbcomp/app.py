import os
from logging.config import dictConfig
from typing import Optional

from flask import render_template, request, send_from_directory
from flask_babel import get_locale, lazy_gettext as _
from werkzeug.utils import ImportStringError

from .auth import auth_bp
from .comp import comp_bp
from .ext import babel, csrf, db, login_manager, pages
from .home import home_bp
from .models import User
from .profile import profile_bp
from .utils import pagination
from .utils.app import Application

__all__ = ['create_app']


def create_app(env: Optional[str] = None) -> Application:
    flask_environment = os.environ.get('FLASK_ENV', '').lower()
    if flask_environment == 'production':
        configure_logging()
    app = Application()
    configure_app(app, env)
    configure_extensions(app)
    with app.app_context():
        configure_blueprints(app)
        configure_templates(app)
        configure_error_handlers(app)
    return app


def configure_app(app: Application, env: Optional[str]):
    app.config.from_object('hbcomp.config')
    if env is not None:
        try:
            app.config.from_object(f'hbcomp.config_{env}')
        except ImportStringError:
            app.logger.info(f'no environment configuration for {env}')
    if app.config['DEBUG']:
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static'), 'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )


def configure_blueprints(app: Application):
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(comp_bp, url_prefix='/comp')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def configure_extensions(app: Application):
    db.init_app(app)
    csrf.init_app(app)
    pages.init_app(app)
    pages.get('foo')

    if not app.testing:
        @babel.localeselector
        def get_locale():
            accept_languages = app.config.get('ACCEPT_LANGUAGES', ['pl', 'en'])
            return request.accept_languages.best_match(accept_languages)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    babel.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _('Please log in to access this page')
    login_manager.login_message_category = 'warning'


def configure_templates(app: Application):
    app.jinja_env.globals.update({
        'url_for_other_page': pagination.url_for_other_page,
        'get_locale': get_locale,
    })


def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi'],
        },
    })


def configure_error_handlers(app: Application):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
