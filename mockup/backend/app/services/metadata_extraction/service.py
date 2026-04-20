import re


def infer_year(text: str) -> int | None:
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text or "")
    if not years:
        return None
    year = int(years[0])
    if 1900 <= year <= 2100:
        return year
    return None
