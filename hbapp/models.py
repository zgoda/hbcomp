import datetime

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), nullable=False, index=True)
    location = db.Column(db.String(200))
    location_computed = db.Column(db.Text)
    access_token = db.Column(db.Text)
    oauth_token = db.Column(db.Text)
    oauth_token_secret = db.Column(db.Text)
    oauth_service = db.Column(db.String(50))
    remote_userid = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        db.Index('user_remote_id', 'oauth_service', 'remote_userid'),
    )

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    edition = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, index=True)
    entries_start_date = db.Column(db.Date, nullable=False)
    entries_finish_date = db.Column(db.Date, nullable=False, index=True)
    announcement = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text)
    purely_virtual = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
