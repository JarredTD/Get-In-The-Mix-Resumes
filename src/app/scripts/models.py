"""Models for the Flask App"""

from datetime import datetime
from typing_extensions import Any, Dict
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class ResumeData(db.Model):
    """
    Represents resume data for an individual.

    This class is a SQLAlchemy model that represents the 'resume_data' table,
    which stores information about individuals' resumes. Each instance of this class
    corresponds to a row in the table.

    :ivar id: The primary key of the 'resume_data' table. Unique identifier
              for each resume.
    :type id: int
    :ivar first_name: The first name of the individual. This field is indexed to improve
                      query performance when searching by first name.
    :type first_name: str
    :ivar last_name: The last name of the individual. This field is also indexed.
    :type last_name: str
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    entry_date = db.Column(
        db.DateTime, nullable=False, index=True, default=datetime.utcnow
    )

    def __repr__(self):
        """
        Provides a string representation of a ResumeData instance,
        which includes the first and last name of the individual.

        :return: A string representation of the instance, including
                 the first and last name.
        :rtype: str
        """
        return f"<User {self.first_name} {self.last_name}>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dict structure of the table
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date": self.entry_date,
        }


class User(db.Model, UserMixin):
    """
    Represents a user within the database, inheriting from ``db.Model``
    and ``UserMixin``.

    Attributes:
        id (int): Unique identifier for the user, serves as the primary key.
        username (str): The user's username, must be unique and is indexed.
        password_hash (str): The hashed version of the user's password.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """
        Provides a string representation of a User instance,
        which includes the username and password of the individual.

        :return: A string representation of the instance, including
                    the username and password.
        :rtype: str
        """
        return f"<User {self.username}, {self.password_hash}>"

    def set_password(self, password):
        """
        Generates a password hash for the given password and stores it.

        :param password: The plaintext password to hash and store.
        :type password: str
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the given password matches the stored password hash.

        :param password: The plaintext password to verify against the stored hash.
        :type password: str
        :return: True if the password matches the stored hash, False otherwise.
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)
