"""Forms for validation through flask-wtf.

This module defines Flask-WTF form classes for various functionalities including
user login, registration, and resume data input such as experience, education,
projects, skills, and courses.
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Optional
from wtforms import (
    StringField,
    PasswordField,
    IntegerField,
    SubmitField,
    FormField,
    FieldList,
    DateField,
    TextAreaField,
)
from .models import User


class LoginForm(FlaskForm):
    """
    A form for user login.

    Attributes:
        username (StringField): Input field for the username. Required.
        password (PasswordField): Input field for the password. Required.
        submit (SubmitField): Button to submit the form.
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """
    A form for user registration.

    Attributes:
        username (StringField): Input field for the username. Required.
        password (PasswordField): Input field for the password. Required.
        confirm_password (PasswordField): Input field to confirm the password.
            Must match the password field. Required.

        submit (SubmitField): Button to submit the form.

    Methods:
        validate_username: Validates that the provided username is not already taken.
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validates that the provided username is not already taken by another user
        in the database.

        This method queries the database for the existence of the given username.
        If the username is found, it raises a ValidationError with an
        appropriate message indicating that the username is already in use.

        :param username: The username field from the form, which is an
                        instance of wtforms.fields.StringField. It contains
                        the submitted username.

        :type username: wtforms.fields.StringField
        :raises ValidationError: If the username already exists in the database.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken. Please choose a different one."
            )


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


class SkillForm(FlaskForm):
    """
    A form for listing skills.

    Allows users to input individual skills, which can include programming languages,
    software proficiency, or other professional skills relevant to their resume.

    Attributes:
        name (StringField): The name of the skill. Required.
    """

    name = StringField("Skill Name", validators=[DataRequired()])


class CourseForm(FlaskForm):
    """
    A form for entering courses.

    Designed to capture information about relevant courses completed by the user,
    which may be pertinent to their educational background or professional expertise.

    Attributes:
        name (StringField): The name of the course. Required.
    """

    name = StringField("Course Name", validators=[DataRequired()])


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
