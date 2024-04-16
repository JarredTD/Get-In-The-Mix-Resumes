"""Tests app routes"""

# pylint: disable=no-name-in-module

from tests import BaseTestCase

TEST_USERNAME = "testuser"
TEST_PASSWORD = "test"
HOME = "Resume Form"
INDEX_ROUTE = "/"
ABOUT_US_CHECK = "All About Me"
ABOUT_US_ROUTE = "/about-us"
PROJECT_MOTIVATION_ROUTE = "/project-motivation"
PROJECT_MOTIVATION = "Project Motivation"
TEST_DB_ROUTE = "db/test-db"
DB_CONNECTED = "Database is connected"
LOGIN_ROUTE = "auth/login"
LOGIN = "Login"
REGISTER_ROUTE = "auth/register"
REGISTER = "Register"


class FlaskRoutingTestCase(BaseTestCase):
    """Test the routing and responses of the Flask application."""

    def test_index_route(self):
        """Test the index page route after logging in."""
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.get(INDEX_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(HOME, response.data.decode())

    def test_about_us_route(self):
        """Test the about us page route."""
        response = self.client.get(ABOUT_US_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(ABOUT_US_CHECK, response.data.decode())

    def test_project_motivation_route(self):
        """Test the project motivation page route."""
        response = self.client.get(PROJECT_MOTIVATION_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(PROJECT_MOTIVATION, response.data.decode())

    def test_db_route(self):
        """Test the test-db route."""
        response = self.client.get(TEST_DB_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(DB_CONNECTED, response.data.decode())

    def test_login_route(self):
        """Test the test-db route."""
        response = self.client.get(LOGIN_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(LOGIN, response.data.decode())

    def test_register_route(self):
        """Test the test-db route."""
        response = self.client.get(REGISTER_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(REGISTER, response.data.decode())
