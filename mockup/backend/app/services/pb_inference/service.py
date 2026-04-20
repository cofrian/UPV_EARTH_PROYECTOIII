import csv
from functools import lru_cache

import numpy as np

from app.core.config import settings
from app.services.embedding_service.service import embed_texts


@lru_cache(maxsize=1)
def load_pb_catalog() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with open(settings.pb_reference_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(
                {
                    "pb_code": row.get("pb_code", "PB-UNK"),
                    "pb_name": row.get("pb_name", "Unknown"),
                    "text": " ".join(
                        [
                            row.get("short_definition", ""),
                            row.get("core_keywords", ""),
                            row.get("applied_keywords_upv", ""),
                        ]
                    ).strip(),
                }
            )
    return rows


def infer_pb_scores(clean_abstract: str, top_k: int | None = None) -> dict:
    pb_catalog = load_pb_catalog()
    pb_texts = [item["text"] for item in pb_catalog]
    vectors = embed_texts([clean_abstract, *pb_texts])

    abstract_vec = vectors[0]
    pb_vecs = vectors[1:]
    similarities = pb_vecs @ abstract_vec

    scored = []
    for item, score in zip(pb_catalog, similarities, strict=False):
        scored.append({"pb_code": item["pb_code"], "pb_name": item["pb_name"], "score": float(score)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    k = top_k or settings.pb_top_k
    top = scored[0]
    secondary = scored[1:k]

    return {
        "top_pb_code": top["pb_code"],
        "top_pb_score": top["score"],
        "secondary_pbs": secondary,
        "score_map": {item["pb_code"]: round(item["score"], 4) for item in scored},
        "explanation_text": (
            f"El abstract se alinea principalmente con {top['pb_code']} por similitud semantica ")
            + "respecto a definiciones y keywords de los Planetary Boundaries.",
    }
