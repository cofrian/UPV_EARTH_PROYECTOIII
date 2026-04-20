import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.paper_repository import PaperRepository
from app.schemas.paper import PBResultOut, PaperListResponse, PaperOut

router = APIRouter()


def _to_paper_out(repo: PaperRepository, paper) -> PaperOut:
    pb = repo.get_latest_pb_result(paper.id)
    pb_out = None
    if pb:
        pb_out = PBResultOut(
            top_pb_code=pb.top_pb_code,
            top_pb_score=pb.top_pb_score,
            secondary_pbs=pb.secondary_pbs,
            score_map=pb.score_map,
            explanation_text=pb.explanation_text,
        )
    return PaperOut(
        id=paper.id,
        doc_id=paper.doc_id,
        title=paper.title,
        abstract_norm=paper.abstract_norm,
        year=paper.year,
        doi=paper.doi,
        source=paper.source,
        journal=paper.journal,
        keywords=paper.keywords,
        created_at=paper.created_at,
        pb_result=pb_out,
    )


@router.get("", response_model=PaperListResponse)
def list_papers(
    query: str | None = None,
    year: int | None = None,
    max_year: int | None = Query(default=None, ge=1900, le=2100),
    journal: str | None = None,
    pb: str | None = None,
    doi: str | None = None,
    keywords: str | None = None,
    sort: str = Query(default="created_desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PaperListResponse:
    repo = PaperRepository(db)
    items, total = repo.list_papers(query, year, max_year, journal, pb, doi, keywords, sort, page, page_size)
    return PaperListResponse(total=total, page=page, page_size=page_size, items=[_to_paper_out(repo, i) for i in items])


@router.get("/{paper_id}", response_model=PaperOut)
def get_paper(paper_id: uuid.UUID, db: Session = Depends(get_db)) -> PaperOut:
    repo = PaperRepository(db)
    paper = repo.get_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper no encontrado")
    return _to_paper_out(repo, paper)
