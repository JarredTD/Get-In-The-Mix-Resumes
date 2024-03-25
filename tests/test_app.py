"""Unit tests for the Flask application defined in app.py."""

# pylint: disable=import-error
# pylint: disable=no-name-in-module

import unittest
from app import create_app, db
from app.config import TestingConfig


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


if __name__ == "__main__":
    unittest.main()
