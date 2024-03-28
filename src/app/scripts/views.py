"""Views component of MVC paradigm"""

from flask import Blueprint, render_template
from flask_login import login_required

views_bp = Blueprint("views_bp", __name__)


@views_bp.route("/")
@login_required
def index() -> str:
    """
    Serve the main index page.

    :return: The rendered template for the main index page.
    :rtype: str
    """
    return render_template("index.html")


@views_bp.route("/about-us")
def about_us() -> str:
    """
    Serve the 'About Us' page.

    :return: The rendered template for the 'About Us' page.
    :rtype: str
    """
    return render_template("about_us.html")


@views_bp.route("/project-motivation")
def motivation() -> str:
    """
    Serve the 'Project Motivation' page.

    :return: The rendered template for the 'Project Motivation' page.
    :rtype: str
    """
    return render_template("motivation.html")
