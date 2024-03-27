"""Unit tests for the Flask application defined in app.py."""

# Disabled for false-positives
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=unused-import

import unittest
import json
import pytest
from app import create_app, db
from app.config import TestingConfig
from app.scripts.models import ResumeData
from app.scripts.controllers import load_resume_ids, load_resume


class BaseTestCase(unittest.TestCase):
    """
    A base test case that sets up the application and database for testing.
    """

    def setUp(self):
        """
        Prepare the test client and database for the Flask application.
        """
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Create all database tables
        db.create_all()

    def tearDown(self):
        """
        Clean up after each test case.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class FlaskRoutingTestCase(BaseTestCase):
    """
    Test the routing and responses of the Flask application.
    """

    def test_index_route(self):
        """Test the index page route"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_about_us_route(self):
        """Test the about us page route"""
        response = self.client.get("/about-us")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_motivation_route(self):
        """Test the project motivation page route"""
        response = self.client.get("/project-motivation")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_db_route(self):
        """Test test-db route"""
        response = self.client.get("/test-db")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)


class ResumeDataModelTestCase(BaseTestCase):
    """
    Test the ResumeData model operations.
    """

    def test_resume_data_creation(self):
        """Sanity check on add record"""
        resume = ResumeData(first_name="Jane", last_name="Doe")
        db.session.add(resume)
        db.session.commit()

        created = ResumeData.query.filter_by(first_name="Jane").first()
        self.assertIsNotNone(created)
        self.assertEqual(created.first_name, "Jane")
        self.assertEqual(created.last_name, "Doe")

    def test_resume_data_retrieval(self):
        """Sanity check on getting record"""
        resume = ResumeData(first_name="John", last_name="Smith")
        db.session.add(resume)
        db.session.commit()

        retrieved = ResumeData.query.filter_by(first_name="John").first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, "John")
        self.assertEqual(retrieved.last_name, "Smith")

    def test_resume_data_update(self):
        """Sanity check on updating record"""
        resume = ResumeData(first_name="Alice", last_name="Wonderland")
        db.session.add(resume)
        db.session.commit()

        to_update = ResumeData.query.filter_by(first_name="Alice").first()
        to_update.first_name = "Alicia"
        db.session.commit()

        updated = ResumeData.query.filter_by(id=to_update.id).first()
        self.assertEqual(updated.first_name, "Alicia")

    def test_resume_data_deletion(self):
        """Sanity check on deleting record"""
        resume = ResumeData(first_name="Bob", last_name="Builder")
        db.session.add(resume)
        db.session.commit()

        to_delete = ResumeData.query.filter_by(first_name="Bob").first()
        db.session.delete(to_delete)
        db.session.commit()

        deleted = ResumeData.query.filter_by(id=to_delete.id).first()
        self.assertIsNone(deleted)


class ResumeEndpointTestCase(BaseTestCase):
    """
    Test the endpoints related to ResumeData.
    """

    def test_load_resume_ids(self):
        """Test load_resume_ids enpoint"""
        john = ResumeData(id=0, first_name="John", last_name="Smith")
        alice = ResumeData(id=1, first_name="Alice", last_name="Land")
        jane = ResumeData(id=2, first_name="Jane", last_name="Mary")
        db.session.add_all([john, alice, jane])
        db.session.commit()

        resume_ids = self.client.get("/load-resume-ids").json
        self.assertEqual(resume_ids, [0, 1, 2])

    def test_load_resume_success(self):
        """Test load_resume w/ success"""
        resume_request = {"id": 0}
        john = ResumeData(id=0, first_name="John", last_name="Smith")
        db.session.add(john)
        db.session.commit()

        resume = self.client.post(
            "/load-resume",
            data=json.dumps(resume_request),
            content_type="application/json",
        )
        resume_data = resume.json

        self.assertEqual(resume.status_code, 200)
        self.assertIn("application/json", resume.content_type)
        self.assertEqual(resume_data["first_name"], "John")
        self.assertEqual(resume_data["id"], 0)
        self.assertEqual(resume_data["last_name"], "Smith")

    def test_load_resume_bad_request(self):
        """Test load_resume w/ bad request"""
        resume_request = {"name": "john"}

        john = ResumeData(id=0, first_name="John", last_name="Smith")
        db.session.add(john)
        db.session.commit()

        resume = self.client.post(
            "/load-resume",
            data=json.dumps(resume_request),
            content_type="application/json",
        )
        self.assertEqual(resume.status_code, 400)

    def test_load_resume_not_found(self):
        """Test load_resume w/ resume not found"""
        resume_request = {"id": 0}

        resume = self.client.post(
            "/load-resume",
            data=json.dumps(resume_request),
            content_type="application/json",
        )
        self.assertEqual(resume.status_code, 404)


if __name__ == "__main__":
    unittest.main()
