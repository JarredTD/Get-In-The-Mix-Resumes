"""Model for education data"""

from . import db


class Education(db.Model):
    """
    Represents an individual's educational background.

    Attributes:
        id (db.Column): Primary key.
        resume_id (db.Column): Foreign key linking to the ResumeData model.
        school (db.Column): Name of the school or university.
        major (db.Column): Major field of study.
        minor (db.Column): Minor field of study (if applicable).
        grad_year (db.Column): Year of graduation.
    """

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume_data.id"), nullable=False)
    school = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    minor = db.Column(db.String(255))
    grad_year = db.Column(db.Integer)

    def to_dict(self):
        """
        Converts the Education instance to a dictionary format for easier
        serialization.

        Minor field may be None if not specified. The graduation year is
        included directly.

        :return: Dictionary containing key details of the Education instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "school": self.school,
            "major": self.major,
            "minor": self.minor,
            "grad_year": self.grad_year,
        }
