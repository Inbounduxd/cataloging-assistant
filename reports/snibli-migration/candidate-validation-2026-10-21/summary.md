# Comparación local de candidata — 2026-10-21

**La candidata coincide con las dimensiones observables de la captura; la
migración completa permanece UNKNOWN.** No se adoptó el contrato en runtime.

| Comprobación | Contra v3.9.2 | Contra candidata explícita |
|---|---|---|
| Controles configurados | FAIL: 56 → 57 | PASS: 57 / 57 |
| Registro esperado | 54 claves preservadas | PASS: 55 / 55 |
| Valores de tipos documentales | FAIL: tres valores añadidos | PASS: lista candidata literal |
| Vocabularios planos asociados | Diferencia en common_types | PASS: 17 / 17 |
| Árbol srsc | UNKNOWN | UNKNOWN |
| Colección actual | Sin equivalencia probada con piloto histórica | PASS: UUID y Handle explícitos |
| Secciones activas traditional | UNKNOWN / HTTP 204 | UNKNOWN / HTTP 204 |

La candidata es `reconciliation-proposal/candidate-contract.json`; la observación
es la exportación autenticada `authenticated-20261021T055428Z-8a836a27/export.json`.
El candidato y los archivos de captura se leen sin modificarlos. La herramienta
no requiere volver a introducir credenciales para esta comparación offline.

## Implementación

`scripts/audit_snibli_migration.py` acepta `--candidate` y valida la referencia:
56 identidades originales preservadas, clave literal `dc.subject.linguiscgroup`,
dimensiones de control, posiciones e identidades únicas, consistencia de recuentos,
registro de las claves y vocabularios. Rechaza flags que habiliten escrituras,
promoción automática o uso runtime. No se colapsan los controles con metadata
compartido. Cada dimensión se compara contra la evidencia actual.

Los reportes incluyen simultáneamente el resultado de la release preservada y
el de la candidata. El proceso devolvió código **1** porque conserva los dos FAIL
de drift contra v3.9.2. La candidata no cambia esos hechos ni constituye una
aprobación institucional o un nuevo baseline ACTIVE.

La CLI emitió 8 PASS, 2 FAIL, 3 UNKNOWN y 8 NOT_TESTED. El agregado no representa
un porcentaje de compatibilidad; cada resultado conserva su alcance. `audit.json`,
`audit.md` y `diff.json` incluyen configuración, procedencia y resultados.

## Comando ejecutado

Desde `/home/keilyn/cat` en WSL:

```bash
python3 /home/keilyn/snibli-migration-audit/scripts/audit_snibli_migration.py \
  --offline \
  --candidate /home/keilyn/snibli-migration-audit/reports/snibli-migration/reconciliation-proposal/candidate-contract.json \
  --observed /home/keilyn/snibli-migration-audit/reports/snibli-migration/authenticated-20261021T055428Z-8a836a27/export.json \
  --output /home/keilyn/snibli-migration-audit/reports/snibli-migration/candidate-validation-2026-10-21
```

## Validación

13 pruebas nuevas cubren coincidencia parcial, preservación del drift histórico,
ejecución sin red, bloqueo de candidatas inseguras, identidades duplicadas,
claves literales, vocabularios no normalizados, metadatos compartidos, cambios de
ID observables aunque las secciones sean 204, y argumentos CLI incompletos.

La selección de regresión anterior más
`apps/api/tests/test_snibli_candidate_reference.py` termina en **100 passed**.
Ruff PASS. No se cambiaron las expectativas de pruebas anteriores. El código API
y la skill permanecen idénticos a HEAD. No se ejecutaron solicitudes HTTP,
autenticación, escrituras PostgreSQL, promociones, commits, PR o despliegues.

## Pendiente fuera de esta implementación

La aprobación institucional del significado del control `dc.type.genre` y de los
valores nuevos sigue siendo una decisión explícita de revisión. La semántica no
se deduce de una coincidencia estructural con un JSON candidato. Para declarar
equivalencia completa aún falta resolver la pertenencia activa con evidencia
autorizada y la jerarquía srsc, además de la validación semántica/Golden Set.
