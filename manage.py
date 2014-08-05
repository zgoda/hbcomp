from flask.ext.script import Manager, Server, Shell

from notesapp import make_app


manager = Manager(make_app)

manager.add_command('runserver', Server(host='0.0.0.0'))
manager.add_command('shell', Shell())


@manager.command
def initdb():
    """Initialize empty database"""
    from notesapp.models import db
    db.create_all()


@manager.command
def cleardb():
    """Clear database"""
    from notesapp.models import db
    db.drop_all()


@manager.command
def recreatedb():
    """Recreate database from scratch"""
    from notesapp.models import db
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
