import csv
import json
import time
from functools import lru_cache

import requests

from app.core.config import settings


@lru_cache(maxsize=1)
def build_pb_rules() -> str:
    lines: list[str] = []
    with open(settings.pb_reference_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lines.append(f"- PB Code: {row.get('pb_code', 'PB-UNK')} ({row.get('pb_name', 'Unknown')})")
            lines.append(f"  * Core Definition: {row.get('short_definition', '')}")
            lines.append(f"  * UPV Context: Look for terms like: {row.get('applied_keywords_upv', '')}")
            lines.append(f"  * ACTIVATION LOGIC: {row.get('activation_logic', '')}")
            lines.append(f"  * EXCLUSION RULE (CRITICAL): {row.get('exclusion_notes', '')}")
            lines.append("")
    return "\n".join(lines)


def build_prompt(abstract_text: str) -> str:
    pb_rules = build_pb_rules()
    return f"""You are a strict and precise scientific evaluator analyzing research abstracts from the Universitat Politècnica de València (UPV) against the Planetary Boundaries (PBs) framework.

Your task is to find the PB with the HIGHEST conceptual similarity to the abstract. You must strictly apply the activation rules and evaluate the exclusion rules. Do not force a match if the scientific connection is weak.

### PLANETARY BOUNDARIES RULES:
{pb_rules}

### ABSTRACT TO EVALUATE:
<text>
{abstract_text}
</text>

### INSTRUCTIONS:
Step 1: Concept Extraction. Identify the core scientific concepts, phenomena, or metrics in the abstract.
Step 2: Similarity Matching. Compare these concepts against the Core Definition and Activation Logic of each PB. Select the PB(s) with the strongest scientific overlap.
Step 3: Exclusion Check. Apply the EXCLUSION RULE. If the rule is explicitly violated, the PB MUST be discarded.
Step 4: Output the final decision in JSON format EXACTLY as follows. You must include a \"confidence\" score (High, Medium, or Low) evaluating how strong the match is. Return ONLY valid JSON, without any markdown formatting or extra text.

{{
    \"reasoning_process\": \"Analyze the similarity and evaluate the exclusion rules to justify your decision.\",
    \"assigned_pbs\": [
        {{
            \"pb_code\": \"PB1\",
            \"reason\": \"Justify why this is the highest similarity match.\",
            \"confidence\": \"High / Medium / Low\"
        }}
    ]
}}
If no PB meets the criteria after applying the strict rules, return {{\"reasoning_process\": \"Explain why similarities were too weak or excluded...\", \"assigned_pbs\": []}}.
"""


def parse_llm_output(raw_text: str) -> dict:
    start_idx = raw_text.find("{")
    end_idx = raw_text.rfind("}")
    if start_idx == -1 or end_idx == -1:
        return {
            "reasoning_process": (
                f"No se encontro JSON valido en la salida del modelo {settings.ollama_model_name}."
            ),
            "assigned_pbs": [],
        }

    try:
        payload = json.loads(raw_text[start_idx : end_idx + 1])
        return {
            "reasoning_process": payload.get("reasoning_process", ""),
            "assigned_pbs": payload.get("assigned_pbs", []),
        }
    except json.JSONDecodeError:
        return {
            "reasoning_process": f"Salida JSON invalida en {settings.ollama_model_name}.",
            "assigned_pbs": [],
        }


def run_llm_pb_assessment(abstract_text: str) -> dict:
    if not settings.llm_enabled:
        return {
            "enabled": False,
            "reasoning_process": "LLM deshabilitado por configuracion.",
            "assigned_pbs": [],
            "assigned_pb_codes": [],
            "duration_sec": 0.0,
            "raw_output": "",
        }

    prompt = build_prompt(abstract_text)
    payload = {
        "model": settings.ollama_model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": settings.llm_temperature,
            "top_p": 0.9,
        },
    }

    try:
        started = time.perf_counter()
        response = requests.post(settings.ollama_url, json=payload, timeout=180)
        response.raise_for_status()
        duration_sec = round(time.perf_counter() - started, 3)
        raw_output = response.json().get("response", "")
        parsed = parse_llm_output(raw_output)
        assigned_pbs = parsed.get("assigned_pbs", [])
        assigned_pb_codes = [item.get("pb_code") for item in assigned_pbs if item.get("pb_code")]
        return {
            "enabled": True,
            "reasoning_process": parsed.get("reasoning_process", ""),
            "assigned_pbs": assigned_pbs,
            "assigned_pb_codes": assigned_pb_codes,
            "duration_sec": duration_sec,
            "raw_output": raw_output,
        }
    except Exception as exc:
        return {
            "enabled": True,
            "reasoning_process": f"Error ejecutando {settings.ollama_model_name}: {exc}",
            "assigned_pbs": [],
            "assigned_pb_codes": [],
            "duration_sec": 0.0,
            "raw_output": "",
        }
