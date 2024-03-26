"""Models for the Flask App"""

from typing_extensions import Any, Dict
from datetime import datetime
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
