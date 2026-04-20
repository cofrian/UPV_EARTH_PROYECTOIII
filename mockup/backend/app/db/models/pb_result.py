import uuid

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PBResult(Base):
    __tablename__ = "pb_results"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    model_version: Mapped[str] = mapped_column(String(128), default="all-MiniLM-L6-v2@v1")
    top_pb_code: Mapped[str] = mapped_column(String(32), index=True)
    top_pb_score: Mapped[float] = mapped_column(Float)
    secondary_pbs: Mapped[dict] = mapped_column(JSON, default=dict)
    score_map: Mapped[dict] = mapped_column(JSON, default=dict)
    threshold_used: Mapped[float] = mapped_column(Float, default=0.3)
    explanation_text: Mapped[str] = mapped_column(String(2048), default="")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    paper = relationship("Paper", back_populates="pb_results")
