DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'sqlite://'

FLATPAGES_EXTENSION = '.html.md'
FLATPAGES_MARKDOWN_EXTENSIONS = []

try:
    from config_local import *  # NOQA
except ImportError:
    pass
