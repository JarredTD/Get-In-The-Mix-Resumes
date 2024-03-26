"""Sensitive Constants"""

import os

# pylint: disable=too-few-public-methods


class Config:
    """Base configuration class."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration class."""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration class."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
