import re
import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_abstract(text: str) -> str:
    normalized = normalize_text(text)
    normalized = re.sub(r"(?i)\b(abstract|summary|resumen)\s*[:\-]?", "", normalized)
    normalized = re.sub(r"\[[0-9,\- ]+\]", "", normalized)
    return normalize_text(normalized)
