from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    """
    A form for entering courses.

    Designed to capture information about relevant courses completed by the user,
    which may be pertinent to their educational background or professional expertise.

    Attributes:
        name (StringField): The name of the course. Required.
    """

    name = StringField("Course Name", validators=[DataRequired()])
