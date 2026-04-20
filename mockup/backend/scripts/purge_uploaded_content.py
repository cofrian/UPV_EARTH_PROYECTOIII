"""
Purga contenido generado por subidas manuales en el mockup.

Elimina:
- papers con source=uploaded_pdf o doc_id con prefijo upload-
- pb_results asociados
- desvincula processing_jobs.paper_id

No rompe el corpus seed.
"""
from __future__ import annotations

from sqlalchemy import or_, func

from app.db.base import Base
from app.db.models.paper import Paper
from app.db.models.pb_result import PBResult
from app.db.models.processing_job import ProcessingJob
from app.db.session import SessionLocal, engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        source_norm = func.lower(func.trim(func.coalesce(Paper.source, "")))
        uploaded_papers = (
            db.query(Paper)
            .filter(
                or_(
                    source_norm == "uploaded_pdf",
                    Paper.doc_id.like("upload-%"),
                )
            )
            .all()
        )

        paper_ids = [p.id for p in uploaded_papers]
        print(f"papers subidos detectados: {len(paper_ids)}")
        if not paper_ids:
            print("No hay registros para purgar.")
            return

        jobs_updated = (
            db.query(ProcessingJob)
            .filter(ProcessingJob.paper_id.in_(paper_ids))
            .update({"paper_id": None}, synchronize_session=False)
        )
        pb_deleted = db.query(PBResult).filter(PBResult.paper_id.in_(paper_ids)).delete(
            synchronize_session=False
        )
        papers_deleted = db.query(Paper).filter(Paper.id.in_(paper_ids)).delete(
            synchronize_session=False
        )
        db.commit()

        print(f"jobs desvinculados: {jobs_updated}")
        print(f"pb_results eliminados: {pb_deleted}")
        print(f"papers eliminados: {papers_deleted}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
