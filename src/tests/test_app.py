"""Unit tests for the Flask application defined in app.py."""

# pylint: disable=import-error, no-name-in-module, unused-import
import unittest
import json
from app import create_app, db
from app.config import TestingConfig
from app.scripts.models import ResumeData, User

# Constants for user credentials and test data
TEST_USERNAME = "testuser"
TEST_PASSWORD = "test"
NEW_USER_USERNAME = "newuser"
NEW_USER_PASSWORD = "123456"
CONFIRM_PASSWORD = "123456"
WRONG_PASSWORD = "wrongpassword"
JANE_DOE_FIRST_NAME = "Jane"
JANE_DOE_LAST_NAME = "Doe"
JOHN_SMITH_FIRST_NAME = "John"
JOHN_SMITH_LAST_NAME = "Smith"
ALICE_FIRST_NAME = "Alice"
ALICE_LAST_NAME = "Wonderland"
ALICIA_FIRST_NAME = "Alicia"
BOB_FIRST_NAME = "Bob"
BOB_LAST_NAME = "Builder"
HOME = "Home"
ABOUT_US = "About Us"
PROJECT_MOTIVATION = "Project Motivation"
LOGIN = "Login"
REGISTER = "Register"
INVALID_CREDENTIALS = "Invalid Credentials"
JSON = "application/json"
DB_CONNECTED = "Database is connected"

# Constants for routes
LOGIN_ROUTE = "/login"
REGISTER_ROUTE = "/register"
LOGOUT_ROUTE = "/logout"
ABOUT_US_ROUTE = "/about-us"
PROJECT_MOTIVATION_ROUTE = "/project-motivation"
TEST_DB_ROUTE = "/test-db"
LOAD_RESUME_IDS_ROUTE = "/load-resume-ids"
LOAD_RESUME_ROUTE = "/load-resume"


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

    def login(self, username, password):
        """Helper method to log in as a user."""
        return self.client.post(
            LOGIN_ROUTE,
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    def register(self, username, password, confirm_password):
        """Helper method to register a new user."""
        return self.client.post(
            REGISTER_ROUTE,
            data={
                "username": username,
                "password": password,
                "confirm_password": confirm_password,
            },
            follow_redirects=True,
        )

    def logout(self):
        """Helper method to log out a user."""
        return self.client.get(LOGOUT_ROUTE, follow_redirects=True)


class FlaskRoutingTestCase(BaseTestCase):
    """Test the routing and responses of the Flask application."""

    def test_index_route(self):
        """Test the index page route after logging in."""
        response = self.login(TEST_USERNAME, TEST_PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertIn(HOME, response.data.decode())

    def test_about_us_route(self):
        """Test the about us page route."""
        response = self.client.get(ABOUT_US_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertIn(ABOUT_US, response.data.decode())

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


class ResumeDataModelTestCase(BaseTestCase):
    """Test the ResumeData model operations."""

    def test_resume_data_creation(self):
        """Sanity check on adding a record."""
        resume = ResumeData(
            user_id=self.testuser.id,
            first_name=JANE_DOE_FIRST_NAME,
            last_name=JANE_DOE_LAST_NAME,
        )
        db.session.add(resume)
        db.session.commit()

        created = ResumeData.query.filter_by(first_name=JANE_DOE_FIRST_NAME).first()
        self.assertIsNotNone(created)
        self.assertEqual(created.first_name, JANE_DOE_FIRST_NAME)
        self.assertEqual(created.last_name, JANE_DOE_LAST_NAME)

    def test_resume_data_retrieval(self):
        """Sanity check on retrieving a record."""
        resume = ResumeData(
            user_id=self.testuser.id,
            first_name=JOHN_SMITH_FIRST_NAME,
            last_name=JOHN_SMITH_LAST_NAME,
        )
        db.session.add(resume)
        db.session.commit()

        retrieved = ResumeData.query.filter_by(first_name=JOHN_SMITH_FIRST_NAME).first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.first_name, JOHN_SMITH_FIRST_NAME)
        self.assertEqual(retrieved.last_name, JOHN_SMITH_LAST_NAME)

    def test_resume_data_update(self):
        """Sanity check on updating a record."""
        resume = ResumeData(
            user_id=self.testuser.id,
            first_name=ALICE_FIRST_NAME,
            last_name=ALICE_LAST_NAME,
        )
        db.session.add(resume)
        db.session.commit()

        to_update = ResumeData.query.filter_by(first_name=ALICE_FIRST_NAME).first()
        to_update.first_name = ALICIA_FIRST_NAME
        db.session.commit()

        updated = ResumeData.query.filter_by(id=to_update.id).first()
        self.assertEqual(updated.first_name, ALICIA_FIRST_NAME)

    def test_resume_data_deletion(self):
        """Sanity check on deleting a record."""
        resume = ResumeData(
            user_id=self.testuser.id, first_name=BOB_FIRST_NAME, last_name=BOB_LAST_NAME
        )
        db.session.add(resume)
        db.session.commit()

        to_delete = ResumeData.query.filter_by(first_name=BOB_FIRST_NAME).first()
        db.session.delete(to_delete)
        db.session.commit()

        deleted = ResumeData.query.filter_by(id=to_delete.id).first()
        self.assertIsNone(deleted)


class ResumeEndpointTestCase(BaseTestCase):
    """Test the endpoints related to ResumeData."""

    def test_load_resume_ids(self):
        """Test load_resume_ids endpoint."""
        resumes = [
            ResumeData(
                user_id=self.testuser.id,
                first_name=JANE_DOE_FIRST_NAME,
                last_name=JANE_DOE_LAST_NAME,
            ),
            ResumeData(
                user_id=self.testuser.id,
                first_name=JOHN_SMITH_FIRST_NAME,
                last_name=JOHN_SMITH_LAST_NAME,
            ),
        ]
        db.session.add_all(resumes)
        db.session.commit()

        response = self.client.get(LOAD_RESUME_IDS_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreaterEqual(len(response.json), 2)

    def test_load_resume_success(self):
        """Test load_resume with success."""
        resume = ResumeData(
            user_id=self.testuser.id,
            first_name=JOHN_SMITH_FIRST_NAME,
            last_name=JOHN_SMITH_LAST_NAME,
        )
        db.session.add(resume)
        db.session.commit()

        resume_request = {"id": resume.id}
        response = self.client.post(
            LOAD_RESUME_ROUTE,
            data=json.dumps(resume_request),
            content_type=JSON,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(JSON, response.content_type)
        self.assertEqual(response.json["first_name"], JOHN_SMITH_FIRST_NAME)
        self.assertEqual(response.json["last_name"], JOHN_SMITH_LAST_NAME)

    def test_load_resume_bad_request(self):
        """Test load_resume with bad request."""
        resume_request = {"name": "john"}
        response = self.client.post(
            LOAD_RESUME_ROUTE,
            data=json.dumps(resume_request),
            content_type=JSON,
        )
        self.assertEqual(response.status_code, 400)

    def test_load_resume_not_found(self):
        """Test load_resume with resume not found."""
        resume_request = {"id": 999}
        response = self.client.post(
            LOAD_RESUME_ROUTE,
            data=json.dumps(resume_request),
            content_type=JSON,
        )
        self.assertEqual(response.status_code, 404)


class UserAuthenticationTestCase(BaseTestCase):
    """Test authentication routes."""

    def test_user_registration(self):
        """Test user can register successfully."""
        response = self.register(
            NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.query.filter_by(username=NEW_USER_USERNAME).first())

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


if __name__ == "__main__":
    unittest.main()
