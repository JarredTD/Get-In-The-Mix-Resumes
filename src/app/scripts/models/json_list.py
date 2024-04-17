"""Custom Type Decorator for storing list of strings as json"""

import json
from sqlalchemy import TypeDecorator, Text


class JsonList(TypeDecorator):
    """
    A custom SQLAlchemy column type for storing lists as JSON-formatted strings.

    This type automatically serializes Python lists to JSON strings when data is
    bound to the database, and deserializes JSON strings back to Python lists when
    querying the data. It's designed to be used as a column type in SQLAlchemy models
    for fields that require storing list data in a relational database.

    Inherits from:
        TypeDecorator: A generic superclass from SQLAlchemy for creating custom types.

    Example:
        class MyModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            my_list = db.Column(JSONList)

    After defining a model with `JSONList`, you can directly assign Python
    lists to `my_list`, and they will be stored as JSON strings in the
    database. When querying, these strings will be returned as Python lists.
    """

    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """
        Process the Python value before saving it to the database.

        This method serializes Python lists to JSON strings. If the value is
        `None`, it remains `None`.

        :param value: The original Python list to be serialized to JSON.
        :param dialect: The dialect in use (not used in this method but required
                        by the interface).
        :return: A JSON string representation of the list, or `None` if the
                 original value was `None`.
        """
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        """
        Process the database value back to a Python type after querying.

        This method deserializes JSON strings back into Python lists. If the value is
        `None`, it remains `None`.

        :param value: The JSON string from the database to be deserialized.
        :param dialect: The dialect in use (not used in this method but required by
                        the interface).
        :return: A Python list representation of the JSON string, or `None` if the
                original value was `None`.
        """
        if value is not None:
            value = json.loads(value)
        return value
