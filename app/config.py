"""Sensitive Constants"""

import os


class Config:
    """Config Class"""

    DATABASE_URI = os.getenv("DATABASE_URI")
