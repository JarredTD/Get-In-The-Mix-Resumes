"""Test authentication process"""

# pylint: disable=no-name-in-module

from app.scripts.models import User
from tests import BaseTestCase

NEW_USER_USERNAME = "newuser"
NEW_USER_PASSWORD = "123456"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "test"
WRONG_PASSWORD = "wrongpassword"
LOGIN = "Login"
HOME = "Home"
REGISTER = "Register"
INVALID_CREDENTIALS = "Invalid Credentials"


class UserAuthenticationTestCase(BaseTestCase):
    """Test authentication routes."""

    def test_user_registration(self):
        """Test user can register successfully."""
        response = self.register(
            NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.query.filter_by(username=NEW_USER_USERNAME).first())

    def test_user_login_with_next_parameter(self):
        """
        Test registered user can login and is redirected according
        to 'next' parameter.
        """
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)

        next_url = "ht://d"  # Invalid next

        login_url = f"/login?next={next_url}"
        response = self.client.post(
            login_url,
            data={"username": NEW_USER_USERNAME, "password": NEW_USER_PASSWORD},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 400, "Expected abort")

    def test_user_login(self):
        """Test registered user can login."""
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        response = self.login(NEW_USER_USERNAME, NEW_USER_PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertIn(HOME, response.data.decode())

    def test_user_logout(self):
        """Test logged in user can logout."""
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(LOGIN, response.data.decode())

    def test_incorrect_login(self):
        """Test user cannot login with incorrect credentials."""
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        response = self.login(NEW_USER_USERNAME, WRONG_PASSWORD)
        self.assertIn(INVALID_CREDENTIALS, response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_duplicate_registration(self):
        """Test that duplicate user registration is not allowed."""
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        response = self.register(
            NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD
        )
        self.assertIn(REGISTER, response.data.decode())
        self.assertEqual(response.status_code, 200)
