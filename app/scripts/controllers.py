"""Controller for the flask app"""

from typing import Union, List, Tuple
from flask import jsonify, Response, Blueprint
from .models import ResumeData

controllers_bp = Blueprint("controllers_bp", __name__)


@controllers_bp.route("/test-db")
def test_db() -> str:
    """Sanity Check that db is connected"""
    result = ResumeData.query.first()
    if result:
        return f"Database is connected. Found: {result}"

    return "Database is connected but found no data."


@controllers_bp.route("/load", methods=["POST", "GET"])
def load(route_request) -> Union[str, Response, Tuple[Response, int]]:
    """
    Loads a list of resume ids, or data specific to an id.

    This endpoint responds to both GET and POST requests.
    For GET requests, it returns a list of all resume IDs.
    For POST requests, it expects a JSON payload with an "id" key and returns
    data specific to that resume ID.

    :param route_request: The request object.
    :type route_request: Flask request
    :returns: For GET requests, a string representation of a list of resume IDs.
                For POST requests, returns the result of ``loadResume(id_value)``
                function call.
    :rtype: str for GET requests; Flask `Response` for POST requests.
    :raises BadRequest: If the POST request does not include a JSON payload
                        with an "id" key.
    """
    if route_request.method == "POST":
        if not route_request.json or "id" not in route_request.json:
            return jsonify({"error": "Bad request"}), 400

        id_value = route_request.json["id"]
        return load_resume(id_value)

    return ", ".join(get_resume_ids())


def load_resume(id_value: str) -> Union[Response, Tuple[Response, int]]:
    """
    Loads data of a specific resume.

    :param id_value: The ID of the resume to load.
    :type id_value: str
    :return: A JSON response with the resume data.
    :rtype: Flask `Response`
    """

    return jsonify({"message": "Resume loaded", "id": id_value}), 200


def get_resume_ids() -> List[str]:
    """
    Loads all resume IDs from the database.

    :return: A list of resume IDs.
    :rtype: List[str]
    """

    return ["1", "2", "3"]
