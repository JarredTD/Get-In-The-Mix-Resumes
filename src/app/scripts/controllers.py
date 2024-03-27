"""Controller for the flask app"""

from typing import List, Union
from flask import jsonify, request, Blueprint
from flask.wrappers import Response
from .models import ResumeData

controllers_bp = Blueprint("controllers_bp", __name__)


@controllers_bp.route("/test-db", methods=["GET"])
def test_db() -> str:
    """
    Sanity Check that db is connected

    :returns: Message that db is connected
    :rtype: str
    """
    ResumeData.query.first()

    return "Database is connected."


@controllers_bp.route("/load-resume-ids", methods=["GET"])
def load_resume_ids() -> Response:
    """
    Queries all ids found in ResumeData table

    :returns: List of all ids in ResumeData table
    :rtype: List of Ints
    """
    ids = (
        ResumeData.query.with_entities(ResumeData.id)
        .order_by(ResumeData.entry_date)
        .all()
    )
    id_list: List[int] = [id[0] for id in ids]
    return jsonify(id_list)


@controllers_bp.route("/load-resume", methods=["POST"])
def load_resume() -> Union[Response, tuple]:
    """
    Queries for a specific resume in the ResumeData table

    :returns: A json of the resume data for the found resume
            or an error for invalid request or resume not found
    :rtype: Json object
    """
    resume_request = request.get_json()
    resume_id = resume_request.get("id")

    if resume_id is None:
        return jsonify({"error": "Missing ID"}), 400

    resume = ResumeData.query.filter_by(id=resume_id).first()

    if resume is None:
        return jsonify({"error": "No Resume Found"}), 404

    return jsonify(resume.to_dict())
