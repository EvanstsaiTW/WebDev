from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError


class SearchForm(FlaskForm):
    key = StringField("keywords", validators=[DataRequired()])
    submit = SubmitField('search!')