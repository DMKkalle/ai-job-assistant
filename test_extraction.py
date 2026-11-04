import pytest
from pydantic import ValidationError

from app.extraction import extract_job_draft
from app.schemas import JobDraft


class FakeExtractionClient:
    def __init__(self, response):
        self.response = response
        self.received_texts = []

    def extract_job(self, job_ad_text):
        self.received_texts.append(job_ad_text)
        return self.response


def valid_response():
    return {
        "title": "AI Engineer",
        "company": "Example AB",
        "technologies": ["Python"],
        "requirements": [
            {
                "name": "Python",
                "category": "technical_skill",
                "importance": "required",
                "source_evidence": "Experience with Python.",
            }
        ],
    }


def test_returns_validated_job_draft():
    draft = extract_job_draft(
        "We are hiring an AI Engineer.",
        FakeExtractionClient(valid_response()),
    )

    assert isinstance(draft, JobDraft)
    assert draft.title == "AI Engineer"


def test_rejects_invalid_model_output():
    response = valid_response()
    response["requirements"][0]["importance"] = "bonus"

    with pytest.raises(ValidationError):
        extract_job_draft("AI Engineer", FakeExtractionClient(response))
