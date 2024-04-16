from . import db
from .json_list import JsonList


class Extracurricular(db.Model):
    """
    Represents an individual's extracurricular activities.

    Attributes:
        id (db.Column): Primary key.
        resume_id (db.Column): Foreign key linking to the ResumeData model.
        name (db.Column): Name of the club, organization, or activity.
        title (db.Column): Role or position held in the extracurricular activity.
        bullet_points (db.Column): Descriptive bullet points of responsibilities
                                   and achievements.
    """

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume_data.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    bullet_points = db.Column(JsonList)

    def to_dict(self):
        """
        Serializes the Extracurricular instance into a dictionary.

        The bullet_points attribute, being a JSON serializable list, is
        included directly allowing for easy conversion to JSON format.

        :return: A dictionary representation of the Extracurricular instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "name": self.name,
            "title": self.title,
            "bullet_points": self.bullet_points,
        }
