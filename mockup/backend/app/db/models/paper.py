import uuid

from sqlalchemy import DateTime, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    title: Mapped[str] = mapped_column(Text, default="")
    abstract_raw: Mapped[str] = mapped_column(Text, default="")
    abstract_norm: Mapped[str] = mapped_column(Text, default="")
    clean_abstract: Mapped[str] = mapped_column(Text, default="")
    year: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    authors: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True)
    journal: Mapped[str | None] = mapped_column(String(512), index=True, nullable=True)
    language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pb_results = relationship("PBResult", back_populates="paper", cascade="all,delete")
    jobs = relationship("ProcessingJob", back_populates="paper")
