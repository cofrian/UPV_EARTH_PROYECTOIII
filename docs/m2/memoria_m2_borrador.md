# M2 - Memoria del Proyecto UPV Earth

## 1. Introduccion

Este entregable corresponde al milestone M2 y resume el estado actual del proyecto, los resultados obtenidos hasta la fecha y las acciones planificadas para completar el prototipo con mayor robustez metodologica. El objetivo global del proyecto es analizar y estructurar un corpus cientifico vinculado a los 9 Planetary Boundaries (PB), para materializar una vista minable y evaluar modelos de clasificacion multietiqueta que den soporte a una futura herramienta de consulta y analisis.

## 2. Data Preparation (hecho)

### 2.1 Recoleccion e integracion de datos

Se trabajo sobre un corpus mixto de articulos cientificos en PDF, organizado en torno a los 9 Planetary Boundaries. El objetivo no era solo acumular documentos, sino convertirlos en un corpus trazable y reutilizable para analitica, modelado y despliegue.

El flujo de integracion deja tres artefactos principales:

- corpus limpio para analisis y entrenamiento,
- corpus enriquecido con campos derivados para EDA y busqueda,
- tabla de trazabilidad con el estado de filtrado, limpieza y mapeo PB.

Activos de datos clave en M2:

- corpus limpio para analitica y entrenamiento,
- corpus enriquecido para EDA y explicabilidad,
- trazabilidad de filtros y decisiones de preparacion.

### 2.2 Limpieza, control de calidad y cobertura del corpus

Se aplicaron operaciones orientadas a conservar la informacion semantica del texto y eliminar ruido tecnico/editorial:

- normalizacion de abstracts y metadatos,
- eliminacion de duplicados y registros no aprovechables,
- descarte de documentos con texto insuficiente (abstracts con menos de 500 caracteres),
- revision de valores nulos y consistencia de campos,
- mapeo de cada documento a pb_folder como etiqueta objetivo,
- construccion de columnas derivadas para el analisis posterior.

La muestra final usada en la version actual es de 696 abstracts. La distribucion por PB es relativamente equilibrada, con rangos de 66 a 90 documentos por categoria, lo que reduce el riesgo de sesgo fuerte por frecuencia y permite comparar clases con una base razonable.

### 2.3 Evidencia EDA generada para M2

Para entender el corpus antes del modelado se produjeron tres vistas complementarias:

1. Vocabulario caracteristico por PB con TF-IDF sobre clean_abstract.
2. Distribucion de complejidad textual por PB, medida como longitud de abstracts.
3. WordCloud individual por PB con filtrado de terminos genericos y lectura comparativa.

Adicionalmente se incorporaron analisis de similitud para detectar PB potencialmente confusos:

- similitud por terminos TF-IDF extraidos,
- similitud por corpus completo,
- similitud por embeddings semanticos, para capturar proximidad por significado y no solo por coincidencia lexical.

Resultados EDA relevantes:

- Se verifico consistencia semantica por PB mediante vocabulario caracteristico.
- Se identifico heterogeneidad de complejidad textual entre categorias.
- Se detectaron pares de PB con mayor riesgo de confusion (lexical y semantica).
- Se consolidaron evidencias visuales por PB para justificar decisiones de modelado.

Hallazgos cuantitativos clave integrados en el EDA:

- El corpus final analizable quedo en 696 documentos tras limpieza y filtros de calidad.
- La cobertura por PB se mantuvo en un rango aproximado 66-90 documentos por categoria, evitando desequilibrios extremos.
- En similitud semantica, los pares mas proximos fueron Biogeochemical Flows vs Global Freshwater Use (0.896), Stratospheric Ozone Depletion vs Atmospheric Aerosol Loading (0.866) y Ocean Acidification vs Biogeochemical Flows (0.856), lo que adelanta las zonas de mayor confusión esperada en evaluación.

Las tablas y graficos de soporte tecnico se mantienen en el repositorio como anexo reproducible, pero en esta memoria se prioriza la interpretacion metodologica y la toma de decisiones derivada del EDA.

### 2.4 Como el EDA aporta a la rubrica

El EDA no se uso como paso descriptivo aislado, sino como mecanismo de validacion para la tarea de clasificacion:

- Data preparation: permitio verificar cobertura, balance y calidad del texto antes del entrenamiento.
- Minable view: confirmo que la unidad documental y las variables textuales contienen senal discriminativa.
- Model building: justifico el uso combinado de representaciones TF-IDF y embeddings.
- Evaluation: adelanto zonas de confusion esperadas para orientar la lectura de la matriz de confusion.

Este enfoque conecta directamente analitica exploratoria con decisiones tecnicas, que es uno de los puntos clave para alcanzar una valoracion alta en la rubrica.

## 3. Task Description y Minable View (hecho + afinado)

Bloque tecnico formal de Tareas 6-7-8 (minable view, baselines y benchmark BERT/RoBERTa/SciBERT):

- `docs/m2/tarea6_7_8_embeddings.md`

### 3.1 Definicion de la tarea

La tarea principal del proyecto se define como clasificacion multietiqueta o multicategoria de documentos cientificos en torno a los Planetary Boundaries, con posible extension a recuperacion semantica y analisis explicativo de contenidos.

### 3.2 Vista minable

La vista minable actual se materializa con:

- Entrada principal: texto de abstract limpio (clean_abstract).
- Variables de contexto: year, source, journal, keywords (cuando existen).
- Variable objetivo: pb_folder (9 categorias de PB).

Para la fase de embeddings, la columna recomendada pasa a `abstract_norm` del CSV enriquecido.

Esta definicion permite:

- entrenamiento de modelos supervisados,
- comparacion de arquitecturas clasicas vs embeddings,
- explicabilidad mediante terminos TF-IDF y distribuciones por clase.

### 3.3 Hallazgos tempranos de la vista minable

El corpus esta relativamente balanceado por PB (entre 66 y 90 documentos por categoria), lo que favorece comparaciones iniciales entre clases sin sesgos extremos de frecuencia.

## 4. Model Prototype and Evaluation (estado actual)

### 4.1 Prototipo de modelado en curso

El prototipo de modelado se apoya en dos niveles complementarios. Primero, una representacion textual interpretable basada en TF-IDF, que permite una primera linea de clasificacion y explicabilidad. Segundo, una representacion semantica basada en embeddings, que ayuda a medir proximidad entre PB por significado y no solo por palabras compartidas.

La idea del prototipo no es solo predecir, sino dejar una base de comparacion justificable para la fase final: saber que PB son faciles de separar, cuales se solapan y donde hace falta mas supervision o mejores variables.

### 4.2 Evaluacion (estado)

En esta fase se han definido las piezas para evaluacion y analisis de error, con foco en una metodologia reproducible. La memoria ya contempla:

- metricas por clase y agregadas,
- matriz de confusion interpretada,
- comparacion entre representaciones textuales,
- lectura de zonas de duda entre PB.

La evaluacion final debe apoyarse en un protocolo adecuado al problema multiclase/multietiqueta y en una repeticion suficiente para evitar conclusiones fragiles.

## 5. Nuevos resultados analiticos para justificar decisiones

### 5.1 Vocabulario caracteristico por PB

El corpus muestra vocabularios claramente alineados con cada dominio. Los terminos obtenidos por TF-IDF no son solo palabras frecuentes, sino senales utiles para explicar por que un documento cae en una categoria y no en otra.

Ejemplos representativos:

- Climate Change: climate, change, temperature, global.
- Ocean Acidification: ocean, acidification, coral, reef.
- Stratospheric Ozone Depletion: ozone, stratospheric, emissions, chemistry.
- Global Freshwater Use: water, freshwater, rivers.
- Land System Change: land, cover, use, forest.
- Atmospheric Aerosol Loading: aerosol, cloud, dust, radiative.

### 5.2 Complejidad del texto por PB

La longitud de los abstracts no es homogenea. Algunas PB concentran textos mas tecnicos y extensos, mientras que otras tienden a explicaciones mas compactas. Esto importa porque condiciona la representacion textual y el preprocesado, especialmente si despues se usan modelos supervisados o embeddings.

### 5.3 WordCloud por PB

La WordCloud por PB se construyo sobre clean_abstract y campos auxiliares, eliminando terminos genericos para evitar que palabras editoriales o academicas dominen la visualizacion. El resultado es una vista mas util para comparar temas y no solo estilos de redaccion.

### 5.4 Similitud entre PB y posibles zonas de duda

Se anadieron tres analisis complementarios para entender la separabilidad real entre PB:

1. Similitud por terminos TF-IDF extraidos.
2. Similitud por corpus completo usando centroides TF-IDF.
3. Similitud por embeddings semanticos con sentence-transformers.

Este ultimo nivel es el mas importante para interpretar confusiones reales, porque aproxima el significado del texto y no depende tanto de palabras exactas.

Los pares mas proximos detectados fueron:

- Biogeochemical Flows vs Global Freshwater Use (0.896 en embeddings semanticos).
- Stratospheric Ozone Depletion vs Atmospheric Aerosol Loading (0.866 en embeddings semanticos).
- Ocean Acidification vs Biogeochemical Flows (0.856 en embeddings semanticos).
- Climate Change vs Land System Change (0.849 en embeddings semanticos).

En terminos metodologicos, esto indica que los limites mas sensibles del problema estan en los grupos relacionados con agua, nutrientes, atmosfera y cambio global/uso del suelo. Son precisamente los pares que deberian recibir mas atencion en la evaluacion final.

## 6. Deployment Mockup (estado)

El mockup no es solo una demo visual. Es una primera arquitectura operativa para responder a la pregunta central del proyecto: si el flujo puede funcionar en un entorno real de uso.

### 6.1 Arquitectura del mockup

La aplicacion se organiza en cuatro capas:

- Frontend: Next.js + React + TypeScript + Tailwind.
- Backend: FastAPI modular.
- Persistencia: PostgreSQL en el stack principal, con SQLite para ejecucion local ligera.
- Infraestructura: Docker Compose y Nginx como reverse proxy.

En la version de desarrollo y validacion rapida tambien se habilito ejecucion local sin Docker para facilitar pruebas iterativas y depuracion. La configuracion dockerizada se mantuvo como forma de empaquetado y de despliegue reproducible, pero no fue la unica forma de operar el prototipo.

La definicion de esta arquitectura se apoyo explicitamente en la documentacion interna del mockup, especialmente en AGENTS.md para la division modular del backend y el flujo de datos, y en DESIGN.md para fijar la direccion visual, la jerarquia de componentes y los principios de la interfaz.

### 6.2 Flujo funcional de la aplicacion

El flujo de extremo a extremo es el siguiente:

1. El usuario sube un PDF desde el frontend.
2. El backend crea un processing_job y guarda el fichero.
3. Un pipeline asincrono realiza parsing, extraccion de abstract, limpieza, embeddings, scoring PB y resumen.
4. Se persisten paper, pb_result y eventos del job.
5. El frontend consulta el estado por polling y muestra el resultado final, incluyendo scores, explicacion y metadatos.

### 6.3 Backend y persistencia

El backend esta modularizado para separar responsabilidades:

- pdf_ingestion: validacion y guardado de PDFs.
- abstract_extraction: deteccion del abstract.
- text_cleaning: normalizacion conservadora del texto.
- embedding_service: calculo de embeddings semanticos.
- pb_inference: scoring y asignacion PB.
- summarization: resumen fallback cuando no hay LLM.
- paper_repository: consultas, filtros y detalle de papers.
- analytics_service: KPIs y distribuciones del dashboard.

La persistencia central usa una base de datos relacional para guardar papers, resultados PB y eventos. El sistema esta preparado para ejecutarse de forma local o bajo contenedores, y para almacenar uploads y semillas de runtime dentro de mockup/data.

### 6.3.1 Contrato API (resumen de endpoints)

La API esta versionada bajo /api/v1 y se organiza por dominios funcionales. Endpoints principales implementados:

- Salud del servicio:
	- GET /api/v1/health
- Upload e inferencia:
	- POST /api/v1/uploads/pdf
- Jobs de procesamiento:
	- GET /api/v1/jobs/{job_id}
	- GET /api/v1/jobs/{job_id}/result
	- GET /api/v1/jobs/{job_id}/events
- Exploracion de papers:
	- GET /api/v1/papers
	- GET /api/v1/papers/{paper_id}
- Analitica y dashboard:
	- GET /api/v1/analytics/overview
	- GET /api/v1/analytics/distribution/pb
	- GET /api/v1/analytics/distribution/year
	- GET /api/v1/analytics/distribution/source
	- GET /api/v1/analytics/distribution/abstract-length
	- GET /api/v1/analytics/keywords/global
	- GET /api/v1/analytics/keywords/pb/{pb_code}
	- GET /api/v1/analytics/papers/{paper_id}/comparison
	- GET /api/v1/analytics/runtime/metrics

Este diseno permite separar claramente operaciones de ingestion, consulta, monitorizacion y analitica sin mezclar responsabilidades entre rutas.

### 6.3.2 Persistencia y entidades de datos

A nivel de modelo de datos, el backend persiste al menos las siguientes entidades:

- Paper: metadatos y texto procesado del documento.
- PBResult: scoring y clasificacion por Planetary Boundary.
- ProcessingJob: estado y trazabilidad del pipeline asincrono.
- IngestionEvent: eventos por etapa durante el procesamiento.
- CorpusMetric: metricas agregadas para dashboard y seguimiento.

Este esquema permite trazabilidad completa de cada PDF desde su entrada hasta su resultado final, y facilita auditoria de calidad y analisis posterior de errores.

### 6.4 Infraestructura y despliegue

Docker Compose orquesta el stack completo y Nginx actua como punto de entrada para enrutar el trafico hacia el backend. Este enfoque simplifica el despliegue, reduce acoplamientos y deja la demo lista para una presentacion controlada.

### 6.5 Papel de la IA en el mockup

Se utilizo asistencia de IA tipo Copilot/Codex para acelerar la construccion de una PoC inicial, pero no como generacion masiva sin control. La metodologia fue iterativa: primero se planifico la arquitectura y el flujo funcional, despues se pidieron piezas concretas a la IA, se revisaron los resultados y se volvieron a ajustar las instrucciones hasta que el codigo siguio exactamente lo solicitado.

Ese uso por iteraciones fue util para tareas repetitivas de estructuracion, integracion y redaccion tecnica, pero la decision metodologica, la validacion de resultados y el control de calidad siguieron siendo manuales.

## 7. Use of Technology y autonomia

Herramientas empleadas:

- Python para pipeline de extraccion, limpieza, EDA, similitud y apoyo al modelado,
- pandas, numpy, matplotlib, seaborn, scikit-learn y wordcloud para analitica,
- sentence-transformers para comparacion semantica de PB,
- FastAPI, Next.js, PostgreSQL, Nginx y Docker para la capa de producto,
- estructura reproducible de scripts, datos de trazabilidad y artefactos en docs/eda.

La estrategia tecnica muestra autonomia en la integracion de herramientas distintas, en la resolucion de bloqueos y en la construccion de un flujo reproducible desde el corpus hasta la demo.

## 8. Uso de seminarios y de IA

Se han aplicado conceptos del curso en:

- preparacion de datos y control de calidad,
- definicion de vista minable,
- prototipado y evaluacion inicial,
- despliegue de una aplicacion demostrable con backend, frontend y persistencia,
- analisis de similitud y explicabilidad sobre el corpus.

El uso de IA se ha orientado a acelerar una primera PoC y a producir codigo y redaccion de forma iterativa, pero sin sustituir el criterio tecnico del equipo. La validacion de la salida, las decisiones sobre el corpus y la interpretacion de resultados se revisaron manualmente.

En particular, la IA se uso como apoyo por iteraciones guiadas: primero se definia el objetivo, luego se solicitaba una pieza concreta, despues se corregia la salida hasta que encajara con la arquitectura y el estilo del proyecto. Eso permitio avanzar rapido sin perder trazabilidad ni control del resultado final.

## 9. Conclusiones

El trabajo realizado deja tres resultados fuertes para M2: un corpus limpio, trazable y suficientemente equilibrado; una vista minable bien definida con variables de entrada y salida claras; y un mockup tecnico que demuestra como podria funcionar la solucion en un escenario real.

La principal lectura metodologica es que los PB no se separan solo por palabras, sino por estructuras tematicas y semanticas diferentes. Por eso se combinaron TF-IDF, distribuciones de complejidad, similitud por corpus y embeddings semanticos, obteniendo una base mucho mas solida para justificar la fase de modelado final.

En paralelo, el mockup aporta valor de producto: muestra el flujo completo desde la subida del documento hasta la inferencia PB, con persistencia, eventos de proceso, explicacion y salida util para usuario final. Eso permite responder a la pregunta de la rubrica: si, la solucion puede funcionar y puede explicarse con criterio tecnico.

## Anejo A. Plan de trabajo

1. Cerrar pipeline de entrenamiento final con un protocolo de validacion robusto.
2. Comparar al menos dos enfoques de modelado, combinando un baseline interpretable con un enfoque de embeddings o LLM.
3. Reportar metricas detalladas por PB y una matriz de confusion interpretada.
4. Integrar resultados clave del modelo en el mockup para demostracion funcional.
5. Sintetizar la discusion final con limites, riesgos de sesgo y mejoras futuras.
