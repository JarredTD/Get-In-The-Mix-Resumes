"""Declare Flask App"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    """Used to create the app from a config"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # pylint: disable=wrong-import-position
        # pylint: disable=import-outside-toplevel
        # pylint: disable=unused-import

        from app.scripts import models
        from app.scripts.controllers import controllers_bp
        from app.scripts.views import views_bp

        app.register_blueprint(views_bp)
        app.register_blueprint(controllers_bp)

    return app