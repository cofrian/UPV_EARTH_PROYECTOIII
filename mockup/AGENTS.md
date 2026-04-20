# AGENTS.md

## Objetivo del proyecto
UPV-EARTH v1 es una plataforma web para analisis cientifico del corpus UPV y para inferencia de nuevos papers respecto a los 9 Planetary Boundaries (PBs).

## Arquitectura general
1. Frontend: Next.js + React + TypeScript + Tailwind.
2. Backend: FastAPI modular.
3. Persistencia: PostgreSQL.
4. Proxy: Nginx.
5. Despliegue: Docker Compose.

## Modulos backend
1. pdf_ingestion: validacion, guardado y parsing PDF (PyMuPDF).
2. metadata_extraction: inferencia ligera de metadatos (ej. anio).
3. abstract_extraction: deteccion de abstract por patrones.
4. text_cleaning: normalizacion y limpieza semanticamente conservadora.
5. embedding_service: embeddings sentence-transformers.
6. pb_inference: scoring por similitud abstract vs catalogo PB.
7. summarization: resumen fallback sin LLM (primeras frases).
8. paper_repository: lectura de papers, filtros y detalle.
9. analytics_service: KPIs y distribuciones de dashboard.
10. api: rutas versionadas /api/v1.

## Flujo de datos v1
1. Usuario sube PDF.
2. Se crea processing_job y se almacena el archivo.
3. Job asincro: parse -> abstract -> clean -> embedding -> PB scoring -> summary.
4. Se persisten paper + pb_result.
5. Frontend consulta estado por polling y muestra resultado final.

## Ejecucion local/interna
1. Copiar `.env.example` a `.env`.
2. Levantar stack: `docker compose up -d --build`.
3. Seed inicial del corpus:
   `docker compose exec backend python -m scripts.seed_corpus`
4. Acceder via URL interna configurada (por defecto puerto 80 en host).

## Despliegue en red universitaria
1. Backend escucha en 0.0.0.0 dentro del contenedor.
2. Nginx publica en host y enruta `/api` al backend.
3. Limites de subida y timeouts definidos en nginx.conf.
4. Recomendado publicar con IP/hostname interno y firewall restringido.

## Evolucion por fases
Fase v1 (implementada):
1. Dashboard corpus.
2. Explorador de papers.
3. Upload PDF + inferencia PB + resumen fallback.

Fase futura (diseñada, no implementada):
1. Persistir embeddings por paper.
2. Modulo similarity_search con indice vectorial.
3. Endpoint de vecinos semanticos y posicionamiento relativo del paper.

## Similarity Search (fase futura)
Contrato previsto:
1. `POST /api/v2/similarity/search` con `paper_id` o `abstract`.
2. Respuesta con top-k vecinos, distancia y metadatos.
3. Backend preparado para pgvector o Faiss sin romper API v1.
