## Plan Refinado: Plataforma UPV-EARTH v1

### 1) Objetivo de la iteración
Entregar una aplicación web profesional y desplegable en red universitaria que permita:
1. Explorar y analizar el corpus UPV ya procesado.
2. Subir un nuevo PDF científico y obtener análisis PB automático.
3. Operar sin dependencia obligatoria de LLM.

### 2) Alcance funcional v1
Incluye:
1. Dashboard analítico del corpus.
2. Explorador de papers con filtros, ordenación, paginación y detalle.
3. Flujo de subida de PDF con procesamiento asíncrono y estados.
4. Resultado de análisis con abstract detectado, resumen, top PB y secundarios.

No incluye en v1:
1. Búsqueda de papers similares.
2. Posicionamiento fino del paper respecto al corpus completo.
3. Índice vectorial operativo para nearest neighbors.

### 3) Principios de arquitectura
1. Núcleo técnico no-LLM:
PDF parsing -> abstract extraction -> limpieza -> embeddings -> scoring PB.
2. LLM opcional:
Resumen y explicación textual enchufables, nunca bloqueantes.
3. Separación estricta por capas:
API, servicios de dominio, repositorio de datos, infraestructura.
4. Trazabilidad total:
Cada job conserva estados, tiempos, errores y versión del modelo.

### 4) Stack y justificación
1. Backend: FastAPI
Motivo: tipado, velocidad, docs OpenAPI y buen soporte de tareas asíncronas ligeras.
2. Frontend: Next.js + React + TypeScript + Tailwind
Motivo: UI profesional, escalabilidad y buen DX para panel analítico.
3. Base de datos: PostgreSQL
Motivo: consistencia relacional, filtros complejos y evolución futura a vector search.
4. PDF parsing: PyMuPDF
Motivo: robustez y rendimiento en extracción de texto.
5. Embeddings: sentence-transformers
Motivo: inferencia semántica PB sin requerir LLM generativo.
6. Reverse proxy: Nginx
Motivo: despliegue estable en red interna, headers, límites y timeouts.
7. Orquestación: Docker Compose
Motivo: despliegue reproducible en infraestructura universitaria.

### 5) Estructura de carpetas objetivo
```text
UPV_EARTH_PROYECTOIII/
  backend/
    app/
      api/
        v1/
          routes/
            analytics.py
            papers.py
            uploads.py
            jobs.py
      core/
        config.py
        logging.py
        security.py
      db/
        base.py
        models/
          paper.py
          pb_result.py
          processing_job.py
          corpus_metric.py
          ingestion_event.py
      schemas/
        paper.py
        analytics.py
        job.py
        upload.py
      services/
        pdf_ingestion/
        metadata_extraction/
        abstract_extraction/
        text_cleaning/
        embedding_service/
        pb_inference/
        summarization/
        analytics_service/
      repositories/
        paper_repository.py
        job_repository.py
        analytics_repository.py
      workers/
        pipeline_runner.py
      main.py
    scripts/
      seed_corpus.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      app/
        dashboard/
        papers/
        upload/
      components/
      lib/
      styles/
    package.json
    Dockerfile
  infra/
    nginx/
      nginx.conf
      site.conf
  data/
    uploads/
    seed/
  AGENTS.md
  DESIGN.md
  README.md
  .env.example
  docker-compose.yml
```

### 6) Modelo de datos v1 (PostgreSQL)

#### Tabla papers
1. id (uuid, pk)
2. doc_id (text, unique)
3. title (text)
4. abstract_raw (text)
5. abstract_norm (text)
6. clean_abstract (text)
7. year (int)
8. doi (text, index)
9. journal (text, index)
10. source (text, index)
11. keywords (text)
12. authors (text)
13. language (text)
14. pdf_path (text)
15. created_at, updated_at (timestamp)

Índices sugeridos:
1. (year)
2. (journal)
3. (source)
4. (doi)
5. gin/trigram para búsqueda textual de title + abstract_norm

#### Tabla pb_results
1. id (uuid, pk)
2. paper_id (fk papers.id)
3. model_version (text)
4. top_pb_code (text)
5. top_pb_score (float)
6. secondary_pbs (jsonb)
7. score_map (jsonb, 9 PB)
8. threshold_used (float)
9. explanation_text (text)
10. created_at (timestamp)

#### Tabla processing_jobs
1. id (uuid, pk)
2. paper_id (nullable fk)
3. filename_original (text)
4. status (queued, uploaded, parsing, inferencing, summarizing, completed, failed)
5. stage (upload, parse_pdf, extract_abstract, clean_text, embedding, pb_scoring, summarize, persist)
6. progress_pct (int)
7. error_code (text)
8. error_message (text)
9. started_at, finished_at (timestamp)
10. created_at (timestamp)

#### Tabla corpus_metrics_cache
1. id (uuid, pk)
2. metric_group (text)
3. metric_key (text)
4. metric_value (jsonb)
5. generated_at (timestamp)

#### Tabla ingestion_events
1. id (uuid, pk)
2. job_id (fk processing_jobs.id)
3. event_type (text)
4. event_payload (jsonb)
5. created_at (timestamp)

Preparado para fase futura:
1. table paper_embeddings (paper_id, embedding vector)
2. table embedding_index_meta
3. extensión pgvector opcional, no activada en v1

### 7) Flujo de usuario v1
1. Usuario entra por URL interna (ej. http://158.42.94.34).
2. Dashboard muestra KPIs y gráficas de corpus.
3. Usuario explora papers con filtros y abre detalle.
4. Usuario sube PDF en página Upload.
5. Frontend inicia job y hace polling de estado.
6. Al completar, frontend muestra resultados PB y resumen.

### 8) Flujo de inferencia v1
1. Validación de archivo (tipo PDF, tamaño máximo, nombre seguro).
2. Guardado de archivo en almacenamiento local seguro.
3. Extracción de texto con PyMuPDF.
4. Detección de abstract con reglas multiformato.
5. Limpieza semánticamente conservadora.
6. Embedding del abstract limpio.
7. Embedding de definiciones PB y cálculo de similitud (cosine).
8. Selección top PB y secundarios por top-k/threshold.
9. Resumen fallback sin LLM (primeras 3-4 frases).
10. Persistencia de resultados y cierre del job.

### 9) API v1 (contrato inicial)

Analytics:
1. GET /api/v1/analytics/overview
2. GET /api/v1/analytics/distribution/pb
3. GET /api/v1/analytics/distribution/year
4. GET /api/v1/analytics/distribution/abstract-length
5. GET /api/v1/analytics/distribution/source

Papers:
1. GET /api/v1/papers?query=&year=&journal=&pb=&doi=&keywords=&sort=&page=&page_size=
2. GET /api/v1/papers/{paper_id}

Uploads y jobs:
1. POST /api/v1/uploads/pdf
2. GET /api/v1/jobs/{job_id}
3. GET /api/v1/jobs/{job_id}/result

Health:
1. GET /api/v1/health

### 10) Frontend v1 (pantallas)
1. Dashboard:
cards KPI + gráficos coherentes + sección calidad de corpus.
2. Papers Explorer:
barra de búsqueda, filtros combinables, tabla premium, detalle lateral o página dedicada.
3. Upload Analyzer:
zona drag-and-drop, línea de estados por etapa, errores legibles.
4. Analysis Result:
PDF name, abstract detectado, resumen, top PB, secundarios, score chart y explicación.

### 11) Diseño visual (base para DESIGN.md)
1. Estética dark-first técnica y elegante.
2. Paleta verde esmeralda/verde-gris como acento.
3. Tarjetas con jerarquía tipográfica clara y espaciado generoso.
4. Tablas limpias con foco en legibilidad científica.
5. Gráficos consistentes en color, escala y semántica.
6. Motion sutil: entrada de cards y transición de estados del job.
7. Responsive real desktop y móvil.

### 12) Procesamiento asíncrono
Decisión v1:
1. FastAPI BackgroundTasks para simplicidad.

Patrón de operación:
1. POST upload devuelve job_id inmediato.
2. Pipeline corre en background.
3. Frontend consulta GET job cada 2-3 segundos.
4. Status final: completed o failed con error explícito.

### 13) Seguridad y red interna
1. Backend bind a 0.0.0.0 dentro del contenedor.
2. Nginx como punto de entrada único.
3. Validación estricta de PDFs y límite de tamaño.
4. Uploads fuera del web root.
5. Cabeceras proxy correctas (X-Forwarded-For, X-Forwarded-Proto).
6. Timeouts y body size ajustados para PDFs científicos.
7. Exposición interna por IP/hostname universitario.

### 14) Despliegue interno (Docker + Nginx)
1. Servicios compose:
- db (PostgreSQL)
- backend (FastAPI)
- frontend (Next.js)
- nginx (reverse proxy)
2. Red interna entre servicios y publicación de nginx al host.
3. URL operativa inicial por IP interna: 158.42.94.34.
4. Preparado para migrar a hostname interno sin cambios de arquitectura.

### 15) Seed de corpus UPV
1. Script backend/scripts/seed_corpus.py toma:
- data/corpus/master_corpus_mixto_1000_clean_enriched.csv
- data/corpus/master_corpus_mixto_1000_traceability.csv
2. Carga papers y métricas base para dashboard inicial.
3. Permite re-seed controlado con modo truncate+reload opcional.

### 16) Entregables concretos
1. backend funcional (FastAPI modular)
2. frontend funcional (Next.js + TS + Tailwind)
3. AGENTS.md
4. DESIGN.md
5. README.md
6. .env.example
7. docker-compose.yml
8. configuración Nginx
9. estructura de carpetas profesional
10. guía de despliegue por URL interna
11. guía de carga inicial del corpus
12. roadmap de fase futura de similares

### 17) Roadmap fase futura (sin implementar ahora)
Fase 2 de producto:
1. Persistencia de embeddings por paper.
2. Activación de índice vectorial (pgvector o faiss).
3. Endpoint de similares por paper.
4. Posicionamiento relativo del nuevo paper frente al corpus UPV.
5. Visualización de vecinos cercanos y mapa semántico.

### 18) Criterios de aceptación v1
1. La app arranca por Docker Compose en servidor interno.
2. Se accede por URL interna y funciona tras Nginx.
3. Dashboard muestra KPIs y distribuciones correctas.
4. Explorador soporta búsqueda, filtros, orden y paginación.
5. Upload PDF funciona con estados de proceso visibles.
6. Se obtiene resultado PB sin LLM obligatorio.
7. El sistema sigue funcionando aunque no exista proveedor LLM.
8. Documentación permite despliegue reproducible por terceros.
