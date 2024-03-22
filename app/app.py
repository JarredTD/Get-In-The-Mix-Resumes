"""Entry point for the flask application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Routes '/' to 'index.html'"""
    return render_template("index.html")


@app.route("/about-us")
def about_us():
    """Routes '/about-us' to 'about_us.html'"""
    return render_template("about_us.html")


@app.route("/project-motivation")
def motivation():
    """Routes '/project-motivation' to 'motivation.html'"""
    return render_template("motivation.html")
