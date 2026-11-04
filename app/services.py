from sqlalchemy.orm import Session

from app.models import Job, JobSkill
from app.repositories import add_job
from app.schemas import JobCreate
from job_matcher import (
    calculate_match_percentage,
    classify_skills_by_evidence,
    compare_job_requirements,
    find_uncertainties,
)


def analyze_candidate_for_job(candidate: dict, job: dict) -> dict:
    requirement_analysis = compare_job_requirements(candidate, job)
    required_analysis = requirement_analysis["required"]
    preferred_analysis = requirement_analysis["preferred"]

    all_matching_skills = (
        required_analysis["matching_skills"] + preferred_analysis["matching_skills"]
    )
    evidence_classification = classify_skills_by_evidence(
        candidate, all_matching_skills
    )

    return {
        "required": required_analysis,
        "preferred": preferred_analysis,
        "required_match_percentage": calculate_match_percentage(required_analysis),
        "evidence": evidence_classification,
        "uncertainties": find_uncertainties(evidence_classification),
    }


def create_job(session: Session, job_data: JobCreate) -> Job:
    skills = [
        JobSkill(name=name, skill_type="required") for name in job_data.required_skills
    ] + [
        JobSkill(name=name, skill_type="preferred")
        for name in job_data.preferred_skills
    ]

    job = Job(title=job_data.title, company=job_data.company, skills=skills)
    saved_job = add_job(session, job)
    session.commit()
    session.refresh(saved_job)
    return saved_job
