"""Expose blueprints for ease of importing"""

from flask import Blueprint

views_bp = Blueprint("views_bp", __name__)

from . import pages
