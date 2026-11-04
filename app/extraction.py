from typing import Protocol

from app.schemas import JobDraft


class JobExtractionClient(Protocol):
    def extract_job(self, job_ad_text: str) -> object: ...


def extract_job_draft(job_ad_text: str, client: JobExtractionClient) -> JobDraft:
    if not job_ad_text.strip():
        raise ValueError("Job ad text must not be empty")

    raw_draft = client.extract_job(job_ad_text)
    return JobDraft.model_validate(raw_draft)
