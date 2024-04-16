from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class EducationForm(FlaskForm):
    """
    A form for inputting educational background details.

    Attributes:
        school (StringField): The name of the school or university. Required.
        major (StringField): The major field of study. Required.
        minor (StringField): The minor field of study, if any. Optional.
        grad_year (IntegerField): The year of graduation. Required.
    """

    school = StringField("School", validators=[DataRequired()])
    major = StringField("Major", validators=[DataRequired()])
    minor = StringField("Minor", validators=[Optional()])
    grad_year = IntegerField("Graduation Year", validators=[DataRequired()])
