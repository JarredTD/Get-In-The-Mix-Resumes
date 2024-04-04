"""Controller for the flask app"""

from typing import List, Union
from urllib.parse import urlparse, urljoin

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.wrappers import Response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app import db
from .forms import LoginForm, RegistrationForm
from .models import ResumeData, User


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
    ids = (
        ResumeData.query.with_entities(ResumeData.id)
        .filter_by(user_id=current_user.id)
        .order_by(ResumeData.entry_date)
        .all()
    )
    id_list: List[int] = [id[0] for id in ids]  # pragma: no cover
    return jsonify(id_list)


@controllers_bp.route("/load-resume", methods=["POST"])
@login_required
def load_resume() -> Union[Response, tuple]:
    """
    Queries for a specific resume in the ResumeData table

    :returns: A json of the resume data for the found resume
            or an error for invalid request or resume not found
    :rtype: Json object
    """
    resume_request = request.get_json()
    resume_id = resume_request.get("id")

    if resume_id is None:
        return jsonify({"error": "Missing ID"}), 400

    resume = (
        ResumeData.query.filter_by(user_id=current_user.id)
        .filter_by(id=resume_id)
        .first()
    )

    if resume is None:
        return jsonify({"error": "No Resume Found"}), 404

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
