# UPV_EARTH_PROYECTOIII

## Documentacion

- Guia SSH + VS Code: [docs/guia-ssh-vscode.md](docs/guia-ssh-vscode.md)
- Entorno Python y Jupyter: [docs/entorno-python.md](docs/entorno-python.md)
- Flujo completo de extracción del corpus mixto: [docs/flujo_extraccion_1000.md](docs/flujo_extraccion_1000.md)

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

## Flujo actual del corpus

El flujo principal del proyecto ya no es el de 30 PDFs, sino el pipeline unificado de 1000 documentos con 3 bloques de descarga, limpieza, deduplicación y trazabilidad. La explicación detallada está en [docs/flujo_extraccion_1000.md](docs/flujo_extraccion_1000.md).
