"""Sensitive Constants"""

import os

# pylint: disable=too-few-public-methods


class Config:
    """Base configuration class."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    FLASK_LOGIN_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration class."""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration class."""

    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    FLASK_LOGIN_SECRET_KEY = "12345"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SERVER_NAME = "localhost.localdomain"
