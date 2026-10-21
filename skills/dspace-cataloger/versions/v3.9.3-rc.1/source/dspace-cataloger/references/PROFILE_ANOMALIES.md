> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Anomalías y ambigüedades del perfil

Estas observaciones proceden del perfil real y deben impedir normalizaciones
silenciosas.

## 1. Duplicados en `linguisticFamilyPairs`

La lista contiene duplicados literales para:

- `Indoeuropeo`
- `Álgica`

La validación de membresía sigue siendo válida, pero el agente debe deduplicar
solo en la presentación, nunca reescribir el vocabulario de DSpace.

## 2. `registeredLanguagePairs` y `linguiscgroupPairs`

Ambos tienen 256 entradas, pero **no son listas idénticas**. No se deben tratar
como alias ni copiar automáticamente un valor de una a otra.

## 3. Jerarquía lingüística no codificada

El snapshot confirma las listas permitidas de familia, rama, agrupación y lengua,
pero no incluye un crosswalk explícito que indique:

`lengua → agrupación → rama → familia`

Por tanto:

- validar membresía: sí;
- validar jerarquía solo por presencia en listas: no;
- una jerarquía propuesta requiere autoridad/crosswalk o inferencia marcada.

## 4. `dc.language.iso6391`

El campo se etiqueta como “ISO 639-1”, pero su vocabulario `iso6391Pairs`
contiene valores de distinta longitud, incluyendo formas como `spa` y `eng`
junto con `es`, `en`, etc.

No “corregir” automáticamente. Marcar `CAT-LANGCODE-001` cuando haya más de un
código institucional plausible para la misma lengua.

## 5. Colisión en `dc.format.medium`

`traditionalpageone` usa la misma clave para dos controles:

- Soporte → `mediumPairs` (opcional)
- Tipo de extensión → `extentTypePairs` (obligatorio)

No asumir que son semánticamente equivalentes. Si ambos producen valores, marcar
`CAT-FORM-002` y mostrar ambos al catalogador antes de staging.

## 6. `dc.source`

El formulario contiene un campo “Fuente” que escribe `dc.source`, mientras el
scope note del registro de metadatos dice “Do not use; only for harvested metadata”.

Existe una contradicción formulario↔scope note. Marcar `CAT-FORM-003` si se
pretende rellenarlo automáticamente y solicitar política institucional.

## 7. `srsc`

La enumeración estática de `/entries` devolvió HTTP 422. El formulario de
“Palabras Clave” lo usa con `closed: false`; no bloquear palabras clave por
ausencia de enumeración SRSC.

## 8. Etiqueta `Identificador` repetida

`traditionalpageone` usa el mismo rótulo `Identificador` para múltiples claves
`dc.identifier.*`. No usar el rótulo como identidad única. Conservar `uiLabel` y
desambiguar solo en `assistantLabel`.

## 9. Dos bindings distintos para `dc.subject`

`traditionalpagetwo` usa `dc.subject` en:

- Palabras Clave → `srsc`, `closed: false`;
- Tópicos (disciplinas, temas específicos) → `topicsPairs`, `closed: true`.

La validación debe ejecutarse por binding y vocabulario; no fusionar ambos controles
antes de la decisión del catalogador.

## 10. Fidelidad literal de rótulos

La interfaz expone literalmente `Titulo` y `Fecha de Creacion`. UI Fidelity Mode
los conserva como rótulos de presentación. Esto no cambia las claves canónicas:
`dc.title` y `dc.date.issued` respectivamente.



## v3.5 — Tensión taxonómica CLIN / campo Rama

La instancia expone `dc.subject.linguisticBranch`, pero Rama no pertenece a la
jerarquía normativa primaria del CLIN (Familia → Agrupación → Variante). Debe
tratarse como enriquecimiento secundario, con autoridad explícita, y no como
requisito para completar una agrupación lingüística.
