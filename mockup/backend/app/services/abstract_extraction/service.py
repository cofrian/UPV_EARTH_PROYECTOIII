import re

ABSTRACT_PATTERNS = [
    re.compile(r"(?is)\babstract\b\s*[:\-]?\s*(.{200,3000}?)(?=\b(introduction|keywords|1\.|materials|methods)\b)"),
    re.compile(r"(?is)\bsummary\b\s*[:\-]?\s*(.{200,3000}?)(?=\b(introduction|keywords|1\.|materials|methods)\b)"),
    re.compile(r"(?is)\bresumen\b\s*[:\-]?\s*(.{200,3000}?)(?=\b(introduccion|palabras clave|1\.|materiales|metodos)\b)"),
]


def detect_abstract(full_text: str) -> str:
    text = full_text or ""
    for pattern in ABSTRACT_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1).strip()

    # Fallback conservador para no bloquear la inferencia.
    fallback = text[:2500].strip()
    return fallback
