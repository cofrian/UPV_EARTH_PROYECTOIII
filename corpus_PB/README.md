# corpus_PB

Corpus de referencia de Planetary Boundaries (PBs) para el proyecto UPV-EARTH.

Esta carpeta reúne de forma autocontenida todo lo desarrollado hasta ahora para la Tarea 2: definición conceptual del corpus, estructura operativa para clasificación de abstracts y documentación legible para revisión humana.

## Qué contiene

El entregable está organizado en tres bloques:

- `data/`: archivos de trabajo del corpus.
- `docs/`: documentación metodológica y versiones legibles del recurso.
- `references/`: papers y documentos usados para construir y justificar el corpus.

## Qué archivo mirar primero

Si alguien entra por primera vez a esta carpeta, el orden recomendado es:

1. [`docs/corpus_pb_methodology.pdf`](./docs/corpus_pb_methodology.pdf)
Describe el corpus con detalle: propósito, fuentes, lógica de activación, explicación de columnas y justificación PB por PB.
2. [`docs/pb_reference_readable_es.pdf`](./docs/pb_reference_readable_es.pdf)
Versión legible en español del recurso maestro para revisión humana rápida.
3. [`docs/pb_reference_readable_en.pdf`](./docs/pb_reference_readable_en.pdf)
Versión legible en inglés del mismo contenido.
4. [`data/pb_reference.csv`](./data/pb_reference.csv)
Archivo maestro del corpus.

## Estructura interna

```text
corpus_PB/
├── README.md
├── data/
│   ├── README.md
│   ├── lectura_corpus.ipynb
│   ├── pb_reference.csv
│   ├── pb_corpus_documents.csv
│   └── pb_keyword_traceability.csv
├── docs/
│   ├── README.md
│   ├── corpus_pb_methodology.tex
│   ├── corpus_pb_methodology.pdf
│   ├── pb_reference_readable_en.pdf
│   └── pb_reference_readable_es.pdf
└── references/
    ├── README.md
    └── documentos fuente del proyecto
```

## Qué hace cada archivo de datos

- [`data/pb_reference.csv`](./data/pb_reference.csv)
Recurso maestro. Contiene una fila por PB y concentra definiciones, variables de control, capas de keywords, lógica de activación y notas de exclusión.

- [`data/pb_corpus_documents.csv`](./data/pb_corpus_documents.csv)
Versión textual derivada del recurso maestro, pensada para similitud semántica, embeddings o prompts.

- [`data/pb_keyword_traceability.csv`](./data/pb_keyword_traceability.csv)
Fichero de trazabilidad. Resume qué señales proceden de los papers del proyecto, qué familias aplicadas se añadieron y qué reglas de no activación deben respetarse.

- [`data/lectura_corpus.ipynb`](./data/lectura_corpus.ipynb)
Notebook auxiliar para exploración y revisión del corpus.

## Principio metodológico central

El corpus distingue tres niveles:

- evidencia fuerte del PB;
- vocabulario aplicado compatible con una universidad como la UPV;
- términos de método o sector que solo aportan contexto.

Esto evita dos errores frecuentes:

- etiquetar como PB cualquier abstract con lenguaje ambiental genérico;
- confundir tecnologías, sectores o herramientas de análisis con evidencia suficiente del límite planetario.

## Resultado

La carpeta queda preparada para ser subida al repositorio de forma clara:

- el trabajo del corpus está autocontenido;
- la documentación está en PDF y en fuente;
- los datos están separados de la documentación y de las referencias;
- el punto de entrada para cualquier revisor está claramente señalado.
