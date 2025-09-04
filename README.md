# concordia_anthropology

## Operating Systems
On Windows use Windows Subsystem for Linux (WSL) for project.
On macOS or Linux OS everything should just work.

## Setup
1. Install Python 3.13 (e.g., via pyenv)
2. Run: `make setup` to
    - Create venv
    - Install dependencies and build package
    - Install dev dependencies

## Build Project
After initial setup re-build the package only with `make build`

## Run Project
`make run`

## Type Checking (Pylance/Pyright)
- VScode: Install the pylance extension.
- Commandline checking: `make types`
- Config is in `pyrightconfig.json`.


## Tests & Lint
- Tests: `make test`
- Lint: `make lint`

- Check all: `make check` runs tests, type checking and linting.

## Dependencies

Dependencies are kept in pyproject.toml:
[project].dependencies - Has all dependencies for running code.

[project.optional-dependencies].dev - has dependencies for development purposes (e.g., testing and linting).