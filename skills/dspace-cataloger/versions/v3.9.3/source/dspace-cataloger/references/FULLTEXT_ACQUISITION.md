> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Full-Text Acquisition & Evidence

## Objetivo

Antes de cerrar un registro catalográfico, intentar descubrir y consultar todas
las representaciones de texto completo que la fuente publique de forma legítima.

La landing page es una fuente de metadatos, pero no sustituye el texto completo
cuando este está disponible.

## Orden de descubrimiento

Tras abrir la URL primaria:

1. identificar landing/citation page;
2. localizar enlaces explícitos a:
   - XML/JATS;
   - PDF;
   - HTML full text;
   - EPUB u otros formatos textuales;
3. seguir únicamente URLs descubiertas en la fuente o metadatos embebidos;
4. no fabricar rutas de descarga por patrones adivinados;
5. registrar cada representación y su resultado.

## Preferencia de representación

Cuando existan varias:

1. **XML/JATS** para estructura semántica y metadatos;
2. **PDF** para versión publicada, paginación y evidencia por página;
3. **HTML full text** para contenido completo cuando XML/PDF no son accesibles;
4. **OCR** solo si el PDF carece de capa textual.

XML y PDF son complementarios; no se excluyen.

## Estados de adquisición

- `FULLTEXT_XML`
- `FULLTEXT_PDF`
- `FULLTEXT_HTML`
- `FULLTEXT_OCR`
- `FULLTEXT_MULTIPLE`
- `FULLTEXT_UNAVAILABLE`
- `FULLTEXT_BLOCKED`

`FULLTEXT_UNAVAILABLE` significa que no se detectó o recuperó texto completo.
`FULLTEXT_BLOCKED` significa que existe pero no pudo consultarse por acceso,
robots, autenticación, paywall o fallo técnico.

## Front matter

Priorizar la extracción de:

- título;
- subtítulo;
- autor(es);
- afiliaciones;
- ORCID;
- resumen/abstract;
- palabras clave/keywords;
- DOI;
- ISSN/eISSN;
- volumen;
- número;
- fecha;
- páginas;
- licencia.

Los valores hallados en front matter pueden elevarse a `EXTRAÍDO` cuando la
evidencia es inequívoca.

## Texto completo como evidencia temática

Para materias, lenguas estudiadas y clasificación analizar:

- título;
- resumen;
- palabras clave;
- introducción;
- métodos/corpus;
- resultados;
- discusión;
- conclusiones.

La mera frecuencia de un término no basta.

## Referencias bibliográficas

Las referencias se conservan en el corpus, pero:

- una lengua, lugar, institución o persona mencionada solo en bibliografía
  **no constituye evidencia suficiente** para asignar metadatos descriptivos o
  temáticos;
- marcar esos fragmentos como `EXCLUDE_FOR_SUBJECT`.

## Distinción lingüística

Antes de poblar campos lingüísticos, clasificar cada lengua detectada como:

1. `CONTENT_LANGUAGE`: lengua en que está escrito/registrado el recurso;
2. `OBJECT_LANGUAGE`: lengua estudiada, documentada o analizada;
3. `EXAMPLE_LANGUAGE`: lengua de ejemplos o datos lingüísticos;
4. `MENTION_ONLY`: mención incidental;
5. `REFERENCE_ONLY`: aparece solo en referencias.

Mapeo:

- `dc.description.registeredLanguage` solo desde `CONTENT_LANGUAGE` con evidencia;
- `dc.subject.linguiscgroup` puede derivar de `OBJECT_LANGUAGE`;
- familia/rama requieren además autoridad/crosswalk;
- `REFERENCE_ONLY` nunca dispara automáticamente campos lingüísticos.

## OCR

Usar OCR únicamente cuando:

- el recurso realmente sea PDF/imagen;
- no haya texto extraíble suficiente;
- el OCR sea necesario para recuperar evidencia.

Marcar todo texto OCR como tal. Una lectura OCR dudosa no debe sobrescribir
metadatos explícitos de landing/XML.

## Trazabilidad

Cada propuesta debe poder señalar:

- representación;
- URL;
- página si existe;
- sección;
- fragmento/paráfrasis breve de evidencia;
- estado de evidencia;
- método de extracción.

Ejemplo conceptual:

```json
{
  "field": "dc.subject.linguiscgroup",
  "suggestedValue": "Zapoteco",
  "evidenceStatus": "EXTRAÍDO",
  "evidence": [{
    "representation": "PDF",
    "page": 7,
    "section": "Resultados",
    "reason": "La lengua es objeto directo del análisis."
  }]
}
```

## Política de fallo

Si el PDF/XML está anunciado pero la herramienta disponible no consigue
recuperarlo:

- no fingir que fue leído;
- registrar `FULLTEXT_BLOCKED` o `FAILED`;
- conservar como válidos solo los datos de la landing y otras fuentes
  efectivamente consultadas;
- marcar los campos que dependen del texto completo como `PENDIENTE`.
