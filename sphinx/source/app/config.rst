Configuration Classes
=====================

The Flask application uses different configuration classes to tailor its settings for various environments, such as development, testing, and production. This document provides an overview of these classes, all of which are defined in the `config` module.

Configurations Overview
-----------------------

The configurations are defined in a hierarchical structure, with a base `Config` class that sets common settings across all environments. Derived classes like `DevelopmentConfig` and `TestingConfig` provide environment-specific overrides.

.. automodule:: app.config
   :members:
   :special-members: __init__
   :show-inheritance:
   :inherited-members:
