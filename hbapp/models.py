import datetime

from flask import current_app
from flask_login import UserMixin

from .ext import db
from .utils.sqla import ModelMixin


class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'  # "user" is a reserved word in many engines
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

    def is_active(self):
        return self.is_active

    def get_full_name(self):
        return self.name or self.email


class Category(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)


categories = db.Table('competition_categories',
    db.Column('competition_id', db.Integer, db.ForeignKey('competition.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Index('uix_competition_categories', 'competition_id', 'category_id', unique=True),
)


class Competition(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    edition = db.Column(db.Integer)
    qualify_date = db.Column(db.Date)
    date = db.Column(db.Date, nullable=False, index=True)
    entries_start_date = db.Column(db.Date, nullable=False)
    entries_finish_date = db.Column(db.Date, nullable=False, index=True)
    announcement = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text)
    contact_emails = db.Column(db.Text)
    location = db.Column(db.Text)
    location_computed = db.Column(db.Text)
    purely_virtual = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('competitions', lazy='dynamic'))
    categories = db.relationship('Category', secondary=categories,
        backref=db.backref('competitions', lazy='dynamic'))
    is_active = db.Column(db.Boolean, default=False)

    @classmethod
    def recent(cls, limit=None):
        if limit is None:
            limit = current_app.config.get('LIST_LIMIT', 5)
        return cls.query.filter_by(is_active=True).order_by(db.desc(cls.id)).limit(limit)

    @classmethod
    def upcoming(cls, limit=None):
        if limit is None:
            limit = current_app.config.get('LIST_LIMIT', 5)
        return cls.query.filter(
            cls.date>=datetime.datetime.utcnow(), cls.is_active==True
        ).order_by(cls.date).limit(limit)


class Entry(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('entries', lazy='dynamic'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    competition = db.relationship('Competition', backref=db.backref('entries', lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('entries', lazy='dynamic'))
    name = db.Column(db.String(200), nullable=False)
    received = db.Column(db.Date, default=datetime.date.today)
    remarks = db.Column(db.Text)
    recipe = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'competition_id', 'category_id', name='uix_competition_user_entries'),
    )


class Note(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    entry = db.relationship('Entry', backref=db.backref('notes'))
    defects = db.Column(db.Text)
    aroma_note = db.Column(db.Integer, nullable=False)  # max = 12
    aroma_remarks = db.Column(db.Text)
    colour_note = db.Column(db.Integer, nullable=False)  # max = 3
    colour_remarks = db.Column(db.Text)
    head_note = db.Column(db.Integer, nullable=False)  # max = 6
    head_remarks = db.Column(db.Text)
    taste_note = db.Column(db.Integer, nullable=False)  # max = 17
    taste_remarks = db.Column(db.Text)
    bitterness_note = db.Column(db.Integer, nullable=False)  # max = 6
    bitterness_remarks = db.Column(db.Text)
    texture_note = db.Column(db.Integer, nullable=False)  # max = 6
    texture_remarks = db.Column(db.Text)
    general_remarks = db.Column(db.Text)
    judge_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    judge = db.relationship('User', backref=db.backref('notes', lazy='dynamic'))
    final_note = db.Column(db.Integer, nullable=False)  # max = 50


# Note events
def note_pre_save(mapper, connection, target):
    target.final_note = sum([
        target.aroma_note,
        target.colour_note,
        target.head_note,
        target.taste_note,
        target.bitterness_note,
        target.texture_note,
    ])


db.event.listen(Note, 'before_insert', note_pre_save)
db.event.listen(Note, 'before_update', note_pre_save)
