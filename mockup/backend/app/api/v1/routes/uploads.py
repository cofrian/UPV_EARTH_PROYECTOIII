import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.repositories.job_repository import JobRepository
from app.schemas.upload import UploadResponse
from app.services.pdf_ingestion.service import InvalidUploadError, save_upload, validate_pdf
from app.workers.pipeline_runner import run_pdf_pipeline

router = APIRouter()


def _run_pipeline(job_id: uuid.UUID, pdf_path: str) -> None:
    db = SessionLocal()
    try:
        run_pdf_pipeline(db, job_id, pdf_path)
    finally:
        db.close()


@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadResponse:
    try:
        validate_pdf(file)
        pdf_path = await save_upload(file)
    except InvalidUploadError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    jobs = JobRepository(db)
    job = jobs.create_job(file.filename or "upload.pdf")

    background_tasks.add_task(_run_pipeline, job.id, pdf_path)

    return UploadResponse(job_id=str(job.id), status=job.status, message="Archivo recibido y job en cola")
