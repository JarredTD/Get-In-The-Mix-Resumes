from datetime import datetime
from . import db


class ResumeData(db.Model):
    """
    Represents resume data for an individual, encapsulating personal
    and professional details.

    Attributes:
        id (db.Column): Primary key.
        user_id (db.Column): Foreign key linking to the User model.
        first_name (db.Column): The individual's first name.
        last_name (db.Column): The individual's last name.
        email (db.Column): The individual's email address.
        phone_number (db.Column): The individual's phone number.
        github_link (db.Column): URL to the individual's GitHub profile.
        linkedin_link (db.Column): URL to the individual's LinkedIn profile.
        entry_date (db.Column): Timestamp of when the resume entry was created.
        experiences (db.relationship): Relationship to the Experience model.
        educations (db.relationship): Relationship to the Education model.

        extracurriculars (db.relationship): Relationship to the Extracurricular
                                            model.

        projects (db.relationship): Relationship to the Project model.

        skills (db.relationship): Relationship to the Skill model, through a
                                  secondary association table.

        courses (db.relationship): Relationship to the Course model,
                                   through a secondary association table.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    github_link = db.Column(db.String(255))
    linkedin_link = db.Column(db.String(255))
    entry_date = db.Column(
        db.DateTime, nullable=False, index=True, default=datetime.utcnow
    )

    experiences = db.relationship("Experience", backref="resume", lazy=True)
    educations = db.relationship("Education", backref="resume", lazy=True)
    extracurriculars = db.relationship("Extracurricular", backref="resume", lazy=True)
    projects = db.relationship("Project", backref="resume", lazy=True)
    skills = db.relationship(
        "Skill", secondary="resume_skills", back_populates="resumes"
    )
    courses = db.relationship(
        "Course", secondary="resume_courses", back_populates="resumes"
    )

    def __repr__(self):
        """
        Provides a string representation of a ResumeData instance.

        :return: A string representation of the instance.
        :rtype: str
        """
        return f"<User {self.user_id} {self.first_name} {self.last_name}>"

    def to_dict(self):
        """
        Converts the resume data into a dictionary format.

        This method is useful for serializing the resume data into a format that
        can be easily converted to JSON, sent via APIs, or used in other contexts
        where a Python dictionary is needed.

        :return: A dictionary representation of the resume data. The 'date' key
                 corresponds to the 'entry_date' attribute, formatted as a
                 datetime object.
        :rtype: dict
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "github_link": self.github_link,
            "linkedin_link": self.linkedin_link,
            "entry_date": (
                self.entry_date.isoformat() if self.entry_date else None
            ),  # ISO 8601 format
            "experiences": [experience.to_dict() for experience in self.experiences],
            "educations": [education.to_dict() for education in self.educations],
            "extracurriculars": [
                extracurricular.to_dict() for extracurricular in self.extracurriculars
            ],
            "projects": [project.to_dict() for project in self.projects],
            "skills": [skill.to_dict() for skill in self.skills],
            "courses": [course.to_dict() for course in self.courses],
        }


# Association tables
resume_skills = db.Table(
    "resume_skills",
    db.Column(
        "resume_id", db.Integer, db.ForeignKey("resume_data.id"), primary_key=True
    ),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)

resume_courses = db.Table(
    "resume_courses",
    db.Column(
        "resume_id", db.Integer, db.ForeignKey("resume_data.id"), primary_key=True
    ),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
)
