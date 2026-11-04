from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Job


def add_job(session: Session, job: Job) -> Job:
    session.add(job)
    session.flush()
    return job


def get_job(session: Session, job_id: int) -> Job | None:
    return session.get(Job, job_id)


def list_jobs(session: Session, limit: int, offset: int) -> list[Job]:
    statement = (
        select(Job)
        .options(selectinload(Job.skills))
        .order_by(Job.id)
        .offset(offset)
        .limit(limit)
    )
    return list(session.scalars(statement))
