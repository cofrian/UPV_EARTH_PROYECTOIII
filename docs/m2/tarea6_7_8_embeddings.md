# Tareas 6-7-8 (M2) - Bloque técnico de embeddings PB

Fecha de actualización: 2026-04-20

## Tarea 6. Minable view formal

- `sample`: un abstract científico.
- `input`: `abstract_norm` (desde `data/corpus/master_corpus_mixto_1000_clean_enriched.csv`).
- `output`: subconjunto de etiquetas `{PB1..PB9}`.
- `task`: clasificación de texto **multietiqueta**.

Regla de predicción implementada:

- `top-1`
- `top-2`
- `multilabel threshold + delta`:
  - mantener `PB_j` si `score_j >= tau_abs` y `score_j >= score_max - delta`
  - fallback opcional a top-1 si ninguna etiqueta pasa el umbral.

## Tarea 7. Baselines implementados

### Baseline 1 (léxico)

- Scoring por coincidencia de keywords PB:
  - `core_keywords` (peso 2)
  - `applied_keywords_upv` (peso 1)
- Fuente: `corpus_PB/data/pb_reference.csv`.

### Baseline 2 (semántico simple)

- TF-IDF (unigramas + bigramas) de abstracts + textos PB.
- Similitud coseno abstract ↔ PB.
- Fuente PB textual: `corpus_PB/data/pb_corpus_documents.csv`.

## Tarea 8. Modelo principal (BERT/RoBERTa/SciBERT)

Pipeline implementado en:

- `nlp/bert_finetuning/pb_backbones_benchmark.py`

Backbones soportados:

- `bert-base-uncased`
- `roberta-base`
- `allenai/scibert_scivocab_uncased`

Proceso:

1. Embeddings de abstracts.
2. Embeddings de documentos PB.
3. Matriz de similitud coseno.
4. Ajuste de `tau_abs` y `delta` por búsqueda en rejilla sobre validación humana.

## Validación y cobertura real

- Validación humana total: 108 documentos (`nlp/llm/validacion_real.csv`).
- Intersección usable con corpus limpio actual: 73 documentos.
- Documentos fuera de intersección: 35 (principalmente por filtros de calidad del pipeline).

## Resultados iniciales (corrida de referencia)

Salida de referencia en:

- `nlp/bert_finetuning/outputs/backbone_comparison.csv`

Lectura rápida:

- Entre los tres backbones, en modo `threshold_delta`, **SciBERT** fue el mejor en `micro_f1` (~0.404).
- BERT quedó por detrás (~0.380).
- RoBERTa base quedó claramente peor en esta configuración (~0.102), lo que sugiere usar una variante sentence-transformers o ajuste supervisado.
- El baseline léxico `top-2` fue competitivo (~0.417), útil como referencia interpretable.

## Artefactos generados

- Comparativa global:
  - `nlp/bert_finetuning/outputs/backbone_comparison.csv`
- Por modelo:
  - `metrics.json`
  - `predictions_all_docs.csv`
  - `predictions_validation.csv`

## Comando reproducible

```bash
./.venv/bin/python nlp/bert_finetuning/pb_backbones_benchmark.py \
  --models bert-base-uncased,roberta-base,allenai/scibert_scivocab_uncased \
  --batch-size 24 \
  --max-length 256 \
  --fallback-top1
```
