from datetime import datetime

from flask import jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user

from . import resumes_bp
from app import db
from ..models import (
    ResumeData,
    Experience,
    Education,
    Project,
    Skill,
    Course,
    Extracurricular,
)
from ..forms import ResumeForm
from ..util.gen_resume import generate_resume


@resumes_bp.route("/load-resume-ids", methods=["GET"])
@login_required
def load_resume_ids():
    """
    Queries all ids found in ResumeData table

    :returns: List of all ids in ResumeData table
    :rtype: List of Ints
    """
    resume_data = (
        ResumeData.query.with_entities(ResumeData.id, ResumeData.entry_date)
        .filter_by(user_id=current_user.id)
        .order_by(ResumeData.entry_date.asc())
        .all()
    )

    resume_list = [
        {"id": id_, "entry_date": entry_date} for id_, entry_date in resume_data
    ]

    return jsonify(resume_list)


@resumes_bp.route("/load-resume/<int:resume_id>", methods=["GET"])
@login_required
def load_resume(resume_id):
    """
    Queries for a specific resume in the ResumeData table using the resume ID.

    :param resume_id: The ID of the resume to fetch.
    :returns: A JSON of the resume data for the found resume or an error for resume not found.
    :rtype: Response
    """
    resume = ResumeData.query.filter_by(user_id=current_user.id, id=resume_id).first()

    if not resume:
        return jsonify({"error": "No Resume Found"}), 404

    print(resume.to_dict())
    return jsonify(resume.to_dict())


@resumes_bp.route("/delete-resume/<int:resume_id>", methods=["DELETE"])
@login_required
def delete_resume(resume_id):
    resume = ResumeData.query.get(resume_id)
    if resume and resume.user_id == current_user.id:
        try:
            Experience.query.filter_by(resume_id=resume_id).delete()
            Education.query.filter_by(resume_id=resume_id).delete()
            Extracurricular.query.filter_by(resume_id=resume_id).delete()
            Project.query.filter_by(resume_id=resume_id).delete()
            resume.skills = []
            resume.courses = []
            db.session.commit()

            db.session.delete(resume)
            db.session.commit()
            return "Resume deleted successfully", 200
        except Exception as e:
            db.session.rollback()
            return f"An error occurred while deleting the resume: {e}", 500
    else:
        return "Resume not found or not authorized to delete", 404


@resumes_bp.route("/export-resume/<int:resume_id>", methods=["GET"])
@login_required
def export_resume(resume_id):
    resume_data = ResumeData.query.get(resume_id)

    if resume_data:
        generate_resume(resume_data)
        return send_file(
            "static/word/resume.docx", as_attachment=True, download_name="resume.docx"
        )
    else:
        return f"Error: No resume found with ID {resume_id}"


@resumes_bp.route("/save-resume", methods=["POST"])
@login_required
def save_resume():
    form = ResumeForm()
    if form.validate_on_submit():
        new_resume = ResumeData(
            user_id=current_user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            github_link=form.github_link.data or None,
            linkedin_link=form.linkedin_link.data or None,
            entry_date=datetime.utcnow(),
        )

        # Handling Experience
        for exp_form in form.experiences.entries:
            bullet_points_list = exp_form.data["bullet_points"].split("\n")
            experience = Experience(
                company_name=exp_form.data["company_name"],
                title=exp_form.data["title"],
                start_date=exp_form.data["start_date"],
                end_date=(
                    exp_form.data["end_date"] if exp_form.data["end_date"] else None
                ),
                bullet_points=bullet_points_list,
            )
            new_resume.experiences.append(experience)

        # Handling Education
        for edu_form in form.educations.entries:
            education = Education(
                school=edu_form.data["school"],
                major=edu_form.data["major"],
                minor=edu_form.data["minor"] if edu_form.data["minor"] else None,
                grad_year=edu_form.data["grad_year"],
            )
            new_resume.educations.append(education)

        # Handling Extracurricular Activities
        for extra_form in form.extracurriculars.entries:
            bullet_points_list = extra_form.data["bullet_points"].split("\n")
            extracurricular = Extracurricular(
                name=extra_form.data["name"],
                title=extra_form.data["title"],
                bullet_points=bullet_points_list,
            )
            new_resume.extracurriculars.append(extracurricular)

        # Handling Projects
        for proj_form in form.projects.entries:
            bullet_points_list = proj_form.data["bullet_points"].split("\n")
            project = Project(
                name=proj_form.data["name"],
                language_stack=proj_form.data["language_stack"],
                bullet_points=bullet_points_list,
            )
            new_resume.projects.append(project)

        # Handling Skills
        for skill_form in form.skills.entries:
            skill = Skill.query.filter_by(name=skill_form.data["name"]).first()
            if not skill:
                skill = Skill(name=skill_form.data["name"])
            new_resume.skills.append(skill)

        # Handling Courses
        for course_form in form.courses.entries:
            course = Course.query.filter_by(name=course_form.data["name"]).first()
            if not course:
                course = Course(name=course_form.data["name"])
            new_resume.courses.append(course)

        db.session.add(new_resume)
        db.session.commit()

        return redirect(url_for("views_bp.index"))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")
        return "Error: Form validation failed. Check console for details."
