from flask import Blueprint

authentication_bp = Blueprint("authentication_bp", __name__)
resumes_bp = Blueprint("resumes_bp", __name__)
database_bp = Blueprint("database_bp", __name__)

from . import authentication, resumes, database
