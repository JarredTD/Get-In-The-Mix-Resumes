"""Sanity check on db operations"""

# pylint: disable=no-name-in-module

from app import db
from app.scripts.models import ResumeData
from tests import BaseTestCase


class ResumeDataModelTestCase(BaseTestCase):
    """Test the ResumeData model operations."""

    def test_resume_data_creation(self):
        """Sanity check on adding a ResumeData record."""
        self.create_resume_data()

        created = ResumeData.query.filter_by(
            email=self.complete_resume_template["email"]
        ).first()
        self.assertIsNotNone(created, "ResumeData instance should have been created.")

        expected_dict = self.complete_resume_template.copy()
        expected_dict["id"] = created.id
        expected_dict["entry_date"] = (
            created.entry_date.isoformat()
        )  # Format datetime for comparison

        self.assert_dict_contains_subset(
            expected_dict, created.to_dict(), "Created data does not match template."
        )

    def test_resume_data_retrieval(self):
        """Sanity check on retrieving a ResumeData record."""
        created = self.create_resume_data()

        retrieved = ResumeData.query.get(created.id)
        self.assertIsNotNone(retrieved, "Failed to retrieve the ResumeData record.")

        expected_dict = self.complete_resume_template.copy()
        expected_dict["id"] = retrieved.id
        expected_dict["entry_date"] = retrieved.entry_date.isoformat()

        self.assert_dict_contains_subset(
            expected_dict,
            retrieved.to_dict(),
            "Retrieved data does not match template.",
        )

    def test_resume_data_update(self):
        """Sanity check on updating a ResumeData record."""
        created_resume = self.create_resume_data()

        updated_first_name = "Updated"
        created_resume.first_name = updated_first_name
        db.session.commit()

        updated = ResumeData.query.get(created_resume.id)
        updated_dict = updated.to_dict()
        self.assertEqual(
            updated_dict["first_name"],
            updated_first_name,
            "ResumeData first name was not updated correctly.",
        )

    def test_resume_data_deletion(self):
        """Sanity check on deleting a ResumeData record."""
        resume_to_delete = self.create_resume_data()

        db.session.delete(resume_to_delete)
        db.session.commit()

        deleted = ResumeData.query.get(resume_to_delete.id)
        self.assertIsNone(deleted, "ResumeData record was not deleted.")
