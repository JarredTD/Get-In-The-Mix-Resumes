"""Form for the extracurricular data"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ExtracurricularForm(FlaskForm):
    """
    A form for inputting extracurricular activities details.

    Attributes:
        name (StringField): The name of the club, organization, or activity.
        title (StringField): Role or position held in the extracurricular activity.
        bullet_points (TextAreaField): Descriptive bullet points of responsibilities
        and achievements.
    """

    name = StringField("Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    bullet_points = TextAreaField("Bullet Points", validators=[Optional()])
