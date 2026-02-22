# Contributing

Thank you for your interest in contributing to PyPortion.

## Types of Contributions

* **Reporting bugs** — Found something broken? [Open an issue](https://github.com/atharabia/pyportion/issues)
* **Suggesting features** — Have an idea? [Start a discussion](https://github.com/atharabia/pyportion/discussions)
* **Testing new releases** — Try the latest versions and share feedback
* **Improving documentation** — Help others understand PyPortion
* **Contributing code** — Fix bugs or add new features

## Local Development Setup

1. **Fork the repository**

    Go to the GitHub repo and click "Fork" to create your own copy.

2. **Clone your fork**

    ```bash
    git clone https://github.com/<your-username>/pyportion
    ```

3. **Install Poetry (if you don't have it)**

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

4. **Install project dependencies**

    ```bash
    poetry install
    ```

5. **Install pre-commit hooks**

    ```bash
    poetry run pre-commit install
    ```

6. **Make your changes**, then commit and push to open a pull request.

## Pre-Commit Hooks

Pre-commit hooks run automatically on every commit and perform the following checks:

* Format code
* Lint code
* Type check
* Sort imports
* Run test cases

**Note:** Hooks may automatically modify files to match the project's coding style. If this happens, stage the changes and commit again before pushing.

## Pull Request Review

All pull requests go through an automatic review via GitHub Actions, followed by a manual review.

Reviewers focus on:

* Code clarity and readability
* Consistency with the project structure
* Test coverage
* Quality and clarity of commit messages

## Need Help?

Open a [discussion](https://github.com/atharabia/pyportion/discussions) on GitHub.
