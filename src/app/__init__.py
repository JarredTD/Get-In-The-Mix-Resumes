"""Declare Flask App"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=DevelopmentConfig):
    """Used to create the app from a config"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = config_class.FLASK_LOGIN_SECRET_KEY

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "controllers_bp.login"

    with app.app_context():
        # pylint: disable=wrong-import-position
        # pylint: disable=import-outside-toplevel
        # pylint: disable=unused-import

        from app.scripts import models
        from app.scripts import forms
        from app.scripts import controllers
        from app.scripts import views

        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(user_id)

        app.register_blueprint(views.views_bp)
        app.register_blueprint(controllers.authentication_bp, url_prefix="/auth")
        app.register_blueprint(controllers.resumes_bp, url_prefix="/resumes")
        app.register_blueprint(controllers.database_bp, url_prefix="/db")

    return app
