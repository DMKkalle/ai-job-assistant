from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories import get_job, list_jobs
from app.schemas import AnalysisRequest, AnalysisResponse, JobCreate, JobResponse
from app.services import analyze_candidate_for_job, create_job

app = FastAPI(title="AI Job Assistant API")


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_request: Request, error: RequestValidationError):
    details = []
    for validation_error in error.errors():
        field_parts = validation_error["loc"]
        field = ".".join(str(part) for part in field_parts if part != "body")
        details.append({"field": field, "message": validation_error["msg"]})

    return JSONResponse(status_code=422, content={"detail": details})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyses", response_model=AnalysisResponse)
def analyze_job(request: AnalysisRequest):
    return analyze_candidate_for_job(
        request.candidate.model_dump(),
        request.job.model_dump(),
    )


@app.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job_endpoint(
    job_data: JobCreate,
    session: Annotated[Session, Depends(get_session)],
):
    return create_job(session, job_data)


@app.get("/jobs", response_model=list[JobResponse])
def read_jobs(
    session: Annotated[Session, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return list_jobs(session, limit=limit, offset=offset)


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_endpoint(
    job_id: int,
    session: Annotated[Session, Depends(get_session)],
):
    job = get_job(session, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
