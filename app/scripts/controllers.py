"""Controller for the flask app"""

from typing import Union, List, Tuple
from flask import Flask, jsonify, request, Response

from app import app


@app.route("/load", methods=["GET", "POST"])
def load() -> Union[str, Response, Tuple[Response, int]]:
    """
    Loads a list of resume ids, or data specific to an id.

    This endpoint responds to both GET and POST requests.
    For GET requests, it returns a list of all resume IDs.
    For POST requests, it expects a JSON payload with an "id" key and returns
    data specific to that resume ID.

    :return: For GET requests, a string representation of a list of resume IDs.
             For POST requests, returns the result of `loadResume(id_value)` function call.
    :rtype: str for GET requests; Flask `Response` for POST requests.

    :raises BadRequest: If the POST request does not include a JSON payload with an "id" key.
    """
    if request.method == "POST":
        if not request.json or "id" not in request.json:
            return jsonify({"error": "Bad request"}), 400

        id_value = request.json["id"]
        return loadResume(id_value)

    return ", ".join(getResumeIds())


def loadResume(id_value: str) -> Union[Response, Tuple[Response, int]]:
    """
    Loads data of a specific resume.

    :param id_value: The ID of the resume to load.
    :type id_value: str
    :return: A JSON response with the resume data.
    :rtype: Flask `Response`
    """

    return jsonify({"message": "Resume loaded", "id": id_value}), 200


def getResumeIds() -> List[str]:
    """
    Loads all resume IDs from the database.

    :return: A list of resume IDs.
    :rtype: List[str]
    """

    return ["1", "2", "3"]
