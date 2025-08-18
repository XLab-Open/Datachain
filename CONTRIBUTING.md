# Contributing
Welcome to participate in this project, the project aims to build a high-performance model inference library, welcome all kinds of contributions, the main ways to contribute are as follows:

- **Fix Bug**: If you find any bugs or issues, please report them by opening an issue in the repository.
- **Feature Request**: If you have any suggestions or ideas for new features, please submit them by opening an issue in the repository.
- **docs**: You can contribute test documents, functional documentation, and API documentation for each module.
- **Code Contribution**: If you are interested in contributing to the project.

## Overview
1. Create a fork of the Warp GitHub repository by visiting [XLab-Open/Datachain](https://github.com/XLab-Open/Datachain)

2. Clone your fork on your local machine, e.g. git clone https://github.com/XLab-Open/Datachain.git.

3. Create a branch to develop your contribution on.

    Use the following naming conventions for the branch name:
    - New features: **newfeat/feature-name**
    - Bug fixes: **bugfix/feature-name**

4. Make your desired changes.
    - Take some time to review the overall coding standards.
    - Make sure your modifications comply with formatting rules and lint checks.
    - Provide test cases to confirm the functionality works as intended (Datachain tests).
    - Include documentation updates whenever you introduce new functionality (see Documentation build).

5. Push your branch to your forked repository on GitHub, for example: git push origin username/feature-name.

6. Submit a pull request targeting the main branch on GitHub (see Pull Request Guidelines). Collaborate with reviewers to address feedback until it is ready to be merged.


## General Code Style
- Code should adhere to the Google Python Style Guide for consistency and readability.
- All source code contributions must comply with the terms of the Apache 2.0 license.


## Getting started
### Setting dev environment
#### 1. Using uv (optional)
- **Install uv**: see the [installation guide](https://docs.astral.sh/uv/getting-started/installation/).
- **Create virtualenv**: `uv venv --python python3.11 ` and then `source .venv/bin/activate`.
- **Install dev dependencies**: `uv pip install -e ".[dev]"`.
- **Run tests**: `uv run pytest`.
- **Run pre-commit hooks**: `uv run pre-commit run --all-files`.

Alternatively, you can use the Makefile shortcuts:
- `make uv-venv`
- `make uv-install-dev`
- `make uv-test`
- `uv-pre-commit`

#### 2. Using pip (optional)
- **Set conda**: `conda create -n datachain_dev python==3.11 -y`
- **Activate conda**: `conda activate datachain_dev `
- **Install dev dependencies **: `pip install -r requirements-dev.txt `
- **Run tests**: `pytest`.
- **Run pre-commit hooks**: `pre-commit run --all-files`.

### Linting and Formatting
pre-commit is used as the linter and code formatter for Python code in the Warp repository. The contents of pull requests will automatically be checked to ensure adherence to our formatting and linting standards.

- Using uv (optional)
    - **Run pre-commit hooks**: `uv run pre-commit run --all-files`.

    Alternatively, you can use the Makefile shortcuts: `uv-pre-commit`

- Using pip (optional)
    - **Run tests**: `pre-commit run --all-files`.

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration. The following workflows run automatically:

- **Test**: Runs tests across Python 3.8-3.12 with coverage reporting
- **Lint**: Runs code quality checks (spell check, shell check, C++ lint)

#### Running CI Checks Locally

Before submitting a PR, run the CI checks locally:

```shell
# Run all CI checks (format, lint, type-check, test)
make ci-local

# Or run individual checks:
make ci-lint      # Run pre-commit hooks
make ci-test      # Run tests with coverage
```

### Testing
The main test code is located in the tests directory.
- Using uv (optional)
    - **Run tests**: `uv run pytest`.

    Alternatively, you can use the Makefile shortcuts: `make uv-test`

- Using pip (optional)
    - **Run tests**: `pytest`.

### Pull Request Guidelines
Make sure your pull request uses a clear and descriptive title that reflects the intent of your modifications.

Provide a short description that includes:
- A summary of what was changed.
- The parts of the project impacted by these changes.
- The issue or problem that the changes aim to resolve.
- Any limitations or areas not fully addressed by the update.
- References to any GitHub issues that are related to or fixed by this pull request.
