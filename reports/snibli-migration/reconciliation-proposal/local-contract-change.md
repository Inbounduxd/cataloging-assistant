# Cambio local del contrato — 2026-10-21

Actualización posterior: las correcciones de fixtures conservan las aserciones
y añaden tres casos de regresión. La selección ampliada termina en **154 passed**
con warnings tratados como errores. Ver `review-completion.md`. Los resultados
146/5 y reproducción HEAD de abajo se conservan como historial del diagnóstico.

C1, C2 y C3 aprobados expresamente por el usuario. Estado: implementación local
preparada para revisión; sin commits, PR, despliegue o promoción de baseline.

## Cambios

- `apps/api/src/cataloging_api/cataloging_contract.py`: revisión
  `snibli-contract-2026-10-21`, binding comparative-text → `dc.type.genre` entre
  issue e issn; 57 bindings y 55 claves. Opcional, no repetible y controlado por
  `genrePairs`, sin habilitar inferencia o perfil automático. Publica las listas
  literales de genrePairs (3) y common_types (26) en el payload de lectura.
- `apps/api/src/cataloging_api/dspace/contract_resolution.py`: primer formulario
  con 45 bindings, segundo con 12; el límite de orden usa esa misma constante.
- `test_cataloging_contract.py`: expectativas del contrato aprobado, posición,
  flags, valores literales, aislamiento del payload y ausencia de srsc inventado.
- `test_dspace_contract_resolution.py` y `test_dspace_contract_inheritance.py`:
  fixtures y expectativas vinculadas al contrato actual pasan a 57/55 y 45/12.
  No se alteran expectativas de snapshots históricos ni se omiten pruebas.
- ADR-013 y decisiones: procedencia de la aprobación y alcance local.

La candidata y los informes históricos permanecen inalterados. Sus dos FAIL
contra la skill histórica siguen siendo evidencia válida de diferencias.

## Validación en WSL

Desde `/home/keilyn/cat`, con PYTHONPATH apuntando a
`/home/keilyn/snibli-migration-audit/apps/api/src` y el Python del entorno
`/home/keilyn/snibli-audit-venv`:

```bash
python -m pytest -q test_cataloging_contract.py test_dspace_contract_resolution.py test_dspace_contract_snapshot.py test_dspace_contract_sync_204.py test_snibli_candidate_reference.py test_snibli_configuration_export.py test_snibli_migration_audit.py
python -m pytest -q -m 'not integration' test_cataloging_contract.py test_dspace_contract*.py test_snibli*.py
```

Los argumentos anteriores representan rutas absolutas a archivos dentro de
`/home/keilyn/snibli-migration-audit/apps/api/tests/` en las ejecuciones reales.
Primera selección: **93 passed**. Selección ampliada: **146 passed, 5 failed**,
con warnings de AsyncMock. Los cinco fallos se reprodujeron con código original
extraído mediante `git archive HEAD apps/api/src` a un directorio temporal y
PYTHONPATH apuntando allí: **3 passed, 5 failed** en los dos archivos afectados.

Fallos preexistentes: tres en `test_dspace_contract_materialize.py` porque su
SimpleNamespace carece de effective_hash; dos en `test_dspace_contract_sync_core.py`
por una respuesta AsyncMock sin raw_payload sincrónico. No se modificaron esos
archivos ni se ajustó producción para ocultar esos fallos.

Ruff se ejecutó sobre los cinco archivos Python modificados en esta fase;
formato e imports corregidos. `git diff --check` y JSON de decisiones verificados.
No se ejecutaron pruebas de integración PostgreSQL ni sincronizaciones reales.
El diff revisable se guarda en `local-contract.patch`.

## Pendientes

`srsc` completo sigue UNKNOWN y no se declara equivalencia total de la migración.
Las secciones observadas se limitan al borrador 2050; el endpoint HAL 204 conserva
su estado no observable. No se modificó ningún artefacto de skill v3.9.2.
