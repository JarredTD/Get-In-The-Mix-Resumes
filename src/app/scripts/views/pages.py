"""Views rendered """

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms import ResumeForm
from . import views_bp


@views_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Displays the homepage with a form to handle resume data.

    Returns:
        Rendered template: Renders the homepage with a resume form.
    """
    form = ResumeForm()
    return render_template("index.html", form=form)


@views_bp.route("/about-us")
def about_us():
    """
    Serve the 'About Us' page.

    Returns:
        str: The rendered template for the 'About Us' page.
    """
    return render_template("about_us.html")


@views_bp.route("/project-motivation")
def motivation():
    """
    Serve the 'Project Motivation' page.

    Returns:
        str: The rendered template for the 'Project Motivation' page.
    """
    return render_template("motivation.html")
