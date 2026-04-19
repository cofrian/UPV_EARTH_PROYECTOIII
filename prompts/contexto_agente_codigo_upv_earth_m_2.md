# Contexto completo para agente de código — Proyecto UPV-EARTH (M2)

## 1. Qué es el proyecto

Estamos desarrollando un proyecto de NLP/Data Science llamado **UPV-EARTH: Contribution of UPV Scientific Publications in connection to Planetary Boundaries**.

El objetivo general del proyecto es analizar unas **50.000 publicaciones/abstracts de la Universitat Politècnica de València (UPV)** para estimar **a qué Planetary Boundaries (PBs) se vincula la producción científica de la universidad** y construir una primera visión del perfil investigador institucional respecto a esta agenda.

El proyecto toma como marco conceptual y metodológico tres referencias base:

1. **Paper UPV-SDG**: demuestra que se puede analizar producción científica institucional con IA/NLP y visualizar contribución a agendas globales.
2. **Paper PB–SDG**: aporta el marco conceptual de los 9 Planetary Boundaries y la relación con sostenibilidad.
3. **Paper de Larosa et al. sobre NLP/LLMs en clima/sostenibilidad**: insiste en datos, evaluación, interpretabilidad, validez externa, replicabilidad y utilidad práctica.

---

## 2. Qué buscamos en M2

M2 **no es el proyecto final completo**. En M2 necesitamos demostrar que ya existe una **primera pipeline funcional y documentada**.

### Lo que sí debe quedar hecho en M2

1. **Data preparation**
   - corpus unificado
   - limpieza
   - deduplicación
   - EDA básico
   - dataset final documentado

2. **Minable view / definición formal de la tarea**
   - unidad de análisis = abstract
   - input = `clean_abstract`
   - output = uno o varios PBs
   - tarea = **clasificación multilabel de Planetary Boundaries**

3. **Model building**
   - baseline funcional
   - al menos un modelo principal funcional
   - recomendación principal: **embeddings/BERT como modelo central**

4. **Evaluation**
   - muestra manual anotada
   - primeras métricas
   - análisis preliminar de errores/ambigüedad

5. **Deployment mockup**
   - maqueta o prototipo simple

6. **Justificación de tecnología y AI**
   - explicar por qué se usan baseline, BERT, LDA, Top2VEC y LLMs, aunque no todos estén igual de maduros

### Qué NO es núcleo obligatorio de M2

- conexión completa con datos del Banco Mundial
- clasificación fina del tipo de contribución
- optimización fuerte de Top2VEC
- comparación final exhaustiva de todas las técnicas

---

## 3. Qué datos tenemos realmente ahora mismo

### Situación importante

Actualmente, la fuente disponible operativa que se está manejando es una **carpeta de Google Drive con PDFs de papers**.

Es decir, en este momento **no estamos partiendo necesariamente de un export limpio y estructurado de Scopus/OpenAlex**, sino que es posible que tengamos que construir una primera versión del corpus a partir de **PDFs**.

### Implicación clave

Antes de llegar al NLP puro, hay una fase previa de **document processing / extraction**:

**Drive con PDFs → extracción de metadatos y abstract → tabla corpus → limpieza → NLP**

### Qué debe intentar extraerse de cada PDF

- `file_name`
- `doc_id`
- `title`
- `abstract_raw`
- `doi`
- `year`
- `authors`
- `keywords`
- `journal`
- `source = pdf_drive`
- `extraction_method`
- `quality_flag`

### Qué estrategia usar para PDF parsing

No usar LLM como primera opción.

#### Pipeline recomendada sin LLM

- Python
- `PyMuPDF (fitz)` como librería principal de extracción de texto
- `pdfplumber` como apoyo si algún PDF da problemas
- `re` para regex
- `pandas` para construir la tabla
- `unicodedata` y limpieza básica para normalización textual

### Lógica de extracción desde PDF

Intentar detectar con reglas y patrones editoriales:

- DOI por regex
- año por texto de cabecera o publicación
- título por las primeras líneas grandes de la primera página
- abstract por delimitadores como `Abstract`, `ABSTRACT`, `Introduction`, `INTRODUCTION`, `Keywords`
- keywords por delimitadores `Keywords` / `Key words`
- journal desde cabecera o pie editorial

### Evaluación honesta sobre PDFs

Los ejemplos revisados muestran que muchos papers tienen estructura estándar y permiten extracción rule-based razonable. Aun así:

- DOI, año, journal, keywords y muchos abstracts deberían salir bien
- autores y algunos títulos pueden fallar más
- algunos PDFs pueden requerir revisión manual

### Recomendación metodológica

Si más adelante se consigue export estructurado de Scopus/OpenAlex, deberá preferirse como fuente principal del corpus maestro y usar los PDFs como respaldo o para recuperar abstracts faltantes.

---

## 4. Qué problema modelamos

### Unidad de análisis

La unidad de análisis será **un abstract**.

### Input

`clean_abstract`

### Output

Uno o varios PBs entre los 9 Planetary Boundaries:

1. Climate Change
2. Ocean Acidification
3. Stratospheric Ozone Depletion
4. Biogeochemical Flows
5. Freshwater Use
6. Land-System Change
7. Biosphere Integrity
8. Novel Entities
9. Atmospheric Aerosol Loading

### Tipo de tarea

**Clasificación multilabel**.

Un abstract puede estar asociado a ninguno, uno o varios PBs.

---

## 5. Lógica metodológica del proyecto

### Idea central que debe quedar clara

Aunque el proyecto contempla varias técnicas, el **método principal de M2 está orientado a BERT / embeddings**. Por tanto, una parte esencial del trabajo de corpus consiste en construir el **mejor input posible para representación semántica contextual**.

Esto implica que:
- el corpus no debe limpiarse de forma agresiva si eso destruye semántica útil
- la versión principal del texto debe estar pensada para **embeddings/BERT**
- la extracción, limpieza, filtrado y deduplicación deben hacerse teniendo en cuenta que después el texto será codificado como vectores semánticos y comparado por similitud
- el uso de coseno en el proyecto tiene dos papeles distintos: uno **auxiliar en deduplicación** y otro **central en comparación semántica abstract ↔ PB**

La prioridad metodológica del corpus, por tanto, no es solo “tener textos limpios”, sino **tener textos óptimos para BERT / embeddings**.

## 5. Lógica metodológica del proyecto

El proyecto no depende de una sola técnica. La arquitectura conceptual es esta:

### 5.1 Baseline léxico

Lógica:
- buscar coincidencias entre términos del abstract y términos del corpus PB
- útil como referencia mínima e interpretable

### 5.2 Baseline semántico simple

Lógica:
- medir similitud entre el abstract y las definiciones de cada PB
- puede hacerse con TF-IDF + coseno o embeddings sencillos

### 5.3 BERT / embeddings contextuales

Lógica:
- **método principal recomendado para M2**
- generar representación semántica del abstract
- generar representación semántica de cada PB
- **calcular similitud (por ejemplo, coseno) entre embedding del abstract y embedding del PB**
- asignar etiquetas por top-k o threshold

Este punto debe entenderse como el núcleo técnico del proyecto en M2. El trabajo de corpus debe estar subordinado a este objetivo: producir una entrada textual de alta calidad para que la representación semántica con BERT / embeddings sea lo más fiable posible.

### 5.4 LDA

Lógica:
- descubrir temas latentes del corpus
- usarlo para exploración e interpretación global, no como clasificador principal

### 5.5 Top2VEC

Lógica:
- descubrir clusters semánticos del corpus
- útil para comparación exploratoria con la estructura PB

### 5.6 LLM

Lógica:
- no usar como sistema único en M2
- usar como apoyo para:
  - zero-shot en una muestra
  - revisión de casos ambiguos
  - explicación cualitativa de etiquetas

---

## 6. Diseño recomendado del corpus

No se debe tener una sola columna textual para todo. Se recomienda una arquitectura multicapa.

### Tabla maestra base

Columnas mínimas objetivo:

- `doc_id`
- `source`
- `source_record_id` si existe
- `file_name` si viene de PDF
- `title`
- `abstract_raw`
- `year`
- `doi`
- `authors`
- `keywords`
- `journal`
- `language`

### Columnas textuales derivadas

#### `abstract_norm`
Versión normalizada básica:
- espacios limpios
- saltos de línea corregidos
- Unicode normalizado
- basura editorial eliminada si es trivial

#### `clean_abstract_semantic`
Para:
- **BERT**
- **embeddings**
- similitud semántica
- LLM si hace falta

Esta es la **columna principal del proyecto para el modelo central de M2**.

Regla: limpieza suave, sin destruir semántica.

Objetivo explícito: que el texto conserve suficiente estructura, contexto y contenido conceptual para que un encoder semántico tipo BERT produzca buenas representaciones vectoriales.

#### `clean_abstract_lex`
Para:
- baseline por keywords
- TF-IDF
- LDA
- top términos

Aquí sí se permite:
- lowercase
- tokenización
- stopwords
- opcionalmente lematización

### Flags de calidad recomendados

- `has_abstract`
- `abstract_char_len`
- `abstract_token_len`
- `abstract_quality_flag`
- `pdf_text_ok`
- `quality_score`

### Trazabilidad de extracción recomendada

- `abstract_extraction_method`
- `title_extraction_method`
- `dedup_method`
- `dedup_confidence`

---

## 7. Qué tiene que hacer el agente de código

El agente debe ayudar a construir una pipeline reproducible para pasar de carpeta de PDFs a corpus maestro listo para NLP.

### Bloque A. Ingesta de PDFs

Objetivo:
- recorrer carpeta local con PDFs descargados desde Drive
- leer primera página y/o primeras dos páginas
- extraer texto bruto

### Bloque B. Extracción de metadatos

Objetivo:
- detectar y extraer título
- detectar y extraer abstract
- detectar DOI
- extraer año
- detectar keywords
- extraer nombre de journal si es posible

### Bloque C. Construcción de tabla

Objetivo:
- construir `master_corpus_raw.csv`
- una fila por PDF
- incluir flags de extracción y calidad

### Bloque D. Limpieza

Objetivo:
- crear `abstract_norm`
- filtrar abstracts vacíos
- filtrar abstracts demasiado cortos
- marcar calidad

### Bloque E. Versionado del texto

Objetivo:
- generar `clean_abstract_semantic`
- generar `clean_abstract_lex`

### Bloque F. Deduplicación

Objetivo:
- deduplicar por DOI si existe
- si no hay DOI, deduplicar por título normalizado + año
- usar similitud por coseno como capa auxiliar para generar candidatos sospechosos de duplicado
- guardar trazabilidad del método usado

#### Política recomendada de deduplicación

La deduplicación debe ser jerárquica:

1. **DOI normalizado** como criterio principal de identidad documental.
2. **Coincidencia fuerte de título normalizado + año** cuando no hay DOI.
3. **Similitud por coseno como apoyo**, no como criterio único de deduplicación.

#### Uso correcto del coseno en deduplicación

La similitud por coseno **sí tiene utilidad**, pero debe emplearse para **generar candidatos sospechosos de duplicado** y no para eliminar documentos automáticamente por sí sola.

Debe quedar claro que este uso del coseno es **distinto** del uso principal del coseno en el proyecto.

- En **deduplicación**, el coseno es una herramienta **auxiliar** para detectar registros parecidos.
- En el bloque de **BERT / embeddings**, el coseno será una herramienta **central** para comparar vectores semánticos de abstracts y Planetary Boundaries.

Esto se debe a que una similitud alta puede reflejar que dos papers tratan un tema muy parecido, pero no garantiza que sean exactamente el mismo documento.

#### Recomendación práctica

- aplicar coseno preferentemente sobre **títulos normalizados**
- usarlo solo en casos **sin DOI** o con metadatos imperfectos
- marcar esos pares como candidatos a revisión con campos como:
  - `dedup_method = cosine_candidate`
  - `dedup_confidence = medium` o `low`
  - `needs_review = True`

#### Regla metodológica

El coseno debe entenderse como una herramienta para:
- detectar registros muy parecidos
- apoyar la revisión de casos dudosos
- mejorar la cobertura cuando el título ha salido ligeramente distinto o el parsing del PDF no es perfecto

Pero **no** debe sustituir a DOI o título+año como criterios principales de deduplicación.

### Bloque G. Export final

Objetivo:
- `master_corpus_clean.csv`
- tabla de trazabilidad de filtros
- resumen de recuentos

---

## 8. Reglas metodológicas que el agente debe respetar

### 8.1 No destruir la semántica del texto principal

Para la versión semántica del abstract:
- no usar stemming agresivo
- no quitar stopwords a la fuerza
- no romper puntuación de forma destructiva
- no tokenizar manualmente para BERT

### 8.2 Sí permitir limpieza más fuerte en la versión léxica

Para `clean_abstract_lex` sí se permite:
- lowercase
- tokenización clásica
- stopwords
- lematización opcional

### 8.3 Mantener trazabilidad completa

Cada filtro aplicado debe poder contarse y justificarse.

### 8.4 Priorizar robustez sobre sofisticación

Para M2 importa más:
- una pipeline clara
- bien documentada
- con resultados reproducibles

que una solución muy compleja y frágil.

---

## 9. Qué análisis exploratorio debe salir del corpus final

El agente debe facilitar como mínimo:

- número final de abstracts
- distribución por año
- longitud media/mediana de abstracts
- porcentaje de abstracts válidos
- número de PDFs procesados correctamente
- número de fallos de extracción
- tabla de nulos
- top términos / bigramas en versión léxica

Gráficos mínimos esperables:
- publicaciones por año
- distribución de longitud de abstracts
- tabla o heatmap de nulos

---

## 10. Qué entregables esperamos del bloque de datos/corpus

### Entregable 1
`master_corpus_raw.csv`
- salida directa de la extracción

### Entregable 2
`master_corpus_clean.csv`
- corpus ya filtrado, limpiado y deduplicado

### Entregable 3
`corpus_processing_log.csv` o equivalente
- trazabilidad de extracción, filtros y deduplicación

### Entregable 4
EDA básico
- tablas y gráficos

### Entregable 5
Documento corto de decisiones metodológicas
- cómo se extrajo
- cómo se limpió
- cómo se deduplicó
- qué umbral se aplicó
- qué quedó fuera

---

## 11. Priorización realista para M2

### Lo prioritario

1. Sacar abstracts y metadatos desde PDFs
2. Construir tabla maestra
3. Filtrar y limpiar
4. Deduplicar
5. Generar columnas de texto para modelado
6. EDA básico
7. Documentar todo

### Lo que puede quedar para después

- mejoras avanzadas de extracción
- enriquecimiento con más metadatos
- conexión con otras fuentes
- clasificación fina del tipo de contribución

---

## 12. Resumen ejecutivo para el agente

### Problema
Construir una primera pipeline funcional para transformar una carpeta de PDFs de papers científicos en un corpus usable para una tarea de clasificación multilabel de Planetary Boundaries.

### Input real actual
Carpeta de Google Drive con PDFs.

### Output esperado
Un corpus maestro limpio, deduplicado, documentado y listo para baseline, embeddings/BERT y evaluación preliminar.

### Stack recomendado
Python.

### Librerías recomendadas
- `PyMuPDF`
- `pdfplumber` (opcional de apoyo)
- `re`
- `pandas`
- `unicodedata`
- `pathlib`

### Restricciones metodológicas
- priorizar pipeline reproducible y clara
- no depender de LLM para extracción básica
- mantener trazabilidad
- separar versión semántica y versión léxica del abstract

### Meta de M2
No cerrar el proyecto final completo, sino demostrar una **primera versión funcional y documentada del sistema**.

---

## 13. Instrucción final para el agente

Cuando diseñes o implementes código para este proyecto:

1. asume que la fuente actual son PDFs en Drive
2. prioriza extracción robusta y trazable
3. construye el corpus maestro antes de cualquier modelado
4. separa claramente extracción, limpieza, deduplicación y export
5. deja todo preparado para que después otro bloque pueda aplicar baseline, BERT/embeddings, LDA y evaluación
6. documenta supuestos, fallos y reglas de decisión

