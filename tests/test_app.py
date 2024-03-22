"""Unit tests for app.py"""

# pylint: disable=import-error
# pylint: disable=no-name-in-module

import unittest
from app.app import app


class FlaskTestCase(unittest.TestCase):
    """Test suite for app"""

    def setUp(self):
        """Creates test client of app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """Test index page routing"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_about_us(self):
        """Test about us page routing"""
        response = self.app.get("/about-us")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)

    def test_motivation(self):
        """Test project motivation page routing"""
        response = self.app.get("/project-motivation")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)


if __name__ == "__main__":
    unittest.main()
