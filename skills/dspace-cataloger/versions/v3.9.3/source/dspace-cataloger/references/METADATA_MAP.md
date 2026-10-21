> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Mapa real de formularios y metadatos

> **v3.4 — Identidad de binding.** Esta tabla conserva el mapa v3.3. Para
> presentación y serialización sin ambigüedad, complementarla con
> `assets/dspace-form-contract-v1.json`. La identidad del control es
> `bindingId + uiLabel + metadataField`; no colapsar controles que compartan clave.

Este mapa deriva de `traditionalpageone` y `traditionalpagetwo` recuperados por la API.

| Formulario | Etiqueta | Campo | Entrada | Obligatorio | Repetible | Vocabulario | Cerrado |
|---|---|---|---|---:|---:|---|---:|
| `traditionalpageone` | Provenance / Catalogación | `dcterms.provenance` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Titulo | `dc.title` | `onebox` | sí | no | `—` | no |
| `traditionalpageone` | Variante de título | `dc.title.alternative` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Subtítulo | `dc.title.subtitle` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Título de revista | `dc.relation.ispartof` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Es parte de (título del libro) | `dc.source.booktitle` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Autor | `dc.contributor.author` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Traductor | `dc.contributor.translator` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Colaboradores | `dc.contributor.other` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Instituciones participantes | `dc.contributor.institution` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Editores | `dc.contributor.editor` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Fecha de Creacion | `dc.date.issued` | `date` | no | no | `—` | no |
| `traditionalpageone` | País donde se encontró el recurso | `dc.coverage.countryFound` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Editorial | `dc.publisher` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Edicion(No)/Periodicdad | `dc.identifier.issue` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.issn` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.other` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.ismn` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.govdoc` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.uri` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.isbn` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.eissn` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.eisbn` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.handle` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Identificador | `dc.identifier.doi` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Fuente | `dc.source` | `onebox` | no | no | `—` | no |
| `traditionalpageone` | Type | `dc.type` | `dropdown` | no | sí | `common_types` | sí |
| `traditionalpageone` | Uso de lengua | `dc.description.languageUsage` | `dropdown` | no | no | `languageUsagePairs` | sí |
| `traditionalpageone` | Lengua de registro | `dc.description.registeredLanguage` | `dropdown` | no | sí | `registeredLanguagePairs` | sí |
| `traditionalpageone` | Lengua registrada (Agrupación lingüística) | `dc.subject.linguiscgroup` | `dropdown` | no | sí | `linguiscgroupPairs` | sí |
| `traditionalpageone` | Familia lingüística | `dc.subject.linguisticFamily` | `dropdown` | no | sí | `linguisticFamilyPairs` | sí |
| `traditionalpageone` | Rama lingüística | `dc.subject.linguisticBranch` | `dropdown` | no | sí | `linguisticBranchPairs` | sí |
| `traditionalpageone` | Variante lingüística (CLIN) | `dc.subject.linguisticVariant` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Autodenominación | `dc.subject.selfDenomination` | `dropdown` | no | sí | `selfDenominationPairs` | sí |
| `traditionalpageone` | ISO 639-1 | `dc.language.iso6391` | `dropdown` | no | sí | `iso6391Pairs` | sí |
| `traditionalpageone` | Soporte | `dc.format.medium` | `dropdown` | no | no | `mediumPairs` | sí |
| `traditionalpageone` | Tipo de extensión | `dc.format.medium` | `dropdown` | sí | no | `extentTypePairs` | sí |
| `traditionalpageone` | Número de páginas / extensión | `dc.format.extent` | `onebox` | sí | no | `—` | no |
| `traditionalpageone` | Derechos | `dc.rights` | `textarea` | no | no | `—` | no |
| `traditionalpageone` | Licencia de uso | `dc.rights.license` | `dropdown` | no | no | `licensePairs` | sí |
| `traditionalpageone` | Derecho de acceso | `dc.rights.accessRights` | `dropdown` | no | no | `accessRightsPairs` | sí |
| `traditionalpageone` | Repositorio físico | `dc.source.physicalRepository` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Repositorio digital (URL) | `dc.identifier.url` | `onebox` | no | sí | `—` | no |
| `traditionalpageone` | Clasificación primaria | `dc.subject.primaryClassification` | `dropdown` | no | no | `primaryClassificationPairs` | sí |
| `traditionalpagetwo` | Palabras Clave | `dc.subject` | `tag` | no | sí | `srsc` | no |
| `traditionalpagetwo` | Abstract | `dc.description.abstract` | `textarea` | no | no | `—` | no |
| `traditionalpagetwo` | Nivel educativo | `dc.audience.educationLevel` | `dropdown` | no | sí | `educationLevelPairs` | sí |
| `traditionalpagetwo` | Para L1 o para L2 | `dc.audience.languageTarget` | `dropdown` | no | no | `languageTargetPairs` | sí |
| `traditionalpagetwo` | Tópicos (disciplinas, temas específicos) | `dc.subject` | `dropdown` | no | sí | `topicsPairs` | sí |
| `traditionalpagetwo` | País | `dc.coverage.country` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Estado | `dc.coverage.state` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Región | `dc.coverage.region` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Comunidad | `dc.coverage.community` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Temporal | `dc.coverage.temporal` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Siglo | `dc.coverage.century` | `onebox` | no | sí | `—` | no |
| `traditionalpagetwo` | Notas | `dc.description` | `textarea` | no | no | `—` | no |

## Semántica local confirmada

- `dc.coverage.countryFound`: **País donde se encontró el recurso**.
- `dc.coverage.country`: país de origen del recurso.
- `dc.coverage.state`: estado de origen del recurso.
- `dc.coverage.region`: región de origen del recurso.
- `dc.coverage.community`: comunidad de origen del recurso.
- `dc.contributor.institution`: institución a la que pertenece el autor / institución participante.
- `dc.subject.primaryClassification`: clasificación primaria cerrada.

## Reglas de mapeo importantes

- Revista contenedora → `dc.relation.ispartof`.
- Libro contenedor → `dc.source.booktitle`.
- URL de repositorio digital → `dc.identifier.url`.
- URI/identificador general → `dc.identifier.uri` solo cuando corresponda.
- No crear Handle: `dc.identifier.handle` se verifica si ya existe.

## Nota de gobernanza lingüística v3.5

Para México, la correspondencia normativa de CLIN es:

`dc.subject.linguisticFamily` → Familia CLIN
`dc.subject.linguiscgroup` → Agrupación CLIN
`dc.subject.linguisticVariant` → Variante CLIN

`dc.subject.linguisticBranch` es enriquecimiento genealógico secundario y no debe
presentarse como nivel CLIN. `dc.description.registeredLanguage` permanece fuera
de esta jerarquía: describe la lengua de redacción/registro del recurso.
