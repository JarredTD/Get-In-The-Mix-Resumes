"""Form for meta data, and housing other forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, FormField
from wtforms.validators import DataRequired, Email, Optional
from . import (
    ExperienceForm,
    EducationForm,
    ExtracurricularForm,
    ProjectForm,
    SkillForm,
    CourseForm,
)


class ResumeForm(FlaskForm):
    """
    A comprehensive form for creating or updating a resume.

    Attributes:
        first_name (StringField): The individual's first name. Required.
        last_name (StringField): The individual's last name. Required.
        email (StringField): The individual's email address. Required and must be a
                             valid email format.

        phone_number (StringField): The individual's phone number. Required.
        github_link (StringField): URL to the individual's GitHub profile. Optional.
        linkedin_link (StringField): URL to the individual's LinkedIn profile. Optional.
        experiences (FieldList): A list of forms for inputting experiences.
                                 At least one entry required.

        educations (FieldList): A list of forms for inputting educational backgrounds.
                                At least one entry required.

        projects (FieldList): A list of forms for inputting projects.
                              At least one entry required.

        skills (FieldList): A list of forms for inputting skills.
                            At least one entry required.

        courses (FieldList): A list of forms for inputting courses.
                             At least one entry required.

        submit (SubmitField): Button to submit the form.
    """

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    github_link = StringField("Github Link", validators=[Optional()])
    linkedin_link = StringField("LinkedIn Link", validators=[Optional()])
    experiences = FieldList(FormField(ExperienceForm), min_entries=1)
    educations = FieldList(FormField(EducationForm), min_entries=1)
    extracurriculars = FieldList(FormField(ExtracurricularForm), min_entries=1)
    projects = FieldList(FormField(ProjectForm), min_entries=1)
    skills = FieldList(FormField(SkillForm), min_entries=1)
    courses = FieldList(FormField(CourseForm), min_entries=1)
    submit = SubmitField("Submit")
