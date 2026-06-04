# Contributing to Empathy Engine

Thank you for your interest in contributing.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Quality checks

```bash
ruff check .
black .
mypy empathy_engine app.py cli.py
pytest tests/ -v
```

## Pull request guidelines

- Keep changes focused and well-tested.
- Update `CHANGELOG.md` for user-visible changes.
- Ensure CI passes before requesting review.
