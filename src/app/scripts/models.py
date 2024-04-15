"""Models for the Flask App.

This module contains the SQLAlchemy model definitions used in a Flask application
for managing resume data, user authentication, and related functionalities.
"""

# pylint: disable=too-many-ancestors, too-few-public-methods, abstract-method

import json
from datetime import datetime
from typing_extensions import Any, Dict
from sqlalchemy import TypeDecorator, Text
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class JsonList(TypeDecorator):
    """
    A custom SQLAlchemy column type for storing lists as JSON-formatted strings.

    This type automatically serializes Python lists to JSON strings when data is
    bound to the database, and deserializes JSON strings back to Python lists when
    querying the data. It's designed to be used as a column type in SQLAlchemy models
    for fields that require storing list data in a relational database.

    Inherits from:
        TypeDecorator: A generic superclass from SQLAlchemy for creating custom types.

    Example:
        class MyModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            my_list = db.Column(JSONList)

    After defining a model with `JSONList`, you can directly assign Python
    lists to `my_list`, and they will be stored as JSON strings in the
    database. When querying, these strings will be returned as Python lists.
    """

    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """
        Process the Python value before saving it to the database.

        This method serializes Python lists to JSON strings. If the value is
        `None`, it remains `None`.

        :param value: The original Python list to be serialized to JSON.
        :param dialect: The dialect in use (not used in this method but required
                        by the interface).
        :return: A JSON string representation of the list, or `None` if the
                 original value was `None`.
        """
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """
        Process the database value back to a Python type after querying.

        This method deserializes JSON strings back into Python lists. If the value is
        `None`, it remains `None`.

        :param value: The JSON string from the database to be deserialized.
        :param dialect: The dialect in use (not used in this method but required by
                        the interface).
        :return: A Python list representation of the JSON string, or `None` if the
                original value was `None`.
        """
        if value is not None:
            value = json.loads(value)
        return value


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

    def to_dict(self) -> Dict[str, Any]:
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
