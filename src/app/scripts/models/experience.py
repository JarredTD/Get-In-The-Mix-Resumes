from . import db
from .json_list import JsonList


class Experience(db.Model):
    """
    Represents an individual's work experience.

    Attributes:
        id (db.Column): Primary key.
        resume_id (db.Column): Foreign key linking to the ResumeData model.
        company_name (db.Column): Name of the company.
        title (db.Column): Job title at the company.
        start_date (db.Column): Start date of the employment.
        end_date (db.Column): End date of the employment (if applicable).
        bullet_points (db.Column): Descriptive bullet points of job responsibilities
                                   and achievements.
    """

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume_data.id"), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    bullet_points = db.Column(JsonList)

    def to_dict(self):
        """
        Serializes the Experience instance into a dictionary.

        Converts date fields to ISO 8601 format strings for JSON compatibility.
        The bullet_points, stored as a JSON serializable list, are directly assignable.

        :return: A dictionary representation of the Experience instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "company_name": self.company_name,
            "title": self.title,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "bullet_points": self.bullet_points,
        }
