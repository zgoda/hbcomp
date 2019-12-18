from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from .app import create_app
from .ext import db


def make_app(info):
    load_dotenv(find_dotenv())
    return create_app()


cli = FlaskGroup(create_app=make_app)
cli.help = 'This is a management script for the HBComp application.'


@cli.group(name='db', help='database management commands')
def db_ops():
    pass


@db_ops.command('init', short_help='initialize missing database objects')
def initdb():
    db.create_all()


@db_ops.command('clear', short_help='remove all database objects')
def cleardb():
    db.drop_all()


@db_ops.command('recreate', short_help='recreate all database objects from scratch')
def recreatedb():
    db.drop_all()
    db.create_all()
