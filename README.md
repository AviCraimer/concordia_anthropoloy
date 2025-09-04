# concordia_anthropology

## Setup
On Windows use Windows Subsystem for Linux (WSL) for project.
On MaxOS or Linux OS everything should just work.

1. Install Python 3.13 (e.g., via pyenv)
2. Run: `make setup` to
    - Create venv
    - Install dependencies and build package
    - Install dev depedencies

## Build Project

After setup to re-build the package run `make build`

## Run Project
`make run`

## Type Checking (Pylance/Pyright)
- VScode: Install the pylance extension.
- Commandline checking: `make types`
- Config: `pyrightconfig.json`.


## Tests & Lint
- Tests: `make test`
- Lint: `make lint`

- Check all: `make check` runs tests, type checking and linting.

## Dependencies

Dependencies are kept in pyproject.toml:
[project].dependencies - Has all dependencies for running code.

[project.optional-dependencies].dev - has dependencies for development purposes (e.g., testing and linting).