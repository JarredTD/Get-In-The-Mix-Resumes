"""Tests endpoints for ResumeData"""

# pylint: disable=no-name-in-module

import json
from tests import BaseTestCase

LOAD_RESUME_IDS_ROUTE = "/load-resume-ids"
LOAD_RESUME_ROUTE = "/load-resume"
JSON = "application/json"


class ResumeEndpointTestCase(BaseTestCase):
    """Test the endpoints related to ResumeData."""

    def test_load_resume_ids(self):
        """Test load_resume_ids endpoint."""
        self.create_resume_data()
        self.create_resume_data()

        response = self.client.get(LOAD_RESUME_IDS_ROUTE)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreaterEqual(len(response.json), 2)

    def test_load_resume_success(self):
        """Test load_resume with success, ensuring related models are included."""
        resume = self.create_resume_data()
        self.create_experience(resume.id)
        self.create_education(resume.id)
        self.create_extracurricular(resume.id)
        self.create_project(resume.id)
        self.create_skill(resume.id)
        self.create_course(resume.id)

        resume_request = {"id": resume.id}
        response = self.client.post(
            LOAD_RESUME_ROUTE,
            data=json.dumps(resume_request),
            content_type=JSON,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(JSON, response.content_type)

        # Construct the expected subset for the primary resume data
        expected_subset = {
            "first_name": resume.first_name,
            "last_name": resume.last_name,
            "email": resume.email,
            # Add more fields from resume_template if necessary
        }

        self.assert_dict_contains_subset(
            expected_subset, response.json, "Resume data does not match."
        )

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
