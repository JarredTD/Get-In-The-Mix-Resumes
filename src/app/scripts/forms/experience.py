from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ExperienceForm(FlaskForm):
    """
    A form for inputting work experience details.

    Attributes:
        company_name (StringField): The name of the company. Required.
        title (StringField): The job title. Required.
        start_date (DateField): The start date of the experience. Required.
        end_date (DateField): The end date of the experience. Optional.
        bullet_points (TextAreaField): A list of accomplishments or responsibilities.
                                       Optional
    """

    company_name = StringField("Company Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[Optional()])
    bullet_points = TextAreaField("Bullet Points", validators=[Optional()])
