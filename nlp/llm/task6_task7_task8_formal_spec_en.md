# Tasks 6-8 Formal Specification (UPV-EARTH, M2)

## Context and Evidence from This Repository

This formalization is grounded on the current project assets:

- Abstract corpus for modeling: [data/corpus/master_corpus_mixto_1000_clean_enriched.csv](../../data/corpus/master_corpus_mixto_1000_clean_enriched.csv)
- Recommended embedding input field: [docs/bert_embeddings_inputs.md](../../docs/bert_embeddings_inputs.md) (`abstract_norm`)
- PB conceptual reference: [corpus_PB/data/pb_reference.csv](../../corpus_PB/data/pb_reference.csv)
- PB textual documents for semantic matching: [corpus_PB/data/pb_corpus_documents.csv](../../corpus_PB/data/pb_corpus_documents.csv)
- Keyword traceability for lexical rules: [corpus_PB/data/pb_keyword_traceability.csv](../../corpus_PB/data/pb_keyword_traceability.csv)
- Existing semantic-scoring implementation: [mockup/backend/app/services/pb_inference/service.py](../../mockup/backend/app/services/pb_inference/service.py)
- Existing embedding model in mockup: [mockup/backend/app/services/embedding_service/service.py](../../mockup/backend/app/services/embedding_service/service.py)
- Existing PB similarity analysis: [scripts/aux/analizar_similitud_embeddings.py](../../scripts/aux/analizar_similitud_embeddings.py)
- Human multi-label validation set: [nlp/llm/validacion_real.csv](validacion_real.csv)

Validation evidence (from [nlp/llm/validacion_real.csv](validacion_real.csv)) confirms this is genuinely multi-label in our case:

- 108 documents
- label cardinality distribution: 1 label (12), 2 labels (21), 3 labels (41), 4+ labels (34)
- average labels per abstract: 2.907

This strongly supports multi-label assignment as the main formulation (not top-1-only).

---

## Task 6. Formalize the Minable View

### 6.1 Formal task definition

We define PB assignment as a multi-label text classification problem:

- sample: one scientific abstract
- input: cleaned abstract text (`abstract_norm`)
- output: subset of labels from {PB1, ..., PB9}
- task type: multi-label classification with semantic ranking and thresholding

Let each sample be $(x_i, Y_i)$ where:

- $x_i$ is the abstract text
- $Y_i \subseteq \{PB1,\dots,PB9\}$ is the set of relevant PB labels

The model returns similarity scores:

$$
\mathbf{s}(x_i) = [s_{i,1}, s_{i,2}, \dots, s_{i,9}], \quad s_{i,j} \in [-1,1]
$$

with cosine similarity between abstract and PB representations.

Predicted labels:

$$
\hat{Y}_i = \{PB_j \mid s_{i,j} \ge \tau_{abs} \; \wedge \; s_{i,j} \ge s_i^{max} - \delta \}
$$

where:

- $\tau_{abs}$ controls absolute semantic confidence
- $\delta$ controls relative closeness to the top PB

Optional safety rule:

- if no label passes thresholds, assign None
- optional fallback for product mode: return top-1 only when score margin is very high

### 6.2 Why this minable view is correct for this project

- The project data and PB ontology are text-centric and semantically rich.
- Existing project code already performs embedding + cosine PB scoring.
- Human validation shows multiple PBs per abstract are common, so single-label is structurally lossy.
- The approach remains explainable by exposing similarity scores and activation/exclusion notes from PB definitions.

### 6.3 Representation choices by method family

- LDA / topic methods: BoW or topic distributions over cleaned lexical text (good for exploration, weaker for fine semantic boundaries).
- BERT-family embeddings: dense vectors from `abstract_norm` and PB texts (main method for M2).
- LLM prompting: reasoning layer or adjudication layer, useful for difficult edge cases and explanations.

Primary M2 representation: BERT-family embeddings, because it best balances semantic quality, reproducibility, and implementation complexity.

---

## Task 7. Build the Baseline

### 7.1 Baseline 1 (Lexical)

A transparent keyword baseline using [corpus_PB/data/pb_keyword_traceability.csv](../../corpus_PB/data/pb_keyword_traceability.csv):

1. Build per-PB keyword sets (core + applied keywords).
2. Compute weighted lexical score per PB:

$$
score_{lex}(PB_j) = w_c \cdot hits_{core} + w_a \cdot hits_{applied}
$$

with $w_c > w_a$ to prioritize conceptual terms.

3. Apply exclusion rules from PB reference when available.
4. Return ranked PBs and optionally multi-label via a lexical threshold.

Why needed:

- fully interpretable
- strong sanity check
- identifies where semantics (BERT) adds value over word overlap

### 7.2 Baseline 2 (Simple semantic)

A centroid or document-level similarity baseline using [corpus_PB/data/pb_corpus_documents.csv](../../corpus_PB/data/pb_corpus_documents.csv):

1. Embed abstract and PB document text (same embedding model).
2. Compute cosine similarities.
3. Assign PB by top-1 or thresholded multi-label.

Why needed:

- simple but semantically stronger than lexical baseline
- directly comparable with the main model pipeline
- already consistent with existing repository logic

### 7.3 Baseline deliverables

- A first PB label table per abstract, including scores and rationale fields.
- Example analyses showing success and failure modes for ambiguous PB pairs.

---

## Task 8. Build the Main Model with BERT / Embeddings

### 8.1 Main pipeline (project-specific)

1. Input selection: use `abstract_norm` from [data/corpus/master_corpus_mixto_1000_clean_enriched.csv](../../data/corpus/master_corpus_mixto_1000_clean_enriched.csv).
2. PB reference text: build PB semantic descriptions from [corpus_PB/data/pb_reference.csv](../../corpus_PB/data/pb_reference.csv) and/or [corpus_PB/data/pb_corpus_documents.csv](../../corpus_PB/data/pb_corpus_documents.csv).
3. Generate embeddings for abstracts and PBs.
4. Compute cosine similarity matrix abstract-to-PB.
5. Multi-label decision with calibrated thresholds ($\tau_{abs}, \delta$).
6. Export outputs: top PB, secondary PBs, full score map, and concise explanation.

This is aligned with the current implementation pattern in [mockup/backend/app/services/pb_inference/service.py](../../mockup/backend/app/services/pb_inference/service.py).

### 8.2 Model selection rationale (BERT, SciBERT, RoBERTa)

Recommended protocol for this corpus:

- Main candidate: SciBERT embedding variant (best domain match for scientific abstracts).
- Strong baseline candidate: RoBERTa sentence embeddings (robust generic semantic performance).
- Additional candidate: BERT-base sentence embeddings (reference baseline).

Why this order:

- abstracts are technical/scientific, so SciBERT should better encode domain terms
- RoBERTa gives a strong non-domain-specific control
- BERT-base ensures comparability and reproducibility

Selection criterion:

- choose the model that maximizes multi-label quality on validation while preserving calibration and interpretability

Primary metrics:

- micro/macro F1 (multi-label)
- Jaccard score
- label ranking average precision
- exact match ratio (reported but not optimized alone)

### 8.3 Decision rule: top-1, top-2, or threshold

For this repository, thresholded multi-label should be the default because human annotation is highly multi-label (avg 2.907 labels).

Recommended operating modes:

- Scientific mode (evaluation): thresholded multi-label
- Product mode (compact UX): top-1 + secondary top-2 display

Practical rule:

- keep PBs with score >= absolute threshold and close to the max score (delta criterion)
- tune thresholds on validation to match observed cardinality and maximize F1/Jaccard

### 8.4 What this main model produces

- final PB classification per abstract (multi-label)
- ranked similarities for all 9 PBs
- transparent evidence to compare against lexical and simple semantic baselines
- a defendable, rubric-compliant central method for M2

---

## Final methodological justification for M2

This formulation is defensible because it is:

- formally specified (sample, input, output, prediction rule)
- empirically aligned with project data (true multi-label behavior)
- reproducible with current repository artifacts
- comparable through clear baselines
- semantically robust through BERT-family embeddings

In short: the main model should be embedding-based multi-label PB classification with calibrated thresholds, benchmarked against lexical and simple semantic baselines.

---

## Addendum. Implemented BERT/Embedding Work and Obtained Results

This section documents what was actually implemented in the repository for the BERT-family track, without changing the formal specification above.

### A. What was implemented

Implementation artifacts:

- Main benchmark script: [nlp/bert_finetuning/pb_backbones_benchmark.py](../bert_finetuning/pb_backbones_benchmark.py)
- Runner notebook: [nlp/bert_finetuning/pb_backbones_benchmark.ipynb](../bert_finetuning/pb_backbones_benchmark.ipynb)
- Usage and outputs guide: [nlp/bert_finetuning/README.md](../bert_finetuning/README.md)
- Generated comparison file: [nlp/bert_finetuning/outputs/backbone_comparison.csv](../bert_finetuning/outputs/backbone_comparison.csv)

Implemented pipeline (end-to-end):

1. Load corpus (`abstract_norm`) from `master_corpus_mixto_1000_clean_enriched.csv`.
2. Load PB semantic text from `pb_corpus_documents.csv`.
3. Compute abstract↔PB similarity scores with:
   - `bert-base-uncased`
   - `roberta-base`
   - `allenai/scibert_scivocab_uncased`
4. Compute baselines:
   - Lexical weighted baseline (`core_keywords` + `applied_keywords_upv`).
   - Semantic TF-IDF baseline.
5. Evaluate three decision policies:
   - top-1
   - top-2
   - threshold+delta (tuned on validation grid)
6. Export predictions and metrics per model:
   - `predictions_all_docs.csv`
   - `predictions_validation.csv`
   - `metrics.json`

### B. Evaluation coverage used in practice

- Human validation file contains 108 annotated records.
- After merging with the current cleaned corpus, usable validation size is 73 records.
- This intersection was used for the benchmark metrics.

### C. Main quantitative results (latest run)

From `nlp/bert_finetuning/outputs/backbone_comparison.csv`:

| Model / Rule | Micro-F1 | Macro-F1 | Jaccard (samples) | Exact Match | Tau | Delta |
|---|---:|---:|---:|---:|---:|---:|
| Lexical baseline (top-2) | 0.4167 | 0.2514 | 0.2934 | 0.0548 | - | - |
| Lexical baseline (threshold+delta) | 0.4110 | 0.2540 | 0.3231 | 0.1370 | 0.20 | 0.00 |
| BERT (threshold+delta) | 0.3804 | 0.3179 | 0.2728 | 0.0548 | 0.75 | 0.02 |
| RoBERTa (threshold+delta) | 0.1023 | 0.0677 | 0.0571 | 0.0000 | 0.20 | 0.00 |
| SciBERT (threshold+delta) | 0.4044 | 0.3087 | 0.2924 | 0.0822 | 0.20 | 0.01 |

### D. Practical interpretation

- Best transformer backbone in this setup: **SciBERT** (threshold+delta micro-F1 = 0.4044).
- `bert-base-uncased` is competitive but below SciBERT on the same policy.
- `roberta-base` underperforms in this raw embedding configuration and should be replaced by a sentence-transformers variant or tuned further.
- The lexical baseline remains strong and interpretable, so it is a meaningful benchmark reference for defending added semantic value.
