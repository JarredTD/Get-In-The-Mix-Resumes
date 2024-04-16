from . import db
from .json_list import JsonList


class Project(db.Model):
    """
    Represents a project undertaken by an individual.

    Attributes:
        id (db.Column): Primary key.
        resume_id (db.Column): Foreign key linking to the ResumeData model.
        name (db.Column): Project name.
        language_stack (db.Column): Primary technologies or languages used in
                                    the project.

        bullet_points (db.Column): Descriptive bullet points of the project scope,
                                   achievements, or other relevant details.
    """

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume_data.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    language_stack = db.Column(db.String(255), nullable=False)
    bullet_points = db.Column(JsonList)

    def to_dict(self):
        """
        Converts the Project instance to a dictionary, suitable for JSON serialization.

        This includes the language stack and bullet_points as direct mappings, with
        bullet_points formatted as a JSON list.

        :return: A dictionary representation of the Project attributes.
        :rtype: dict
        """
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "name": self.name,
            "language_stack": self.language_stack,
            "bullet_points": self.bullet_points,
        }
