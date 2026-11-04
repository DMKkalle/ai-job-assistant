import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_session
from app.main import app

client = TestClient(app)


@pytest.fixture
def database_client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    test_engine.dispose()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint():
    response = client.post(
        "/analyses",
        json={
            "candidate": {
                "skills": ["Python", "Git"],
                "evidence": {
                    "Python": ["Built a Python project"],
                    "Git": ["Used Git in a project"],
                },
            },
            "job": {
                "required_skills": ["Python", "Docker"],
                "preferred_skills": ["Git"],
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["required_match_percentage"] == 50


def test_create_and_get_job(database_client):
    created = database_client.post(
        "/jobs",
        json={
            "title": "AI Engineer",
            "company": "Example AB",
            "required_skills": ["Python"],
            "preferred_skills": ["Git"],
        },
    )

    assert created.status_code == 201
    job_id = created.json()["id"]

    fetched = database_client.get(f"/jobs/{job_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "AI Engineer"
