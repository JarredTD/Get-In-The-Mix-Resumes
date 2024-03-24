"""Unit tests for the Flask application defined in app.py."""

# pylint: disable=import-error
# pylint: disable=no-name-in-module

import unittest
from app import app


class FlaskTestCase(unittest.TestCase):
    """
    A collection of unit tests for the Flask application.

    This suite tests the routing and responses for various pages within the application.
    """

    def setUp(self) -> None:
        """
        Prepare the test client for the Flask application.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self) -> None:
        """
        Verify that the index page returns a status code of 200
        and the content type is HTML.
        """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_about_us(self) -> None:
        """
        Ensure the 'About Us' page is accessible and returns HTML content.
        """
        response = self.app.get("/about-us")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_motivation(self) -> None:
        """
        Test that the 'Project Motivation' page is routed correctly and serves HTML.
        """
        response = self.app.get("/project-motivation")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)
