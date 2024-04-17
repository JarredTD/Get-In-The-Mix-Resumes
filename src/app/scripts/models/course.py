"""Model for course data"""

from . import db


class Course(db.Model):
    """
    Represents a course relevant to an individual's career or interests.

    Attributes:
        id (db.Column): Primary key.
        name (db.Column): The name of the course.
        resumes (db.relationship): Relationship back to the ResumeData model through
                                   a secondary association table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    resumes = db.relationship(
        "ResumeData", secondary="resume_courses", back_populates="courses"
    )

    def to_dict(self):
        """
        Serializes the Course instance into a dictionary, omitting detailed
        relational data to prevent circular references and simplify the output.

        This is particularly useful for APIs where a concise representation of
        a Course is needed.

        :return: A dictionary containing the Course's primary information.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
        }
