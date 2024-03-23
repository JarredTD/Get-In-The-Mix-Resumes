"""Entry point for the Flask application."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    Serve the main index page.

    :return: The rendered template for the main index page.
    :rtype: str
    """
    return render_template("index.html")


@app.route("/about-us")
def about_us():
    """
    Serve the 'About Us' page.

    :return: The rendered template for the 'About Us' page.
    :rtype: str
    """
    return render_template("about_us.html")


@app.route("/project-motivation")
def motivation():
    """
    Serve the 'Project Motivation' page.

    :return: The rendered template for the 'Project Motivation' page.
    :rtype: str
    """
    return render_template("motivation.html")
