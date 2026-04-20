import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.paper import PBResultOut


class JobOut(BaseModel):
    id: uuid.UUID
    paper_id: uuid.UUID | None
    filename_original: str
    status: str
    stage: str
    progress_pct: int
    error_code: str | None
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None


class JobResultOut(BaseModel):
    job: JobOut
    abstract_detected: str | None = None
    summary: str | None = None
    pb_result: PBResultOut | None = None


class JobEventOut(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    event_type: str
    event_payload: dict
    created_at: datetime | None
