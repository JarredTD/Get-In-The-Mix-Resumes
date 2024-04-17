"""Model for skill data"""

from . import db


class Skill(db.Model):
    """
    Represents a skill possessed by an individual.

    Attributes:
        id (db.Column): Primary key.
        name (db.Column): The name of the skill.
        resumes (db.relationship): Relationship back to the ResumeData model through
                                   a secondary association table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    resumes = db.relationship(
        "ResumeData", secondary="resume_skills", back_populates="skills"
    )

    def to_dict(self):
        """
        Generates a dictionary from the Skill instance, primarily for serialization.

        This method focuses on the skill's own attributes and does not delve into the
        related resumes to avoid circular reference issues in serialization processes.

        :return: A simplified dictionary representation of the Skill instance.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
        }
