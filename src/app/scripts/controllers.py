"""Controller for the flask app"""

from typing import List, Union
from urllib.parse import urlparse, urljoin
from datetime import datetime

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    send_file,
)
from flask.wrappers import Response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app import db
from .forms import LoginForm, RegistrationForm, ResumeForm
from .models import (
    ResumeData,
    Experience,
    Education,
    Project,
    Skill,
    Course,
    Extracurricular,
    User,
)
from .util.gen_resume import generate_resume


controllers_bp = Blueprint("controllers_bp", __name__)


@controllers_bp.route("/test-db", methods=["GET"])
def test_db() -> str:
    """
    Sanity Check that db is connected

    :returns: Message that db is connected
    :rtype: str
    """
    ResumeData.query.first()

    return "Database is connected."


@controllers_bp.route("/load-resume-ids", methods=["GET"])
@login_required
def load_resume_ids() -> Response:
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


@controllers_bp.route("/load-resume/<int:resume_id>", methods=["GET"])
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


@controllers_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for handling the login process. This function processes both GET
    and POST requests.On GET, it displays the login form. On POST,
    it validates the form and logs the user in if the credentials are correct.

    :return: Redirects to the next page if login is successful and the next URL
             is safe. Otherwise, renders the login template again with a message
             for invalid credentials or displays the login form.
    """
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_url = request.args.get("next")

            if not url_has_allowed_host_and_scheme(next_url, request.host):
                return abort(400)
            return redirect(url_for("views_bp.index"))
        flash("Invalid Credentials")

    return render_template("login.html", form=form)


@controllers_bp.route("/logout")
def logout():
    """
    Route to handle the logout process. It logs out the current user.

    :return: Redirects to the login page.
    """
    logout_user()
    return redirect(url_for("controllers_bp.login"))


@controllers_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for handling user registration. On GET, displays the registration form.
    On POST, it processes the form and creates a new user with the provided
    credentials.

    :return: Redirects to the login page on successful registration, otherwise renders
             the registration form again with error messages.
    """
    form = RegistrationForm()
    if form.is_submitted():
        if form.validate():
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("controllers_bp.login"))
        flash("Registration Not Successful")

    return render_template("register.html", form=form)


@controllers_bp.route("/delete-resume/<int:resume_id>", methods=["DELETE"])
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


@controllers_bp.route("/export-resume/<int:resume_id>", methods=["GET"])
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


@controllers_bp.route("/save-resume", methods=["POST"])
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


def url_has_allowed_host_and_scheme(target, base_host, require_https=False):
    """
    Checks if the provided URL has an allowed host and scheme.

    :param target: The target URL to validate.
    :param base_host: The base host to compare against.
    :param require_https: Boolean indicating if HTTPS is required.
    :return: True if the scheme and host of the target URL are allowed,
            False otherwise.
    """
    full_url = urljoin(request.host_url, target)
    parsed_url = urlparse(full_url)

    is_scheme_allowed = (
        parsed_url.scheme in ("https",)
        if require_https
        else parsed_url.scheme in ("http", "https")
    )
    is_host_allowed = parsed_url.netloc == base_host

    return is_scheme_allowed and is_host_allowed
