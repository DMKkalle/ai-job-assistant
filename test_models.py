from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Job, JobSkill
from app.repositories import add_job, get_job


def test_persists_job_and_skills():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        job = Job(
            title="AI Engineer",
            company="Example AB",
            skills=[
                JobSkill(name="Python", skill_type="required"),
                JobSkill(name="Git", skill_type="preferred"),
            ],
        )
        saved = add_job(session, job)
        job_id = saved.id
        session.commit()

    with Session(engine) as session:
        fetched = get_job(session, job_id)
        assert fetched is not None
        assert fetched.title == "AI Engineer"
        assert {skill.name for skill in fetched.skills} == {"Python", "Git"}
