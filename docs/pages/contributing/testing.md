# Testing

## Test Structure

```
tests/
├── conftest.py               # Shared fixtures
├── commands/                 # Tests for each command
├── step_actions/             # Tests for each step action
└── utils/                    # Test helpers (ANSI stripping, template fixtures)
```

## Running Tests

```bash
poetry run pytest
```

With coverage report:

```bash
poetry run pytest --cov=portion --cov-report=term-missing
```

## Type Checking

```bash
poetry run mypy portion/
```

## Linting

```bash
poetry run flake8 portion/
```

## Import Sorting

```bash
poetry run isort portion/
```

All of the above also run automatically via pre-commit hooks on every commit.
