# DESIGN.md

## Direccion visual
Producto cientifico premium con estilo inspirado en Vercel, Supabase y Linear:
1. Dark-first sobrio.
2. Acento verde esmeralda/verde-gris.
3. Jerarquia tipografica limpia y tecnica.
4. Superficies con profundidad sutil y bordes definidos.

## Paleta
1. Fondo base: #040807
2. Panel principal: #0b1310
3. Panel secundario: #111b17
4. Borde: #1e2d27
5. Texto principal: #d9efe5
6. Texto secundario: #93b0a3
7. Acento primario: #38a57a
8. Acento secundario: #1f694e

## Principios de UI
1. No usar layout de admin genrico.
2. Espaciado amplio en dashboards y tarjetas.
3. Tablas legibles con contraste controlado.
4. Estados de carga/error claros y no intrusivos.
5. Componentes reutilizables con variantes consistentes.

## Dashboard
1. KPIs en tarjetas con numerica dominante.
2. Bloques de distribuciones con orden visual estable.
3. Uso consistente de color por categoria de grafico.
4. Seccion de calidad de corpus separada de volumen.

## Exploracion de papers
1. Barra de busqueda visible y filtros combinables.
2. Tabla centrada en lectura rapida: titulo, anio, journal, top PB.
3. Detalle de paper con bloques: abstract, metadatos, scores PB.

## Upload + inferencia
1. Zona de subida clara y segura.
2. Timeline de estados: upload -> parsing -> inferencing -> summarizing -> done.
3. Errores explicitos por etapa.
4. Resultado final con top PB, secundarios, score map y explicacion.

## Motion
1. Aparicion progresiva de cards al cargar.
2. Transicion suave en cambios de estado de job.
3. Evitar animaciones ornamentales.

## Responsive
1. Desktop: grillas de 2-5 columnas para KPIs.
2. Tablet: 2 columnas para cards y graficos.
3. Movil: flujo vertical, tabla con scroll horizontal controlado.

## Accesibilidad
1. Contraste alto en texto y elementos interactivos.
2. Focus visible en botones e inputs.
3. Labels legibles en formularios y estados de proceso.
