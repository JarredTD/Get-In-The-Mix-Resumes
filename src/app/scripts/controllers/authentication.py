"""Endpoints related to authentication"""

from urllib.parse import urlparse, urljoin

from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from app import db
from . import authentication_bp
from ..forms import LoginForm, RegistrationForm
from ..models import User


@authentication_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for handling the login process. This function processes both GET and
    POST requests.
    On GET, it displays the login form. On POST, it validates the form and logs
    the user in if the credentials are correct.

    Returns:
        Redirects to the next page if login is successful and the next URL is safe.
        Otherwise, renders the login template again with a message for invalid
        credentials or displays the login form.
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


@authentication_bp.route("/logout")
def logout():
    """
    Route to handle the logout process. It logs out the current user.

    Returns:
        Redirects to the login page.
    """
    logout_user()
    return redirect(url_for("authentication_bp.login"))


@authentication_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for handling user registration. On GET, displays the registration form.
    On POST, it processes the form and creates a new user with the provided
    credentials.

    Returns:
        Redirects to the login page on successful registration, otherwise renders
        the registration form again with error messages.
    """
    form = RegistrationForm()
    if form.is_submitted():
        if form.validate():
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("authentication_bp.login"))
        flash("Registration Not Successful")

    return render_template("register.html", form=form)


def url_has_allowed_host_and_scheme(target, base_host, require_https=False):
    """
    Checks if the provided URL has an allowed host and scheme.

    Args:
        target (str): The target URL to validate.
        base_host (str): The base host to compare against.
        require_https (bool): Boolean indicating if HTTPS is required.

    Returns:
        bool: True if the scheme and host of the target URL are allowed,
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
