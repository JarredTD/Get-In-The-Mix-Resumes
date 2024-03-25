"""Controller for the flask app"""

from flask import request, jsonify
from app import app


@app.route("/load", methods=["GET", "POST"])
def load():
    """Loads a list of resume ids, or data specific to an id"""
    if request.method == "POST":
        if not request.json or "id" not in request.json:
            return jsonify({"error": "Bad request"}), 400

        id_value = request.json["id"]
        return loadResume(id_value)
    else:  # For GET requests
        return str(getResumeIds())


def loadResume(id_value):
    """Loads dat of a specific resume"""
    return jsonify({"message": "Resume loaded", "id": id_value}), 200


def getResumeIds():
    """Loads all ids from the db"""
    return ["1", "2", "3"]
