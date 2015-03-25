from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import IntegerField, DateField
from wtforms.validators import DataRequired, Optional
from flask_login import current_user

from ..utils.forms import BaseObjectForm as Form
from ..models import Competition


class CompetitionForm(Form):
    title = StringField(validators=[DataRequired()])
    edition = IntegerField(validators=[Optional()])
    announcement = TextAreaField(validators=[DataRequired()])
    date = DateField(validators=[DataRequired()])
    qualify_date = DateField(validators=[Optional()])
    entries_start_date = DateField(validators=[DataRequired()])
    entries_finish_date = DateField(validators=[DataRequired()])
    url = StringField()
    contact_emails = TextAreaField()
    location = TextAreaField()

    def save(self, obj=None, save=True):
        if obj is None:
            obj = Competition(owner=current_user)
        return super(CompetitionForm, self).save(obj, save)