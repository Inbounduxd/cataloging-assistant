> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Mapeo de la cola de trabajo

Los campos de workflow no son automáticamente metadatos DSpace.

| Columna operativa | Tratamiento |
|---|---|
| ID | conservar como identificador del caso |
| Ficha original | fuente de extracción |
| Enlace fuente | validar; puede alimentar `dc.identifier.url` |
| Responsable original | NO convertir en autor |
| Estado actual | workflow |
| Lote semanal | workflow |
| Extracción | workflow |
| QA | workflow |
| Revisión humana | workflow |
| Handle/UUID | verificar, nunca inventar |
| Observaciones | trazabilidad |

Nunca propagar metadatos de un registro a otro por pertenecer al mismo lote.
