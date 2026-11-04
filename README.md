# AI Job Assistant

A portfolio project for building a reliable AI-assisted job analysis system with **Python, FastAPI, SQLAlchemy, Pydantic, Alembic, and LLM structured outputs**.

The project combines deterministic candidate/job matching with a model-independent extraction layer that turns unstructured job ads into validated, reviewable data.

## Highlights

- Structured LLM extraction into strict Pydantic schemas
- Prompt-injection-aware extraction boundary
- Model-independent design through a small client protocol
- Deterministic required/preferred skill matching with candidate evidence
- FastAPI REST API
- SQLAlchemy + SQLite persistence with Alembic migrations
- Synthetic eval cases
- Automated tests, Ruff, and GitHub Actions CI
- No real CV data, personal candidate data, API keys, or secrets are stored in the repository

## Architecture

```text
Job ad text
    |
    v
Extraction service ---> LLM client boundary ---> OpenAI adapter
    |                         |
    v                         v
Validated JobDraft       Fake clients in tests

Candidate + job data
    |
    v
FastAPI
    |
    v
Application services
    |
    +--> Deterministic matching
    |
    v
Repository layer ---> SQLAlchemy ---> SQLite
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Tech stack

Python · FastAPI · Pydantic · SQLAlchemy · Alembic · SQLite · OpenAI Responses API · pytest · Ruff · GitHub Actions

## Quick start

```bash
git clone https://github.com/DMKkalle/ai-job-assistant.git
cd ai-job-assistant
python -m venv .venv
python -m pip install -r requirements-dev.txt
python -m alembic upgrade head
fastapi dev app/main.py
```

API docs are then available at `http://127.0.0.1:8000/docs`.

Run all checks with:

```bash
python scripts/check.py
```

## Current status

This is an active portfolio project, not a finished commercial product. The API foundation, persistence layer, deterministic matching, validated LLM extraction boundary, OpenAI adapter, tests, and synthetic eval foundation are implemented.

Next steps include exposing extraction through the API, expanding eval coverage, and adding measured model-quality results.
