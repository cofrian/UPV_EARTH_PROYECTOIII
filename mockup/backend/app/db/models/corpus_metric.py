import uuid

from sqlalchemy import JSON, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CorpusMetric(Base):
    __tablename__ = "corpus_metrics_cache"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_group: Mapped[str] = mapped_column(String(64), index=True)
    metric_key: Mapped[str] = mapped_column(String(128), index=True)
    metric_value: Mapped[dict] = mapped_column(JSON, default=dict)
    generated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
