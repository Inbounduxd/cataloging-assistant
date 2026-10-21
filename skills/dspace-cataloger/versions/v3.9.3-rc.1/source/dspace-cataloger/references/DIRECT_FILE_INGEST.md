> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Direct File Ingest — PDF / EPUB

## Objetivo

Procesar archivos entregados directamente por el catalogador sin depender de
una landing web.

## Validación mínima

Antes de extraer:

1. confirmar que el archivo es legible;
2. detectar MIME real cuando sea posible;
3. calcular SHA-256;
4. conservar nombre y tamaño;
5. no modificar el original;
6. registrar método de extracción.

## PDF

### PDF textual

Extraer texto conservando ancla de página.

Preferencia:

`página → sección → evidencia`

### PDF escaneado

Aplicar OCR únicamente cuando no exista capa textual suficiente.

Marcar:

- `representationKind = OCR`
- `sourceOrigin = UPLOAD_USER`
- `CAT-OCR-001` si un valor crítico depende solo de OCR dudoso.

### PDF híbrido

Combinar texto nativo con análisis/OCR solo en páginas necesarias.

## EPUB

Extraer:

- package metadata;
- título;
- creators;
- idioma;
- identificadores;
- publisher si está declarado;
- tabla de contenidos;
- XHTML;
- notas/referencias.

La evidencia debe anclarse a capítulo/sección/archivo XHTML, no a una página
inventada.

## Enriquecimiento posterior

Si después se descubre una landing editorial:

1. incorporarla como nueva representación;
2. no reemplazar el corpus anterior;
3. comparar valores;
4. elevar autoridad bibliográfica cuando corresponda;
5. registrar discrepancias.

## Regla de preservación

El archivo subido es evidencia documental. El proceso puede crear derivados
(texto extraído, chunks, OCR, embeddings), pero nunca sustituir el original.
