import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.pb_result import PBResult
from app.db.session import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobEventOut, JobOut, JobResultOut
from app.schemas.paper import PBResultOut
from app.services.summarization.service import summarize_abstract

router = APIRouter()


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: uuid.UUID, db: Session = Depends(get_db)) -> JobOut:
    jobs = JobRepository(db)
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")

    return JobOut(
        id=job.id,
        paper_id=job.paper_id,
        filename_original=job.filename_original,
        status=job.status,
        stage=job.stage,
        progress_pct=job.progress_pct,
        error_code=job.error_code,
        error_message=job.error_message,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )


@router.get("/{job_id}/result", response_model=JobResultOut)
def get_job_result(job_id: uuid.UUID, db: Session = Depends(get_db)) -> JobResultOut:
    jobs = JobRepository(db)
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")

    job_out = JobOut(
        id=job.id,
        paper_id=job.paper_id,
        filename_original=job.filename_original,
        status=job.status,
        stage=job.stage,
        progress_pct=job.progress_pct,
        error_code=job.error_code,
        error_message=job.error_message,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )

    if not job.paper_id:
        return JobResultOut(job=job_out)

    paper = job.paper
    pb = db.query(PBResult).filter(PBResult.paper_id == job.paper_id).order_by(PBResult.created_at.desc()).first()
    pb_out = None
    if pb:
        pb_out = PBResultOut(
            top_pb_code=pb.top_pb_code,
            top_pb_score=pb.top_pb_score,
            secondary_pbs=pb.secondary_pbs,
            score_map=pb.score_map,
            explanation_text=pb.explanation_text,
        )

    summary = summarize_abstract(paper.clean_abstract) if paper else None
    return JobResultOut(job=job_out, abstract_detected=paper.abstract_norm if paper else None, summary=summary, pb_result=pb_out)


@router.get("/{job_id}/events", response_model=list[JobEventOut])
def list_job_events(job_id: uuid.UUID, limit: int = 200, db: Session = Depends(get_db)) -> list[JobEventOut]:
    jobs = JobRepository(db)
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")

    safe_limit = max(1, min(limit, 1000))
    events = jobs.list_events(job_id, limit=safe_limit)
    return [
        JobEventOut(
            id=event.id,
            job_id=event.job_id,
            event_type=event.event_type,
            event_payload=event.event_payload,
            created_at=event.created_at,
        )
        for event in events
    ]
