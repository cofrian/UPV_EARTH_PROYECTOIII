import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.ingestion_event import IngestionEvent
from app.db.models.paper import Paper
from app.db.models.pb_result import PBResult
from app.db.models.processing_job import ProcessingJob


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, filename: str) -> ProcessingJob:
        job = ProcessingJob(filename_original=filename, status="queued", stage="upload", progress_pct=0)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job(self, job_id: uuid.UUID) -> ProcessingJob | None:
        return self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

    def update_job(self, job: ProcessingJob, *, status: str, stage: str, progress_pct: int, error_code: str | None = None, error_message: str | None = None) -> ProcessingJob:
        job.status = status
        job.stage = stage
        job.progress_pct = progress_pct
        job.error_code = error_code
        job.error_message = error_message
        if status == "parsing" and job.started_at is None:
            job.started_at = datetime.now(timezone.utc)
        if status in {"completed", "failed"}:
            job.finished_at = datetime.now(timezone.utc)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def create_paper(self, **kwargs) -> Paper:
        paper = Paper(**kwargs)
        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)
        return paper

    def create_pb_result(self, **kwargs) -> PBResult:
        result = PBResult(**kwargs)
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def attach_paper_to_job(self, job: ProcessingJob, paper_id: uuid.UUID) -> None:
        job.paper_id = paper_id
        self.db.add(job)
        self.db.commit()

    def add_event(self, job_id: uuid.UUID, event_type: str, payload: dict) -> None:
        event = IngestionEvent(job_id=job_id, event_type=event_type, event_payload=payload)
        self.db.add(event)
        self.db.commit()

    def list_events(self, job_id: uuid.UUID, limit: int = 100) -> list[IngestionEvent]:
        return (
            self.db.query(IngestionEvent)
            .filter(IngestionEvent.job_id == job_id)
            .order_by(IngestionEvent.created_at.asc())
            .limit(limit)
            .all()
        )
