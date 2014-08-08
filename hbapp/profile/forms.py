from flask.ext.wtf import Form
from wtforms.validators import DataRequired, Email
from wtforms.fields import StringField


class ProfileForm(Form):
    name = StringField('name')
    email = StringField('email', validators=[DataRequired(), Email()])
    location = StringField('location')
