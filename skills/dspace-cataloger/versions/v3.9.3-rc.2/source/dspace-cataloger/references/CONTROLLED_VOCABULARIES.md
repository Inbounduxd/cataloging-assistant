> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Vocabularios controlados reales

Inventario recuperado desde `/api/submission/vocabularies`.

| Vocabulario | Entradas | Estado |
|---|---:|---|
| `accessRightsPairs` | 4 | OK |
| `common_iso_languages` | 12 | OK |
| `common_types` | 23 | OK |
| `educationLevelPairs` | 6 | OK |
| `extentTypePairs` | 7 | OK |
| `iso6391Pairs` | 253 | OK |
| `languageTargetPairs` | 3 | OK |
| `languageUsagePairs` | 3 | OK |
| `licensePairs` | 13 | OK |
| `linguiscgroupPairs` | 256 | OK |
| `linguisticBranchPairs` | 82 | OK |
| `linguisticFamilyPairs` | 39 | OK |
| `mediumPairs` | 4 | OK |
| `openaire_organization_types` | 2 | OK |
| `openaire_types` | 74 | OK |
| `openaire_version_types` | 8 | OK |
| `primaryClassificationPairs` | 6 | OK |
| `registeredLanguagePairs` | 256 | OK |
| `selfDenominationPairs` | 20 | OK |
| `srsc` | — | ERROR: GET falló (422): http://132.248.101.240:8080/server/api/submission/vocabularies/srsc/entries?size=1000 |
| `topicsPairs` | 40 | OK |

## Valores cerrados pequeños

### `languageUsagePairs`

`Monolingüe`, `Bilingüe`, `Multilingüe`

### `accessRightsPairs`

`Acceso abierto`, `Acceso embargado`, `Acceso restringido`, `Acceso a registro bibliográfico`

### `mediumPairs`

`Impreso`, `Digital`, `Audiovisual`, `Sonoro`

### `extentTypePairs`

`Impreso`, `Impreso hojas`, `Digital`, `Digital hojas`, `Fotografía`, `Libro`, `Dirección electrónica`

### `primaryClassificationPairs`

`Didácticos`, `Históricos`, `Culturales`, `Lingüísticos`, `Derecho`, `Salud`

### `languageTargetPairs`

`L1`, `L2`, `L1 y L2`

### `educationLevelPairs`

`Preescolar`, `Primaria`, `Secundaria`, `Preparatoria`, `Universidad`, `Postgrado`

### `licensePairs`

`Creative Commons`, `Dominio público`, `Atribución 4.0 Internacional. https://creativecommons.org/licenses/by/4.0/`, `Atribución-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-sa/4.0/`, `Atribución-NoComercial 4.0 Internacional. https://creativecommons.org/licenses/by-nc/4.0/`, `Atribución-NoComercial-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-nc-sa/4.0/`, `Atribución-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nd/4.0/`, `Atribución-NoComercial-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nc-nd/4.0/`, `CC0 1.0 Universal. https://creativecommons.org/publicdomain/zero/1.0/`, `Reconocimiento-Uso no Comercial-Sin Obras Derivadas 2.5 (Perú) https://creativecommons.org/licenses/by-nc-nd/2.5/pe/`, `Autorisation HAL v1 https://about.hal.science/hal-authorisation-v1/#autorisation-hal-v1`, `Copyright/Todos los derechos reservados`, `Copyleft`

### `common_types`

`Animation`, `Article`, `Book`, `Book chapter`, `Dataset`, `Learning Object`, `Image`, `Image, 3-D`, `Map`, `Musical Score`, `Plan or blueprint`, `Preprint`, `Presentation`, `Recording, acoustical`, `Recording, musical`, `Recording, oral`, `Software`, `Technical Report`, `Thesis`, `Video`, `Working Paper`, `Other`, `Pagina Web`

### `topicsPairs`

`Lingüística`, `Educación`, `Alfabetización`, `Lexicografía`, `Lexicología`, `Morfosintaxis`, `Semántica`, `Sociolingüística`, `Historiografía lingüística`, `Documentación lingüística`, `Etnohistoria`, `Educación indígena`, `Fonología`, `Fonética`, `Morfología`, `Sintaxis`, `Pragmática`, `Descripción gramatical`, `Planificación lingüística`, `Políticas lingüísticas`, `Literatura indígena`, `Narrativa`, `Traducción`, `Interpretación`, `Contacto lingüístico`, `Análisis del discurso`, `Etnolingüística`, `Familias lingüísticas`, `Género lingüístico`, `Psicolingüística`, `Patrimonio lingüístico`, `Diversidad lingüística`, `Corpus lingüístico`, `Campos semánticos`, `Partículas discursivas`, `Técnicas etnográficas`, `Transcripción`, `Género gramatical`, `Filología indoamericana`, `Etnografía`

## Listas extensas

Consultar directamente `assets/controlled-vocabulary-index.json` para:

- `registeredLanguagePairs` (256)
- `linguiscgroupPairs` (256)
- `linguisticBranchPairs` (82)
- `linguisticFamilyPairs` (39)
- `iso6391Pairs` (253)

## Regla

Un valor de un campo con `closed: true` solo pasa `CAT-VOCAB-001` si coincide literalmente con uno de los `value` del vocabulario asociado.

`srsc` no pudo enumerarse mediante `/entries` (HTTP 422). Como el binding de Palabras Clave está marcado `closed: false`, no debe tratarse como lista cerrada.