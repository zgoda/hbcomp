import os
os.environ['FLASK_DEBUG'] = '1'
import unittest

import click
from flask.cli import FlaskGroup


def create_hbc_app(info):
    from hbapp import create_app
    return create_app()


cli = FlaskGroup(create_app=create_hbc_app)
cli.help = 'This is a management script for the HBC application.'


@cli.command('initdb', short_help='Initialize missing database objects')
def initdb():
    from hbapp.ext import db
    db.create_all()


@cli.command('cleardb', short_help='Remove all database objects')
def cleardb():
    from hbapp.ext import db
    db.drop_all()


@cli.command('recreatedb', short_help='Recreate all database objects from scratch')
def recreatedb():
    from hbapp.ext import db
    db.drop_all()
    db.create_all()


@click.command('test', short_help='Run tests from application suite')
@click.option('-v', '--verbosity', type=int, default=1)
@click.option('-d', '--testdir', default='tests')
@click.option('-p', '--pattern', default='test_*.py')
@click.argument('labels', required=False, nargs=-1)
def run_tests(labels, verbosity, testdir, pattern):
    dirparts = testdir.split('/')
    if labels:
        prefix = '.'.join(dirparts)
        if prefix:
            names = ['%s.%s' % (prefix, name) for name in labels]
        else:
            names = labels
        suite = unittest.TestLoader().loadTestsFromNames(names)
    else:
        if dirparts:
            testdir = '/'.join(dirparts)
        else:
            testdir = '.'
        suite = unittest.TestLoader().discover(testdir, pattern=pattern)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)


cli.add_command(run_tests)


if __name__ == '__main__':
    cli()
