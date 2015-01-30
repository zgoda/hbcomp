from wtforms.validators import DataRequired, Email
from wtforms.fields import StringField

from ..utils.forms import BaseObjectForm as Form
from ..models import User


class ProfileForm(Form):
    name = StringField('name')
    email = StringField('email', validators=[DataRequired(), Email()])
    location = StringField('location')

    def save(self, obj=None, save=True):
        if obj is None:
            obj = User()
        return super(ProfileForm, self).save(obj, save)
