# Get-In-The-Mix-Resumes

![build](https://github.com/JarredTD/Get-In-The-Mix-Resumes/actions/workflows/main.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/JarredTD/Get-In-The-Mix-Resumes/badge.svg?branch=main)](https://coveralls.io/github/JarredTD/Get-In-The-Mix-Resumes?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

Get-In-The-Mix-Resumes is a tool designed to simplify and enhance the process of creating and managing resumes. It provides an intuitive way to compile professional resumes.

## Self Hosting

### Prerequisites

- Python 3.12
- Docker

### Instructions

Steps 2-4 are done by `deploy.sh`.

1. Clone the repository
2. Build the Docker image
3. Run a container of the image
4. Open the address specified in the docker logs

## Usage

[WIP]

## Contributing

Please follow the guidelines below, use the `build.sh` script in the root directory to confirm all requirements are met.

### Code Style

- We use `Black` for Python code formatting.

### Linting

- We use `pylint` for linting, with a score requirement.

### Testing

- Write tests for your new features or fixes and ensure they pass.
- We use `pytest` for testing, with a coverage requirement.

### Commit Messages

Use the conventional commit format for all your commits. This helps in automating our release process and maintaining a clear history. A conventional commit message should look like this:

```markdown
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:

```markdown
- feat: Introduces a new feature to the project.
- fix: Fixes a bug in the project.
- docs: Changes to documentation only.
- style: Code changes that do not affect the meaning (white-space, formatting, missing semi-colons, etc).
- refactor: Code changes that neither fix a bug nor add a feature.
- perf: Changes that improve performance.
- test: Adding missing tests or correcting existing tests.
- build: Updates to the build process.
- chore: Changes to auxiliary tools and libraries such as documentation generation.
```

For more details, refer to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details. GPL-3.0 is a free, copyleft license for software and other kinds of works, providing the freedom to run, study, share, and modify the software.

For more details on the GPL-3.0 License, please refer to [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html).
