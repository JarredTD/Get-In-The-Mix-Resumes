"""Sanity check on db operations"""

# pylint: disable=no-name-in-module

from app import db
from app.scripts.models import ResumeData
from tests import BaseTestCase

JANE_DOE_FIRST_NAME = "Jane"
JANE_DOE_LAST_NAME = "Doe"
JOHN_SMITH_FIRST_NAME = "John"
JOHN_SMITH_LAST_NAME = "Smith"
ALICE_FIRST_NAME = "Alice"
ALICE_LAST_NAME = "Wonderland"
ALICIA_FIRST_NAME = "Alicia"
BOB_FIRST_NAME = "Bob"
BOB_LAST_NAME = "Builder"


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
