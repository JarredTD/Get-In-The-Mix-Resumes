from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ProjectForm(FlaskForm):
    """
    A form for detailing projects.

    This form captures information about significant projects, including
    academic, personal, or professional projects.

    Attributes:
        name (StringField): The name of the project. Required.
        language_stack (StringField): The primary technologies or languages used
                                      in the project. Required.

        bullet_points (TextAreaField): Descriptive bullet points detailing the
                                       project's scope, achievements, or any other
                                       relevant information. Optional.
    """

    name = StringField("Project Name", validators=[DataRequired()])
    language_stack = StringField("Language/Stack", validators=[DataRequired()])
    bullet_points = TextAreaField("Bullet Points", validators=[Optional()])
