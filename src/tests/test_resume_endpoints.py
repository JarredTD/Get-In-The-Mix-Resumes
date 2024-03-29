"""Tests endpoints for ResumeData"""

# pylint: disable=no-name-in-module

import json
from app import db
from app.scripts.models import ResumeData
from tests import BaseTestCase

JANE_DOE_FIRST_NAME = "Jane"
JANE_DOE_LAST_NAME = "Doe"
JOHN_SMITH_FIRST_NAME = "John"
JOHN_SMITH_LAST_NAME = "Smith"
LOAD_RESUME_IDS_ROUTE = "/load-resume-ids"
LOAD_RESUME_ROUTE = "/load-resume"
JSON = "application/json"


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
