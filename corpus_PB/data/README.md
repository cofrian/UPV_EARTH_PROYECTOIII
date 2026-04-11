# data

Esta carpeta contiene los archivos de trabajo del corpus.

## Archivos

- [`pb_reference.csv`](./pb_reference.csv)
Archivo maestro del corpus. Es la referencia principal para cualquier uso posterior.

- [`pb_corpus_documents.csv`](./pb_corpus_documents.csv)
Versión textual derivada para usos computacionales como embeddings, similitud semántica o prompts.

- [`pb_keyword_traceability.csv`](./pb_keyword_traceability.csv)
Archivo de trazabilidad de keywords y reglas de no activación.

- [`lectura_corpus.ipynb`](./lectura_corpus.ipynb)
Notebook auxiliar para exploración, revisión y lectura del corpus.

## Uso recomendado

Si el objetivo es revisar el corpus de forma conceptual, conviene empezar por los PDFs de `../docs/`.

Si el objetivo es programar sobre el corpus:

1. usar `pb_reference.csv` como base;
2. usar `pb_corpus_documents.csv` para tareas textuales;
3. consultar `pb_keyword_traceability.csv` cuando haya dudas sobre por qué una familia de términos está incluida.
