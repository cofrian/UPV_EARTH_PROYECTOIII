# EDA del corpus limpio

- Documentos procesados: **979**
- Documentos con abstract no vacío (trazabilidad): **973**
- Documentos finales tras filtros: **696**

## Longitud de abstracts (abstract_norm)
- mean_chars: **1691.30**
- median_chars: **1552.00**
- p10_chars: **643.50**
- p25_chars: **1061.50**
- p75_chars: **2087.50**
- p90_chars: **2567.00**

## Calidad y nulos (corpus final)
- year: **1.29%** nulos
- doi: **25.72%** nulos
- journal: **10.78%** nulos
- keywords: **43.82%** nulos
- authors: **0.14%** nulos
- abstract_norm: **0.00%** nulos

## Fuentes
- rclone_drive: **696**

## Sesgos / huecos detectados (trazabilidad)
- abstract_too_short<500: **260**
- abstract_empty|language_unknown: **6**
- language_not_english:fr: **4**
- abstract_too_short<500|language_not_english:fr: **2**
- abstract_too_short<500|language_not_english:pt: **2**
- abstract_too_short<500|language_not_english:de: **2**
- language_low_confidence:0.57: **2**
- language_low_confidence:0.55: **1**
- abstract_too_short<500|language_not_english:it: **1**
- abstract_too_short<500|language_not_english:ro: **1**

## Top términos (unigramas)
- climate: 447
- aerosol: 393
- change: 383
- water: 374
- global: 369
- changes: 302
- ozone: 271
- ocean: 267
- land: 257
- species: 252
- carbon: 230
- surface: 227
- atmospheric: 215
- environmental: 206
- system: 194
- emissions: 192
- effects: 186
- systems: 174
- conditions: 171
- production: 169

## Top términos (bigramas)
- climate change: 218
- land cover: 53
- ocean acidification: 52
- boundary layer: 35
- united states: 32
- organic matter: 32
- air quality: 31
- primary production: 30
- organic carbon: 29
- global climate: 29
- ecosystem services: 29
- remote sensing: 28
- biomass burning: 28
- sustainable development: 27
- aerosol optical: 25
- radiative forcing: 23
- greenhouse gas: 22
- global warming: 22
- earth system: 22
- optical depth: 21