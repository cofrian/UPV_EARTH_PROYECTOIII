import re


def summarize_abstract(text: str, max_sentences: int = 4) -> str:
    parts = re.split(r"(?<=[\.!?])\s+", (text or "").strip())
    parts = [p for p in parts if p]
    return " ".join(parts[:max_sentences])
