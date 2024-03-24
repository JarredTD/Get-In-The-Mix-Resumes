"""Views component of MVC paradigm"""

from flask import render_template
from app import app


@app.route("/")
def index() -> str:
    """
    Serve the main index page.

    :return: The rendered template for the main index page.
    :rtype: str
    """
    return render_template("index.html")


@app.route("/about-us")
def about_us() -> str:
    """
    Serve the 'About Us' page.

    :return: The rendered template for the 'About Us' page.
    :rtype: str
    """
    return render_template("about_us.html")


@app.route("/project-motivation")
def motivation() -> str:
    """
    Serve the 'Project Motivation' page.

    :return: The rendered template for the 'Project Motivation' page.
    :rtype: str
    """
    return render_template("motivation.html")
