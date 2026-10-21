# Revisión final de consumidores — 2026-10-21

Resultado: cambio local revisado; **195 pruebas aprobadas**, warnings como errores.
Sin despliegue, commits o PR. No se declara equivalencia completa de migración.

## Hallazgo corregido

`baseline_diagnose.diagnose_bindings` todavía usaba la frontera histórica de 44
bindings en el primer formulario. Eso habría informado incorrectamente un cambio
de formulario para Clasificación primaria tras insertar el campo comparativo.
Ahora reutiliza EXPECTED_FORM_BINDING_COUNTS de contract_resolution (45/12).
El fixture de baseline usa 57 bindings y su prueba de selector ISSN se desplaza
al índice 16, conservando la expectativa literal ISSN. Una prueba nueva comprueba
que el límite anterior produce exactamente un mismatch de formulario en índice 44.

Se revisaron también los consumidores del payload: el agente obtiene versión y
conteo del contrato; el cliente web declara versión string, conteo number y una
lista de campos sin longitud fija. Las nuevas propiedades del payload son
aditivas. No se modificó la UI ni se ejecutaron pruebas de navegador de la app.

## Validación

WSL, cwd `/home/keilyn/cat`, Python del entorno aislado de auditoría:

```bash
task_repo=/home/keilyn/snibli-migration-audit
PYTHONPATH="$task_repo/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python -m pytest -q -W error -m 'not integration' "$task_repo/apps/api/tests/test_cataloging_contract.py" "$task_repo"/apps/api/tests/test_dspace_contract*.py "$task_repo"/apps/api/tests/test_snibli*.py "$task_repo"/apps/api/tests/test_dspace_baseline*.py "$task_repo/apps/api/tests/test_diagnostics_rules.py" "$task_repo/apps/api/tests/test_profile_metrics.py" "$task_repo/apps/api/tests/test_drafts.py" "$task_repo/apps/api/tests/test_vocabulary_service.py" "$task_repo/apps/api/tests/test_agent_read_only_tools.py" "$task_repo/apps/api/tests/test_evidence_service.py"
```

**195 passed in 6.50s**. La primera recopilación se detuvo por dependencias
ausentes; se instalaron las dependencias declaradas de apps/api mediante
`python -m pip install -e /home/keilyn/snibli-migration-audit/apps/api` únicamente
en `/home/keilyn/snibli-audit-venv`. Se instaló también pyopenssl<26 en ese entorno
para compatibilidad con la restricción cryptography<46 del proyecto, sin cambiar
dependencias del repositorio o paquetes de la instalación externa al entorno.
Ruff de los dos archivos adicionales y git diff --check verificados.

## Entrega y límites

`local-contract.patch` se regenera con todos los cambios rastreados en código,
pruebas y ADR-013. Los scripts y pruebas nuevos de auditoría siguen como archivos
locales sin seguimiento y están descritos en los informes anteriores.

La aprobación C1–C3 se conserva en decision.json; la candidata histórica no se
reescribe. Skill v3.9.2 intacta. srsc completo sigue UNKNOWN; la vista del borrador
2050 prueba sus secciones renderizadas, sin convertir el endpoint 204 en HAL
observable. No se inicia sincronización ni se promueve baseline ACTIVE. La nueva
release de skill requiere un cambio separado; no se preparó ni publicó aquí.
