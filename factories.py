from factory.alchemy import SQLAlchemyModelFactory

from hbapp.models import db, User


class UserFactory(SQLAlchemyModelFactory):
    model = User
    sqlalchemy_session = db.session


def initial_data():
    for n in range(3):
        email = 'user_%s@example.com' % n
        user = User(email=email)
        db.session.add(user)
    db.session.commit()
