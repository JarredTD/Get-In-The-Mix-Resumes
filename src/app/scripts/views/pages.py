"""Views component of MVC paradigm"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms import ResumeForm
from . import views_bp


@views_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = ResumeForm()
    return render_template("index.html", form=form)


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
