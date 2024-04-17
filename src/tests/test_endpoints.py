"""Tests endpoints for ResumeData"""

# pylint: disable=no-name-in-module

from app.scripts import models
from tests import BaseTestCase

NEW_USER_USERNAME = "newuser"
NEW_USER_PASSWORD = "123456"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "test"
LOAD_RESUME_IDS_ROUTE = "resumes/load-resume-ids"
LOAD_RESUME_ROUTE = "resumes/load-resume"
JSON = "application/json"
EXPORT = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class ResumeEndpointTestCase(BaseTestCase):
    """Test the endpoints related to ResumeData."""

    def test_load_resume_ids(self):
        """Test load_resume_ids endpoint."""
        self.create_resume_data()
        self.create_resume_data()
        self.login(TEST_USERNAME, TEST_PASSWORD)

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
        self.login(TEST_USERNAME, TEST_PASSWORD)

        response = self.client.get(
            f"{LOAD_RESUME_ROUTE}/{resume.id}",
            content_type=JSON,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(JSON, response.content_type)

        expected_resume = resume.to_dict()
        actual_response = response.get_json()
        for key, value in expected_resume.items():
            self.assertEqual(
                actual_response.get(key),
                value,
                f"Resume data for {key} does not match.",
            )

    def test_load_resume_not_found(self):
        """Test load_resume with resume not found."""
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.get(
            f"{LOAD_RESUME_ROUTE}/999",
            content_type=JSON,
        )
        self.assertEqual(response.status_code, 404)

    def test_load_resume_wrong_user(self):
        """Test load_resume with resume not accessible by the logged-in user."""
        resume = self.create_resume_data()
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        self.login(NEW_USER_USERNAME, NEW_USER_PASSWORD)

        response = self.client.get(
            f"{LOAD_RESUME_ROUTE}/{resume.id}",
            content_type=JSON,
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_resume_success(self):
        """Test successful resume deletion"""
        resume = self.create_resume_data()
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.delete(f"resumes/delete-resume/{resume.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Resume deleted successfully")

    def test_delete_resume_not_found(self):
        """Test delete attempt on non-existing resume"""
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.delete("/delete-resume/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_resume_unauthorized(self):
        """Test delete attempt w/ wrong user"""
        resume = self.create_resume_data()
        self.register(NEW_USER_USERNAME, NEW_USER_PASSWORD, NEW_USER_PASSWORD)
        self.login(NEW_USER_USERNAME, NEW_USER_PASSWORD)
        response = self.client.delete(f"resumes/delete-resume/{resume.id}")
        self.assertEqual(response.status_code, 404)
        self.assertIn(
            "Resume not found or not authorized to delete", response.data.decode()
        )

    def test_export_resume_success(self):
        """Test successful export attempt"""
        resume = self.create_resume_data()
        self.create_experience(resume.id)
        self.create_education(resume.id)
        self.create_extracurricular(resume.id)
        self.create_project(resume.id)
        self.create_skill(resume.id)
        self.create_course(resume.id)

        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.get(f"resumes/export-resume/{resume.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content_type.startswith(EXPORT))

    def test_export_resume_not_found(self):
        """Test export attempt w/ resume not found"""
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.get("resumes/export-resume/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Error: No resume found with ID 999", response.data.decode())

    def test_save_resume_validation_error(self):
        """Test validation error w/ save attempt"""
        self.login(TEST_USERNAME, TEST_PASSWORD)
        response = self.client.post("resumes/save-resume", data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Error: Form validation failed. Check console for details.",
            response.data.decode(),
        )

    def test_save_resume_success(self):
        """Test successful saving of a resume"""
        self.login(TEST_USERNAME, TEST_PASSWORD)

        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "github_link": "http://github.com/johndoe",
            "linkedin_link": "http://linkedin.com/in/johndoe",
            "experiences-0-company_name": "Test Company",
            "experiences-0-title": "Developer",
            "experiences-0-start_date": "2022-01-01",
            "experiences-0-end_date": "2023-01-01",
            "educations-0-school": "Test University",
            "educations-0-major": "Computer Science",
            "educations-0-grad_year": "2024",
            "extracurriculars-0-name": "Debate Club",
            "extracurriculars-0-title": "President",
            "extracurriculars-0-bullet_points": "Led team to national championships",
            "projects-0-name": "Personal Website",
            "projects-0-language_stack": "HTML, CSS, JavaScript",
            "projects-0-bullet_points": "Developed personal portfolio",
            "skills-0-name": "Python",
            "courses-0-name": "Advanced Python Programming",
        }

        response = self.client.post("/resumes/save-resume", data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/"))

        # Verify the resume was created with the expected data
        resume = models.ResumeData.query.filter_by(email="john.doe@example.com").first()
        self.assertIsNotNone(resume)
        self.assertEqual(resume.first_name, "John")
        self.assertEqual(resume.last_name, "Doe")
        self.assertEqual(resume.phone_number, "1234567890")
        self.assertEqual(resume.github_link, "http://github.com/johndoe")
        self.assertEqual(resume.linkedin_link, "http://linkedin.com/in/johndoe")

        skills = [skill.name for skill in resume.skills]
        courses = [course.name for course in resume.courses]
        self.assertIn("Python", skills)
        self.assertIn("Advanced Python Programming", courses)

        self.assertEqual(resume.experiences[0].company_name, "Test Company")
        self.assertEqual(resume.educations[0].school, "Test University")
        self.assertEqual(resume.extracurriculars[0].name, "Debate Club")
        self.assertEqual(resume.projects[0].name, "Personal Website")
