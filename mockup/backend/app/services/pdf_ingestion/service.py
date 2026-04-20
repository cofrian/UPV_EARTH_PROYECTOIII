import os
import uuid
from pathlib import Path

import fitz
from fastapi import UploadFile

from app.core.config import settings


class InvalidUploadError(Exception):
    pass


def ensure_upload_dir() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)


def validate_pdf(file: UploadFile) -> None:
    filename = (file.filename or "").lower()
    if not filename.endswith(".pdf"):
        raise InvalidUploadError("Solo se permiten archivos PDF.")


async def save_upload(file: UploadFile) -> str:
    ensure_upload_dir()
    safe_name = f"{uuid.uuid4()}_{Path(file.filename or 'upload.pdf').name}"
    target_path = os.path.join(settings.upload_dir, safe_name)

    content = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise InvalidUploadError(f"El archivo supera el limite de {settings.max_upload_size_mb} MB.")

    with open(target_path, "wb") as output:
        output.write(content)

    return target_path


def extract_text_from_pdf(pdf_path: str) -> str:
    text_parts: list[str] = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)
