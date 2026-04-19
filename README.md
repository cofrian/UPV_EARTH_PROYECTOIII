# UPV_EARTH_PROYECTOIII

Estado actual del trabajo preparado para subir al repositorio del proyecto.

## Documentación

- Guía SSH + VS Code: [docs/guia-ssh-vscode.md](docs/guia-ssh-vscode.md)
- Entorno Python y Jupyter: [docs/entorno-python.md](docs/entorno-python.md)
- Flujo completo de extracción del corpus mixto: [docs/flujo_extraccion_1000.md](docs/flujo_extraccion_1000.md)
- Organización del repositorio (mapa de carpetas): [docs/ORGANIZACION_REPO.md](docs/ORGANIZACION_REPO.md)

## Estructura del proyecto

Distribución actual resumida:

- `data/corpus/`: CSV maestros del pipeline (`clean`, `clean_enriched`, `traceability` y evaluaciones).
- `prompts/`: activos de prompts y contexto de prompt.
- `docs/eda/`: salidas EDA (tablas, figuras y resumen) y `docs/eda/auditoria/` para control de calidad de la muestra final real.
- `muestras/`: listados y muestras seleccionadas (aleatoria y balanceada).
- `scripts/aux/`: scripts auxiliares no críticos para el pipeline principal.
- raíz del proyecto: scripts nucleares de extracción y EDA para mantener compatibilidad de ejecución.

Detalle completo y actualizado en: [docs/ORGANIZACION_REPO.md](docs/ORGANIZACION_REPO.md).

## Flujo de PDFs

El flujo actual ya no es el de 30 PDFs ni el de scripts separados. El procesamiento principal está unificado en [extraccion_corpus_mixto.py](extraccion_corpus_mixto.py) y la explicación completa está en [docs/flujo_extraccion_1000.md](docs/flujo_extraccion_1000.md).

La lista de PDFs sigue generándose con `rclone lsf`, que produce el inventario plano usado por el pipeline:

```bash
mkdir -p /root/proyectoiii/muestras && \
rclone lsf upv_drive: --recursive --files-only --include "*.pdf" > /root/proyectoiii/muestras/listado_pdfs.txt && \
wc -l /root/proyectoiii/muestras/listado_pdfs.txt
```

Ese comando hace tres cosas:

- Crea la carpeta local `muestras/` si no existe.
- Lista de forma recursiva todos los archivos PDF del remoto `upv_drive:` y guarda la salida en `muestras/listado_pdfs.txt`.
- Cuenta las líneas del listado para saber cuántos PDFs se han encontrado.

En otras palabras, `listado_pdfs.txt` es el inventario plano de todos los PDFs accesibles en el remoto, y sirve como base para que el pipeline seleccione la muestra aleatoria de 1000 documentos antes de descargarla con `rclone`.

Ese flujo de 30 documentos fue útil para la fase exploratoria, pero ya quedó sustituido por el pipeline de 1000 documentos con limpieza, deduplicación y trazabilidad.

## Corpus PB

El avance adicional del corpus de Planetary Boundaries está en [corpus_PB/README.md](corpus_PB/README.md).

Ruta recomendada:

1. [corpus_PB/README.md](corpus_PB/README.md)
2. [corpus_PB/docs/corpus_pb_methodology.pdf](corpus_PB/docs/corpus_pb_methodology.pdf)
3. [corpus_PB/docs/pb_reference_readable_es.pdf](corpus_PB/docs/pb_reference_readable_es.pdf)
4. [corpus_PB/docs/pb_reference_readable_en.pdf](corpus_PB/docs/pb_reference_readable_en.pdf)
5. [corpus_PB/data/pb_reference.csv](corpus_PB/data/pb_reference.csv)

## Flujo actual del corpus

El flujo principal del proyecto para extracción de PDFs es el pipeline unificado de 1000 documentos con 3 bloques de descarga, limpieza, deduplicación y trazabilidad. La explicación detallada está en [docs/flujo_extraccion_1000.md](docs/flujo_extraccion_1000.md).

## CSV para BERT embeddings

Para la siguiente fase (BERT/embeddings), usar estos archivos:

1. **Entrada principal recomendada**: [data/corpus/master_corpus_mixto_1000_clean_enriched.csv](data/corpus/master_corpus_mixto_1000_clean_enriched.csv)
2. **Alternativa mínima**: [data/corpus/master_corpus_mixto_1000_clean.csv](data/corpus/master_corpus_mixto_1000_clean.csv)

Referencia detallada de qué columna usar y cuáles no usar para embeddings:

- [docs/bert_embeddings_inputs.md](docs/bert_embeddings_inputs.md)
