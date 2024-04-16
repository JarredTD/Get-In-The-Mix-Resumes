from flask import jsonify

from . import database_bp
from ..models import ResumeData


@database_bp.route("/test-db", methods=["GET"])
def test_db():
    """
    Sanity Check that db is connected

    :returns: Message that db is connected
    :rtype: str
    """
    ResumeData.query.first()

    return "Database is connected."
