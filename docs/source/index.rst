=================================
Get In The Mix Resumes
=================================

.. image:: https://github.com/JarredTD/Get-In-The-Mix-Resumes/actions/workflows/main.yml/badge.svg
    :target: https://github.com/JarredTD/Get-In-The-Mix-Resumes/actions

.. image:: https://coveralls.io/repos/github/JarredTD/Get-In-The-Mix-Resumes/badge.svg?branch=main
    :target: https://coveralls.io/github/JarredTD/Get-In-The-Mix-Resumes?branch=main

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


Introduction
============

Get-In-The-Mix-Resumes is a tool designed to simplify and enhance the process of creating and managing resumes. It provides an intuitive way to compile professional resumes.

Installation
============

Prerequisites
-------------

- Python 3.12
- Docker

Instructions
------------

Steps 2-4 are automated by the script ``deploy.sh``.

1. Clone the repository (https://github.com/JarredTD/Get-In-The-Mix-Resumes)
2. Build the Docker image in app/
3. Run a container of the image
4. Open the address specified in the Docker logs

Usage
=====

WIP

Module Documentation
====================

.. toctree::
   :maxdepth: 2

   src/app
   src/app.scripts.controllers.rst
   src/app.scripts.forms.rst
   src/src/app.scripts.models.rst
   src/app.scripts.views.rst
   src/app.scripts.rst
   src/tests


Contributing
============

Please follow the guidelines below, use the ``build.sh`` script in the root directory to confirm all requirements are met.

License
=======

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details. GPL-3.0 is a free, copyleft license for software and other kinds of works, providing the freedom to run, study, share, and modify the software.

For more details on the GPL-3.0 License, please refer to [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
