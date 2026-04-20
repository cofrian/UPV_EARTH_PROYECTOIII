import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import (
    DashboardOverview,
    DistributionResponse,
    KeywordItem,
    PaperComparisonResponse,
    RuntimeMetricsResponse,
)
from app.services.analytics_service.service import (
    distribution_by_abstract_length,
    distribution_by_pb,
    distribution_by_source,
    distribution_by_year,
    overview,
    paper_comparison,
    top_keywords_by_pb,
    top_keywords_global,
)
from app.services.system_metrics import collect_system_metrics

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
def get_overview(db: Session = Depends(get_db)) -> DashboardOverview:
    return DashboardOverview(**overview(db))


@router.get("/distribution/pb", response_model=DistributionResponse)
def get_pb_distribution(db: Session = Depends(get_db)) -> DistributionResponse:
    return DistributionResponse(items=distribution_by_pb(db))


@router.get("/distribution/year", response_model=DistributionResponse)
def get_year_distribution(db: Session = Depends(get_db)) -> DistributionResponse:
    return DistributionResponse(items=distribution_by_year(db))


@router.get("/distribution/source", response_model=DistributionResponse)
def get_source_distribution(db: Session = Depends(get_db)) -> DistributionResponse:
    return DistributionResponse(items=distribution_by_source(db))


@router.get("/distribution/abstract-length", response_model=DistributionResponse)
def get_abstract_length_distribution(db: Session = Depends(get_db)) -> DistributionResponse:
    return DistributionResponse(items=distribution_by_abstract_length(db))


@router.get("/keywords/global", response_model=list[KeywordItem])
def get_global_keywords(
    limit: int = Query(default=20, ge=5, le=50),
    db: Session = Depends(get_db),
) -> list[KeywordItem]:
    return [KeywordItem(**item) for item in top_keywords_global(db, limit=limit)]


@router.get("/keywords/pb/{pb_code}", response_model=list[KeywordItem])
def get_pb_keywords(
    pb_code: str,
    limit: int = Query(default=20, ge=5, le=50),
    db: Session = Depends(get_db),
) -> list[KeywordItem]:
    return [KeywordItem(**item) for item in top_keywords_by_pb(db, pb_code=pb_code, limit=limit)]


@router.get("/papers/{paper_id}/comparison", response_model=PaperComparisonResponse)
def get_paper_comparison(paper_id: uuid.UUID, db: Session = Depends(get_db)) -> PaperComparisonResponse:
    payload = paper_comparison(db, paper_id=paper_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Paper no encontrado")
    return PaperComparisonResponse(**payload)


@router.get("/runtime/metrics", response_model=RuntimeMetricsResponse)
def get_runtime_metrics() -> RuntimeMetricsResponse:
    return RuntimeMetricsResponse(**collect_system_metrics())
