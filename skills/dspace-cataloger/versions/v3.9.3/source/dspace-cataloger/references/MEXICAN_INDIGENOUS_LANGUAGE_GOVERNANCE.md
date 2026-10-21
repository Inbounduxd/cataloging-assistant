> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Gobernanza de lenguas indígenas de México — v3.5

## Autoridad primaria

Para recursos relativos a lenguas indígenas nacionales de México, utilizar el
**Catálogo de las Lenguas Indígenas Nacionales (CLIN), INALI** como autoridad
primaria para la clasificación normativa.

Jerarquía CLIN:

**Familia lingüística → Agrupación lingüística → Variante lingüística**

La **Rama lingüística** no constituye uno de los tres niveles normativos del
CLIN. En esta skill se modela como enriquecimiento genealógico opcional.

## Mapeo a DSpace

| Concepto | Campo DSpace | Autoridad | Regla |
|---|---|---|---|
| Lengua de redacción/registro | `dc.description.registeredLanguage` | fuente + vocabulario local | No confundir con lengua estudiada |
| Familia lingüística | `dc.subject.linguisticFamily` | CLIN/INALI + vocabulario local | Nivel normativo |
| Rama lingüística | `dc.subject.linguisticBranch` | autoridad secundaria | Opcional, no-CLIN |
| Agrupación lingüística | `dc.subject.linguiscgroup` | CLIN/INALI + vocabulario local | Lengua/agrupación objeto del recurso |
| Variante lingüística | `dc.subject.linguisticVariant` | CLIN/INALI + vocabulario local | Requiere reconciliación explícita |

## Modelo interno multientidad

Cuando el recurso trate varias lenguas, preservar cada trayectoria como entidad:

```json
{
  "sourceLabel": "Tsotsil",
  "family": "Maya",
  "branch": "Tseltalano",
  "group": "Tsotsil",
  "variant": null,
  "authority": {
    "family": "CLIN",
    "branch": "SECONDARY_GENEALOGICAL_AUTHORITY",
    "group": "CLIN",
    "variant": null
  }
}
```

No generar combinaciones cruzadas entre valores planos de familias, ramas,
agrupaciones y variantes.

## Lengua del documento vs. lengua objeto

- `registeredLanguage`: lengua de redacción/registro del recurso.
- `linguiscgroup`: agrupación o lengua de la que trata el recurso.
- `languageUsage`: función discursiva global; no se determina contando idiomas.

Un título o abstract paralelo no convierte automáticamente un artículo en
bilingüe. Una lista de lenguas estudiadas tampoco convierte necesariamente el
texto en multilingüe si esas lenguas son objetos de análisis y no contenido
discursivo sustantivo.

## Variantes lingüísticas

No mapear automáticamente a `dc.subject.linguisticVariant`:

- localidades;
- regiones;
- nombres comunitarios;
- denominaciones dialectales libres de la fuente.

Solo cerrar una variante cuando exista evidencia fuente, correspondencia de
autoridad y valor válido en el vocabulario DSpace. En caso contrario: `PENDIENTE`.

## Alias, exónimos y autodenominaciones

Preservar por separado:

1. forma usada por la fuente;
2. forma autorizada por CLIN;
3. forma autorizada por DSpace;
4. autodenominación, si existe campo controlado.

Nunca realizar sustituciones silenciosas (p. ej. `Ngigua → Chocholteco`) sin
validación de autoridad y trazabilidad QA.

## Fuentes recomendadas

- INALI, *Catálogo de las Lenguas Indígenas Nacionales: Variantes lingüísticas
  de México con sus autodenominaciones y referencias geoestadísticas*.
- Diario Oficial de la Federación, publicación del CLIN, 14 de enero de 2008.
- Atlas de las Lenguas Indígenas de México, INALI.
- `assets/dspace-cataloguing-profile-v3.json` y vocabularios de la instancia para
  serialización operacional.
