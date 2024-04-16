from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    """
    Represents a user within the database, including authentication data.

    Attributes:
        id (db.Column): Primary key, unique identifier for the user.
        username (db.Column): User's username, must be unique and is indexed.
        password_hash (db.Column): Hashed version of the user's password.

    Methods:
        set_password(password): Hashes a password and stores it.
        check_password(password): Checks a password against the stored hash.
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
