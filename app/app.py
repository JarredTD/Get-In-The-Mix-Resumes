from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about-us")
def about_us():
    return render_template("about_us.html")

@app.route("/project-motivation")
def motivation():
    return render_template("motivation.html")
