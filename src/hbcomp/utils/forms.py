from flask_wtf import FlaskForm
from wtforms import BooleanField
from flask_babel import lazy_gettext as _

from ..ext import db


class BaseForm(FlaskForm):
    pass


class BaseObjectForm(BaseForm):

    def save(self, obj, save=False):
        self.populate_obj(obj)
        if save:
            db.session.add(obj)
            db.session.commit()
        return obj


class DeleteForm(BaseForm):
    delete_it = BooleanField(_('delete'), default=False)
