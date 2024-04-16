from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ExtracurricularForm(FlaskForm):
    """
    A form for inputting extracurricular activities details.

    Attributes:
        name (StringField): The name of the club, organization, or activity. Required.
        title (StringField): Role or position held in the extracurricular activity. Required.
        bullet_points (TextAreaField): Descriptive bullet points of responsibilities and achievements. Optional.
    """

    name = StringField("Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    bullet_points = TextAreaField("Bullet Points", validators=[Optional()])
