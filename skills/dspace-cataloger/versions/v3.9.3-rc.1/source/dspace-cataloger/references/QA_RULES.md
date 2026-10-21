> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Reglas QA v3

## Contrato y vocabulario

| Código | Regla | Severidad |
|---|---|---|
| `CAT-SCHEMA-001` | Alias de `dc.subject.linguiscgroup` | BLOCK |
| `CAT-VOCAB-001` | Valor de campo cerrado no existe en vocabulario asociado | BLOCK |
| `CAT-VOCAB-002` | Forma similar pero no literal; requiere normalización/aprobación | REVIEW |
| `CAT-LING-001` | Familia presente y rama ausente | WARN |
| `CAT-LING-002` | Rama presente y familia ausente | ERROR |
| `CAT-LING-003` | Jerarquía lingüística afirmada sin crosswalk/autoridad | REVIEW |
| `CAT-LING-004` | Variante ortográfica difiere del valor institucional | SUGGESTION |
| `CAT-LANGCODE-001` | Código de lengua ambiguo dentro de `iso6391Pairs` | REVIEW |

## Formularios

| Código | Regla | Severidad |
|---|---|---|
| `CAT-META-001` | `dc.title` ausente | ERROR |
| `CAT-META-002` | `dc.format.extent` ausente en borrador destinado al formulario tradicional | ERROR |
| `CAT-FORM-002` | Dos controles distintos producen valores para `dc.format.medium` sin política de resolución | REVIEW |
| `CAT-FORM-003` | Auto-llenado de `dc.source` pese a conflicto formulario/scope note | REVIEW |
| `CAT-SOURCE-001` | `dc.source` duplica el contenedor ya expresado en `dc.relation.ispartof` | WARN |

## Derechos, sistema y evidencia

| Código | Regla | Severidad |
|---|---|---|
| `CAT-RIGHTS-001` | Licencia inferida solo por disponibilidad web | BLOCK |
| `CAT-SYSTEM-001` | Handle, fecha de ingesta o provenance técnica inventada | BLOCK |
| `CAT-GEO-001` | `countryFound` usado como país de origen/cobertura | ERROR |
| `CAT-ABSTRACT-001` | Resumen generado presentado como resumen original | BLOCK |
| `CAT-DUP-001` | Posible duplicado de registro DSpace | REVIEW |

## Estado global

- `APROBABLE`: sin BLOCK/ERROR pendientes; vocabularios cerrados validados.
- `REQUIERE_REVISIÓN`: al menos un WARN/REVIEW o inferencia sustantiva.
- `BLOQUEADO`: al menos un BLOCK o evidencia primaria insuficiente.


## Adquisición de texto completo

| Código | Regla | Severidad |
|---|---|---|
| `CAT-FULLTEXT-001` | La landing anuncia PDF/XML pero no se intentó consultar antes de cerrar campos dependientes del full text | ERROR |
| `CAT-FULLTEXT-002` | Se afirma haber leído PDF/XML que no fue recuperado | BLOCK |
| `CAT-EVID-001` | Materia/lengua asignada solo desde referencias bibliográficas | BLOCK |
| `CAT-EVID-002` | Una mención incidental se eleva a materia/lengua sin evidencia fuerte | REVIEW |
| `CAT-ABSTRACT-002` | Resumen generado usado como `dc.description.abstract` | BLOCK |
| `CAT-OCR-001` | Valor crítico deriva exclusivamente de OCR incierto sin revisión | REVIEW |


## Ingesta y fusión de fuentes

| Código | Regla | Severidad |
|---|---|---|
| `CAT-INPUT-001` | Archivo subido procesado sin preservar origen/nombre/hash cuando la herramienta permite obtenerlos | REVIEW |
| `CAT-INPUT-002` | EPUB recibe paginación inventada | BLOCK |
| `CAT-FUSION-001` | Discrepancia entre fuentes resuelta silenciosamente | BLOCK |
| `CAT-FUSION-002` | Dato de hoja de cálculo tratado como evidencia primaria sin contraste disponible | REVIEW |
| `CAT-BITSTREAM-001` | Diferencia bitstream↔metadata DSpace sobrescrita sin revisión | BLOCK |


## Reglas derivadas del Golden Set v3.3

| Código | Regla | Severidad |
|---|---|---|
| `CAT-LANGUSE-001` | Título/abstract paralelo usado como única evidencia de bilingüismo | BLOCK |
| `CAT-LANGUSE-002` | `EXAMPLE_LANGUAGE` promovida automáticamente a `CONTENT_LANGUAGE` | BLOCK |
| `CAT-SERIAL-001` | Volumen escrito en `dc.identifier.issue` | BLOCK |
| `CAT-SERIAL-002` | Fuente contiene volumen pero no hay campo de destino en el perfil | REVIEW |
| `CAT-ID-001` | ISBN u otro identificador estructuralmente inconsistente no marcado | REVIEW |
| `CAT-TYPE-001` | Tipo documental derivado únicamente del contenedor | REVIEW |
| `CAT-ABSTRACT-003` | Abstract paralelo descartado sin preservarlo en Evidence Corpus | REVIEW |
| `CAT-RIGHTS-002` | Copyright restrictivo usado para inferir automáticamente `accessRights` | BLOCK |
| `CAT-LINK-001` | Fila sin URL declarada `FULLTEXT_UNAVAILABLE` sin intentar recuperación bibliográfica | ERROR |
| `CAT-GAP-001` | Concepto verificado sustituido por término parecido del vocabulario para evitar un gap | BLOCK |
| `CAT-ROLE-001` | Rol fuente perdido al mapear a un contributor genérico | REVIEW |
| `CAT-EXTENT-001` | Conteo físico del PDF usado como extensión cuando existe paginación bibliográfica | REVIEW |

## UI Fidelity y contenido generado v3.4

| Código | Regla | Severidad |
|---|---|---|
| `CAT-UI-001` | Etiqueta conocida de la UI sustituida silenciosamente por una traducción/genérico distinto | REVIEW |
| `CAT-UI-002` | Dos bindings distintos colapsados por compartir `metadataField` | ERROR |
| `CAT-UI-003` | Salida estructurada ambigua omite `bindingId` cuando una clave tiene múltiples controles | REVIEW |
| `CAT-GEN-001` | Contenido redactado por el asistente presentado como `EXTRAÍDO`/`VERIFICADO` | BLOCK |
| `CAT-GEN-002` | Contenido `GENERADO` se mapea automáticamente a un campo cuya política exige evidencia original | BLOCK |



## Gobernanza y aprendizaje v3.5

| Código | Regla | Severidad |
|---|---|---|
| `CAT-LING-005` | Recurso multientidad serializado sin preservar internamente relaciones familia–rama–agrupación–variante | REVIEW |
| `CAT-LING-006` | Rama lingüística tratada como nivel normativo CLIN o asignada sin autoridad secundaria | REVIEW |
| `CAT-LING-007` | `registeredLanguage` confundida con lengua objeto de estudio (`linguiscgroup`) | ERROR |
| `CAT-LING-008` | Topónimo/región convertido en variante lingüística sin reconciliación CLIN | BLOCK |
| `CAT-VOCAB-004` | Valor ausente sustituido por la opción más cercana para evitar un gap | BLOCK |
| `CAT-ABSTRACT-004` | Abstract autoral disponible sustituido por paráfrasis generada | BLOCK |
| `CAT-SUBJ-002` | Término inferido presentado como palabra clave autoral | BLOCK |
| `CAT-GEO-002` | `countryFound` inferido desde sede editorial, dominio o afiliación | REVIEW |
| `CAT-DATE-001` | Online-first, fecha de fascículo, recepción o aceptación confundidas sin política de selección | REVIEW |
| `CAT-TITLE-001` | Título dividido en subtítulo solo por contener dos puntos | REVIEW |


## Reglas VERTICAL-021 — v3.9

| Código | Regla | Severidad |
|---|---|---|
| `CAT-LANG-REG-001` | `dc.description.registeredLanguage` se usa para una lengua objeto/estudiada sin evidencia de que sea lengua de escritura del recurso | BLOCK |
| `CAT-LLM-001` | Una salida LLM se promueve automáticamente a `EXTRAÍDO` o `VERIFICADO` | BLOCK |
| `CAT-LLM-002` | El modelo impone `metadata_field` o usa un `binding_id` desconocido/no permitido | BLOCK |
| `CAT-LLM-003` | Existe egress a proveedor sin política explícita aprobada/evaluable, o con decisión `deny/indeterminate` | BLOCK |
| `CAT-LLM-004` | Un candidato LLM se copia automáticamente al draft sin acción humana explícita | BLOCK |
| `CAT-LLM-005` | Una corrida LLM usa Evidence Session stale o evidencia fuera del input manifest congelado | BLOCK |
| `CAT-EVAL-001` | `ADJUDICATED_GOLD` se interpreta como permiso de escritura, OCR, egress o verificación automática | BLOCK |
| `CAT-EVAL-002` | Review/adjudicación pierde igualdad de `case_id`, `binding_id`, reviewer membership o evidence snapshot | ERROR |
