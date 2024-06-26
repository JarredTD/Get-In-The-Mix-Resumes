"""Initial migration.

Revision ID: 5964fd4207d7
Revises:
Create Date: 2024-04-02 15:53:24.344176

"""

from alembic import op
import sqlalchemy as sa
from app.scripts.models import JsonList


# revision identifiers, used by Alembic.
revision = "5964fd4207d7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "course",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skill",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_user_username"), ["username"], unique=True)

    op.create_table(
        "resume_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("github_link", sa.String(length=255), nullable=True),
        sa.Column("linkedin_link", sa.String(length=255), nullable=True),
        sa.Column("entry_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("resume_data", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_resume_data_entry_date"), ["entry_date"], unique=False
        )

    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("school", sa.String(length=255), nullable=False),
        sa.Column("major", sa.String(length=255), nullable=False),
        sa.Column("minor", sa.String(length=255), nullable=True),
        sa.Column("grad_year", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "experience",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("bullet_points", JsonList(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "extracurricular",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("bullet_points", JsonList(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("language_stack", sa.String(length=255), nullable=False),
        sa.Column("bullet_points", JsonList(), nullable=True),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "resume_courses",
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.PrimaryKeyConstraint("resume_id", "course_id"),
    )
    op.create_table(
        "resume_skills",
        sa.Column("resume_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resume_data.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skill.id"],
        ),
        sa.PrimaryKeyConstraint("resume_id", "skill_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("resume_skills")
    op.drop_table("resume_courses")
    op.drop_table("project")
    op.drop_table("extracurricular")
    op.drop_table("experience")
    op.drop_table("education")
    with op.batch_alter_table("resume_data", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_resume_data_entry_date"))

    op.drop_table("resume_data")
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_user_username"))

    op.drop_table("user")
    op.drop_table("skill")
    op.drop_table("course")
    # ### end Alembic commands ###
