"""
Base class that other test classes inherit from.
Constants for tests.
"""

# pylint: disable=no-name-in-module

import unittest
from app import create_app, db
from app.config import TestingConfig
from app.scripts.models import User

TEST_USERNAME = "testuser"
TEST_PASSWORD = "test"
LOGIN_ROUTE = "/login"
REGISTER_ROUTE = "/register"
LOGOUT_ROUTE = "/logout"


class BaseTestCase(unittest.TestCase):
    """A base test case that sets up the application and database for testing."""

    def setUp(self):
        """Prepare the test client and database for the Flask application."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.testuser = User(username=TEST_USERNAME)
        self.testuser.set_password(TEST_PASSWORD)
        db.session.add(self.testuser)
        db.session.commit()

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
