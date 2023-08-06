from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired


class SlideForm(FlaskForm):
    background = FileField('Background Image')
    foreground = FileField('Foreground Image')
    title = StringField('Text')
    show_logo = BooleanField('Show Logo', default=True)
    submit = SubmitField('Submit')
