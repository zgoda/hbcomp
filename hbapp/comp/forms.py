from wtforms.fields import StringField, TextAreaField, BooleanField
from wtforms.fields.html5 import IntegerField, DateField
from wtforms.validators import DataRequired
from flask_login import current_user

from ..utils.forms import BaseObjectForm as Form
from ..models import Competition


class CompetitionForm(Form):
    title = StringField(validators=[DataRequired()])
    edition = IntegerField()
    announcement = TextAreaField(validators=[DataRequired()])
    date = DateField(validators=[DataRequired()])
    qualify_date = DateField()
    entries_start_date = DateField(validators=[DataRequired()])
    entries_finish_date = DateField(validators=[DataRequired()])
    url = StringField()
    contact_emails = TextAreaField()
    location = TextAreaField()
    purely_virtual = BooleanField()
    is_active = BooleanField()

    def save(self, obj=None, save=True):
        if obj is None:
            obj = Competition(owner=current_user)
        return super(CompetitionForm, self).save(obj, save)
