# UPV-EARTH Mockup v1

Esta carpeta contiene toda la aplicacion web (backend, frontend, infraestructura y docs de despliegue) para mantener limpio el repo principal.

## Contenido
- backend/: FastAPI + pipeline PDF -> PB.
- frontend/: Next.js + TypeScript + Tailwind.
- infra/nginx/: reverse proxy.
- data/uploads/: PDFs subidos.
- data/seed/: archivos auxiliares de seed.
- docker-compose.yml: orquestacion completa.
- .env.example: variables de entorno.
- AGENTS.md y DESIGN.md: arquitectura y sistema visual.

## Arranque
1. Copiar variables:
   cp mockup/.env.example mockup/.env
2. Levantar stack:
   docker compose -f mockup/docker-compose.yml --env-file mockup/.env up -d --build

## Ejecucion sin Docker
1. Backend local (SQLite):
   export DATABASE_URL='sqlite:////home/sortmon/UPV_EARTH_PROYECTOIII/mockup/data/seed/upvearth_local.db'
   export UPLOAD_DIR='/home/sortmon/UPV_EARTH_PROYECTOIII/mockup/data/uploads'
   export PB_REFERENCE_CSV='/home/sortmon/UPV_EARTH_PROYECTOIII/corpus_PB/data/pb_reference.csv'
   /home/sortmon/UPV_EARTH_PROYECTOIII/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
2. Frontend local:
   export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/sortmon/UPV_EARTH_PROYECTOIII/.nodeenv/bin'
   export NEXT_PUBLIC_API_BASE_URL='/api/v1'
   export API_BASE_URL_INTERNAL='http://127.0.0.1:8000/api/v1'
   npm run dev -- --hostname 0.0.0.0 --port 3000

## Seed del corpus UPV
1. Ejecutar seed inicial:
   docker compose -f mockup/docker-compose.yml --env-file mockup/.env exec backend python -m scripts.seed_corpus

## URL interna
- Acceso inicial por IP interna:
  http://158.42.94.34

## Gemma / Ollama
- El pipeline de subida de PDF invoca Gemma por defecto.
- Variables relevantes:
   - `LLM_ENABLED=true` (poner `false` para desactivar)
   - `OLLAMA_URL=http://127.0.0.1:11434/api/generate`
   - `OLLAMA_MODEL_NAME=gemma4:26b`
   - `LLM_TEMPERATURE=0.0`
- El resultado de Gemma se incorpora al `explanation_text` del resultado PB y se registra en eventos del job (`llm_reasoning`).

## Nuevos endpoints analiticos
- `GET /api/v1/analytics/keywords/global?limit=12`
- `GET /api/v1/analytics/keywords/pb/{pb_code}?limit=12`
- `GET /api/v1/analytics/papers/{paper_id}/comparison`
- `GET /api/v1/jobs/{job_id}/events?limit=200` (eventos del pipeline + metricas runtime CPU/RAM/GPU)

## Notas de rutas
- El stack usa datos reales del repo padre en modo solo lectura:
  - ../data/corpus -> /app/data/corpus
  - ../corpus_PB -> /app/corpus_PB
- Uploads y seed de runtime se guardan dentro de mockup/data.
