> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Language Policy v3.5

## Objetivo

Determinar uso lingüístico y roles de lenguas por función discursiva, no por
conteo de idiomas detectados.

## Roles

- `CONTENT_LANGUAGE`: lengua que constituye contenido sustantivo del recurso.
- `OBJECT_LANGUAGE`: lengua estudiada o descrita.
- `EXAMPLE_LANGUAGE`: lengua de ejemplos, corpus citado o datos.
- `MENTION_ONLY`: mención incidental.
- `REFERENCE_ONLY`: aparece únicamente en referencias.

## Decisión de languageUsage

### Monolingüe

Usar cuando existe una lengua principal de contenido y las demás aparecen solo
como título paralelo, abstract paralelo, ejemplos, citas o corpus de investigación.

### Bilingüe

Usar cuando dos lenguas constituyen contenido sustantivo del recurso.

### Multilingüe

Usar cuando tres o más lenguas constituyen contenido sustantivo del recurso.

## Reglas de exclusión

No declarar bilingüe únicamente por:

- título paralelo;
- abstract paralelo;
- citas;
- glosas;
- ejemplos;
- testimonios parciales;
- referencias bibliográficas.

## Regla de mapeo

`dc.description.registeredLanguage` describe lenguas registradas según la política
institucional. `dc.subject.linguiscgroup` no debe duplicar mecánicamente todas las
lenguas del contenido: se usa según su función semántica y el contrato local.

Consultar `assets/policy-decisions.json`, especialmente `POL-LANGUSE-*`.


## Extensión v3.5 — lengua del documento vs. lengua objeto

`dc.description.registeredLanguage` se interpreta como lengua de
redacción/registro del recurso. `dc.subject.linguiscgroup` representa la
agrupación lingüística objeto del recurso.

No poblar `registeredLanguage` con todas las lenguas mencionadas o estudiadas.
No poblar `linguiscgroup` con la lengua de redacción salvo que también sea objeto
explícito de estudio.

Para lenguas indígenas de México, consultar
`references/MEXICAN_INDIGENOUS_LANGUAGE_GOVERNANCE.md`.


## Lengua de registro — aclaración v3.9

`dc.description.registeredLanguage` representa la **lengua de escritura/registro
del recurso**.

No debe poblarse con una lengua únicamente porque sea:

- objeto de estudio;
- lengua de ejemplos;
- lengua citada;
- lengua de testimonios/corpus;
- lengua mencionada.

Las lenguas objeto deben modelarse en las dimensiones lingüísticas apropiadas.

La corrección está reforzada por la adjudicación empírica de VERTICAL-021:
un recurso escrito en español que estudia P'urhepecha debe registrar `Español`
en `dc.description.registeredLanguage`, salvo evidencia documental contraria.
