# Entorno Python del proyecto

Esta guia deja el proyecto preparado para trabajar con Python 3.11, un entorno virtual aislado, Jupyter y el cliente de Ollama.

## Estructura recomendada

- `.venv/`: entorno virtual local, no se sube a Git.
- `pyproject.toml`: metadatos del proyecto y dependencias base.
- `data/raw/`: datos de entrada sin versionar.
- `docs/`: documentacion del flujo de trabajo.

## Requisitos

- Python 3.11 instalado en la maquina.
- `pip` disponible para ese interprete.

## Crear el entorno virtual

Desde la raiz del repo:

```bash
/root/.local/python-3.11.12/bin/python3.11 -m venv .venv
```

## Activar el entorno

```bash
source .venv/bin/activate
```

Para salir:

```bash
deactivate
```

## Instalar dependencias

Con el entorno activado:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Eso instala JupyterLab, ipykernel y el cliente de Ollama desde `pyproject.toml`.

## Abrir Jupyter

```bash
jupyter lab
```

Si prefieres usar el binario del entorno:

```bash
.venv/bin/jupyter lab
```

## Usar Ollama desde Python

Con el servicio de Ollama activo en la maquina, puedes probar una llamada basica asi:

```bash
python - <<'PY'
from ollama import chat

response = chat(
	model="llama3.1:8b",
	messages=[
		{"role": "user", "content": "Di hola en una frase corta"},
	],
)

print(response.message.content)
PY
```

Si el modelo no esta descargado aun, primero haz:

```bash
ollama pull llama3.1:8b
```

Y si quieres comprobar que el servicio responde:

```bash
ollama list
```

## Kernel para notebooks

Si quieres dejar un kernel identificado para VS Code o Jupyter:

```bash
python -m ipykernel install --user --name upv-earth-proyectoiii --display-name "Python 3.11 (UPV Earth)"
```

## Datos

- Guarda los datos originales en `data/raw/`.
- No subas datos crudos al repositorio.
- Si necesitas resultados intermedios o limpios, crea carpetas separadas como `data/processed/` o `data/interim/`.

## Reglas de Git

El archivo `.gitignore` ya excluye:

- entornos virtuales (`.venv/`, `venv/`, `env/`).
- caches de Python y Jupyter.
- archivos de configuracion local.
- la carpeta `data/raw/`.
