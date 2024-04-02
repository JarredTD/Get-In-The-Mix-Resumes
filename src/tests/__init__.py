"""
Base class that other test classes inherit from.
Constants for tests.
"""

# pylint: disable=no-name-in-module, too-many-arguments

import unittest
from datetime import date
from app import create_app, db
from app.config import TestingConfig
from app.scripts.models import (
    User,
    ResumeData,
    Education,
    Experience,
    Extracurricular,
    Project,
    Course,
    Skill,
)

LOGIN_ROUTE = "/login"
REGISTER_ROUTE = "/register"
LOGOUT_ROUTE = "/logout"


class BaseTestCase(unittest.TestCase):
    """A base test case that sets up the application and database for testing."""

    user_template = {
        "username": "testuser",
        "password": "test",
    }

    resume_template = {
        "first_name": "Sample",
        "last_name": "User",
        "email": "sample@example.com",
        "phone_number": "123-456-7890",
        "github_link": "https://github.com/sampleuser",
        "linkedin_link": "https://www.linkedin.com/in/sampleuser/",
        # Note: "user_id" will be added dynamically based on the created test user
    }

    experience_template = {
        "company_name": "Test Company",
        "title": "Test Title",
        "start_date": date(2020, 1, 1),
        "end_date": date(2021, 1, 1),
        "bullet_points": ["Achievement 1", "Achievement 2"],
    }

    education_template = {
        "school": "Test University",
        "major": "Test Major",
        "minor": "Test Minor",
        "grad_year": 2024,
    }

    extracurricular_template = {
        "name": "Debate Club",
        "title": "Vice President",
        "bullet_points": [
            "Organized weekly debates",
            "Led team to regional championships",
        ],
    }

    project_template = {
        "name": "Test Project",
        "language_stack": "Python, JavaScript",
        "bullet_points": ["Feature 1", "Feature 2"],
    }

    skill_template = {
        "name": "Python Programming",
    }

    course_template = {
        "name": "Introduction to Python",
    }

    def setUp(self):
        """Prepare the test client and database for the Flask application."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.testuser = User(username=self.user_template["username"])
        self.testuser.set_password(self.user_template["password"])
        db.session.add(self.testuser)
        db.session.commit()

        self.complete_resume_template = self.resume_template.copy()
        self.complete_resume_template["user_id"] = self.testuser.id

    def tearDown(self):
        """Clean up after each test case."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password, route_append="", follow_redirects=True):
        """Helper method to log in as a user."""
        return self.client.post(
            LOGIN_ROUTE + route_append,
            data={"username": username, "password": password},
            follow_redirects=follow_redirects,
        )

    def register(
        self,
        username,
        password,
        confirm_password,
        route_append="",
        follow_redirects=True,
    ):
        """Helper method to register a new user."""
        return self.client.post(
            REGISTER_ROUTE + route_append,
            data={
                "username": username,
                "password": password,
                "confirm_password": confirm_password,
            },
            follow_redirects=follow_redirects,
        )

    def logout(self):
        """Helper method to log out a user."""
        return self.client.get(LOGOUT_ROUTE, follow_redirects=True)

    def create_resume_data(self):
        """Helper method to create ResumeData from the template."""
        resume_data = ResumeData(**self.complete_resume_template)
        db.session.add(resume_data)
        db.session.commit()
        return resume_data

    def create_experience(self, resume_id, overrides=None):
        """Helper method to create an Experience instance."""
        data = self.experience_template.copy()
        data["resume_id"] = resume_id
        if overrides:
            data.update(overrides)
        experience = Experience(**data)
        db.session.add(experience)
        db.session.commit()
        return experience

    def create_education(self, resume_id, overrides=None):
        """Helper method to create an Education instance."""
        data = self.education_template.copy()
        data["resume_id"] = resume_id
        if overrides:
            data.update(overrides)
        education = Education(**data)
        db.session.add(education)
        db.session.commit()
        return education

    def create_extracurricular(self, resume_id, overrides=None):
        """
        Helper method to create an Extracurricular instance associated with
        a ResumeData.
        """
        data = self.extracurricular_template.copy()
        data["resume_id"] = resume_id
        if overrides:
            data.update(overrides)
        extracurricular = Extracurricular(**data)
        db.session.add(extracurricular)
        db.session.commit()
        return extracurricular

    def create_project(self, resume_id, overrides=None):
        """Helper method to create a Project instance."""
        data = self.project_template.copy()
        data["resume_id"] = resume_id
        if overrides:
            data.update(overrides)
        project = Project(**data)
        db.session.add(project)
        db.session.commit()
        return project

    def create_skill(self, resume_id, overrides=None):
        """
        Helper method to create a Skill instance and associate it with a ResumeData.
        """
        data = self.skill_template.copy()
        if overrides:
            data.update(overrides)
        skill = Skill(**data)
        db.session.add(skill)
        db.session.commit()

        resume = ResumeData.query.get(resume_id)
        resume.skills.append(skill)
        db.session.commit()
        return skill

    def create_course(self, resume_id, overrides=None):
        """
        Helper method to create a Course instance and associate it with a ResumeData.
        """
        data = self.course_template.copy()
        if overrides:
            data.update(overrides)
        course = Course(**data)
        db.session.add(course)
        db.session.commit()

        resume = ResumeData.query.get(resume_id)
        resume.courses.append(course)
        db.session.commit()
        return course

    def assert_dict_contains_subset(self, subset, dictionary, msg=None):
        """
        Recursively check whether `dictionary` contains the `subset`.
        This method supports deep comparison of nested dictionaries and lists.
        """
        for key, expected_value in subset.items():
            self.assertIn(key, dictionary, msg=msg)
            actual_value = dictionary[key]

            if isinstance(expected_value, dict) and isinstance(actual_value, dict):
                # Dicts
                self.assert_dict_contains_subset(expected_value, actual_value, msg=msg)
            elif isinstance(expected_value, list) and isinstance(actual_value, list):
                # Lists
                self.assertEqual(len(expected_value), len(actual_value), msg=msg)
                for expected_item, actual_item in zip(expected_value, actual_value):
                    if isinstance(expected_item, dict) and isinstance(
                        actual_item, dict
                    ):
                        self.assert_dict_contains_subset(
                            expected_item, actual_item, msg=msg
                        )
                    else:
                        self.assertEqual(expected_item, actual_item, msg=msg)
            else:  # Non-Container
                self.assertEqual(expected_value, actual_value, msg=msg)
