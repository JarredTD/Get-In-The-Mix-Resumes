from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from ..models import User


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
