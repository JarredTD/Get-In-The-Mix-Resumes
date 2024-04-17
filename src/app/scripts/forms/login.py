"""Form for login"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


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
