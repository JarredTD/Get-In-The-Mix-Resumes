"""Form for skill data"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SkillForm(FlaskForm):
    """
    A form for listing skills.

    Allows users to input individual skills, which can include programming
    languages, software proficiency, or other professional skills relevant
    to their resume.

    Attributes:
        name (StringField): The name of the skill. Required.
    """

    name = StringField("Skill Name", validators=[DataRequired()])
