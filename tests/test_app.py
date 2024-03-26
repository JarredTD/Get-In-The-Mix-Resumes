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

    def test_load_resume_ids(self):
        """
        Test usage of the load_resume_ids endpoint.
        """
        john = ResumeData(id=0, first_name="John", last_name="Smith")
        alice = ResumeData(id=1, first_name="Alice", last_name="Land")
        jane = ResumeData(id=2, first_name="Jane", last_name="Mary")

        db.session.add(john)
        db.session.add(alice)
        db.session.add(jane)
        db.session.commit()

        resume_ids = self.client.get("/load-resume-ids").json

        for i in range(0, 3):
            self.assertEqual(resume_ids[i], i)

    def test_load_resume_success(self):
        """
        Test usage of the load_resume endpoint on success
        """

        resume_request = {
            "id": 0,
        }

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
        """
        Test usage of the load_resume endpoint on failure due to bad request
        """

        resume_request = {
            "name": "john",
        }

        john = ResumeData(id=0, first_name="John", last_name="Smith")
        db.session.add(john)
        db.session.commit()

        resume = self.client.post(
            "/load-resume",
            data=json.dumps(resume_request),
            content_type="application/json",
        )

        self.assertEqual(resume.status_code, 400)
        self.assertIn("application/json", resume.content_type)

    def test_load_resume_not_found(self):
        """
        Test usage of the load_resume endpoint on failure due to resume not found
        """

        resume_request = {
            "id": "0",
        }

        resume = self.client.post(
            "/load-resume",
            data=json.dumps(resume_request),
            content_type="application/json",
        )

        self.assertEqual(resume.status_code, 404)
        self.assertIn("application/json", resume.content_type)


if __name__ == "__main__":
    unittest.main()
