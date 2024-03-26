"""Unit tests for the Flask application defined in app.py."""

# pylint: disable=import-error
# pylint: disable=no-name-in-module
import pytest
import unittest
from app import create_app, db
from app.config import TestingConfig
from app.scripts.models import ResumeData


class FlaskTestCase(unittest.TestCase):
    """
    A collection of unit tests for the Flask application.

    This suite tests the routing, responses,
    and database interactions within the application.
    """

    def setUp(self):
        """
        Prepare the test client and database for the Flask application.
        """
        # Use the application factory to create a test app with TestingConfig
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

    def test_index_route(self):
        """
        Verify that the index page returns a status code of 200
        and the content type is HTML.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_about_us_route(self):
        """
        Ensure the 'About Us' page is accessible and returns HTML content.
        """
        response = self.client.get("/about-us")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_motivation_route(self):
        """
        Test that the 'Project Motivation' page is routed correctly and serves HTML.
        """
        response = self.client.get("/project-motivation")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_resume_data_creation(self):
        """
        Test the creation of a ResumeData instance.
        """
        resume = ResumeData(first_name="Jane", last_name="Doe")
        db.session.add(resume)
        db.session.commit()

        created = ResumeData.query.filter_by(first_name="Jane").first()
        self.assertIsNotNone(created)
        self.assertEqual(created.first_name, "Jane")
        self.assertEqual(created.last_name, "Doe")

    def test_resume_data_retrieval(self):
        """
        Test the retrieval of a ResumeData instance.
        """
        resume = ResumeData(first_name="John", last_name="Smith")
        db.session.add(resume)
        db.session.commit()

        retrieved = ResumeData.query.filter_by(first_name="John").first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, "John")
        self.assertEqual(retrieved.last_name, "Smith")

    def test_resume_data_update(self):
        """
        Test the updating of a ResumeData instance.
        """
        resume = ResumeData(first_name="Alice", last_name="Wonderland")
        db.session.add(resume)
        db.session.commit()

        # Retrieve and update
        to_update = ResumeData.query.filter_by(first_name="Alice").first()
        to_update.first_name = "Alicia"
        db.session.commit()

        updated = ResumeData.query.filter_by(id=to_update.id).first()
        self.assertEqual(updated.first_name, "Alicia")

    def test_resume_data_deletion(self):
        """
        Test the deletion of a ResumeData instance.
        """
        resume = ResumeData(first_name="Bob", last_name="Builder")
        db.session.add(resume)
        db.session.commit()

        # Retrieve and delete
        to_delete = ResumeData.query.filter_by(first_name="Bob").first()
        db.session.delete(to_delete)
        db.session.commit()

        deleted = ResumeData.query.filter_by(id=to_delete.id).first()
        self.assertIsNone(deleted)


if __name__ == "__main__":
    unittest.main()
