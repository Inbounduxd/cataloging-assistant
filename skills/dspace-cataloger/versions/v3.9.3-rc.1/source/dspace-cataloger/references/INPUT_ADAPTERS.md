> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Input Adapters v3.2

## Principio

El núcleo catalográfico no debe depender del canal de entrada.

Todos los orígenes se convierten primero a un **Evidence Corpus** conforme a
`assets/evidence-corpus.schema.json`.

```text
URL ───────────────┐
PDF upload ────────┤
EPUB upload ───────┤
Google Sheets ─────┤
DSpace item ───────┤──> Evidence Corpus ──> Cataloguing Core
DSpace bitstream ──┘
```

## 1. URL

Ruta:

`URL → landing → discovery → PDF/XML/HTML → parse → Evidence Corpus`

Conservar la landing incluso si existe full text, porque puede aportar fecha
oficial, DOI, volumen, número, licencia y URLs canónicas.

## 2. PDF subido

Ruta:

`PDF_UPLOAD → MIME/hash → texto/páginas → segmentación → Evidence Corpus`

Registrar:

- `sourceOrigin = UPLOAD_USER`
- nombre original;
- MIME;
- tamaño;
- SHA-256;
- número de páginas;
- presencia/ausencia de capa textual.

Si tiene texto extraíble, no aplicar OCR.

Si no tiene texto suficiente:

`PDF_UPLOAD → OCR → representationKind=OCR`

El OCR nunca debe ocultar que el origen fue un PDF subido.

## 3. EPUB subido

Ruta:

`EPUB_UPLOAD → package metadata → XHTML → estructura → Evidence Corpus`

Registrar:

- metadata del paquete;
- títulos de capítulos/secciones;
- archivos XHTML;
- localizadores estructurales.

No inventar paginación. Usar `locator` como:

`chapter=3; section=2; xhtml=chapter03.xhtml`

## 4. Google Sheets / Excel

Ruta:

`SPREADSHEET_ROW → evidencia previa de trabajo`

La fila es evidencia operativa/secundaria y puede contener datos correctos, pero
no reemplaza una fuente documental primaria.

Usar:

- `representationKind = SPREADSHEET`
- `sectionClass = SPREADSHEET_METADATA`

Los valores heredados se contrastan contra PDF/XML/landing cuando sea posible.

## 5. DSpace Item

Ruta:

`DSpace item → metadata existente + bitstreams → Evidence Corpus`

Permite dos modos:

- catalogación/enriquecimiento;
- auditoría de registros existentes.

Los metadatos existentes son evidencia del estado actual del repositorio, no
prueba automática de que sean correctos.

## 6. DSpace Bitstream

Ruta:

`DSpace bitstream → PDF/EPUB/etc → parse → Evidence Corpus`

Registrar:

`sourceOrigin = DSpace_BITSTREAM`

Nunca sobrescribir metadatos existentes solo porque el bitstream sugiera un
valor diferente; generar una discrepancia para revisión.

## Autoridad de contenido vs autoridad bibliográfica

Cada representación puede tener dos dimensiones:

### `contentAuthority`

Qué tan confiable es para analizar el contenido intelectual.

### `bibliographicAuthority`

Qué tan confiable es para fecha, DOI, publicación, volumen, número, licencia,
versión, etc.

Ejemplo:

```text
PDF subido por usuario
  contentAuthority       = PRIMARY
  bibliographicAuthority = USER_SUPPLIED

Landing editorial
  contentAuthority       = SECONDARY
  bibliographicAuthority = OFFICIAL
```

La fusión de evidencias debe respetar ambas dimensiones.
