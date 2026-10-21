# Revisión y regresión local — 2026-10-21

Estado: cambio local preparado para revisión humana. No desplegado.

## Selector srsc

Se revisó el control Palabras Clave del borrador existente
https://www.iifl.unam.mx/SNIBLI/workspaceitems/2050/edit.
El DOM muestra un input `dc_subject`, role combobox, `aria-autocomplete="list"`.
Al abrirlo sin escribir no aparece un árbol completo ni opciones que permitan
recorrerlo. Estado final observado: valor vacío, `aria-expanded="false"`, clase
`ng-pristine` y botón Guardar no habilitado. No se escribieron consultas,
seleccionaron términos, guardaron cambios o aceptó la licencia.

La interfaz aporta evidencia de un autocompletado, no de integridad de la
jerarquía de `srsc`. **srsc completo: UNKNOWN**. Sigue siendo necesaria una
exportación verificable de ese vocabulario si se requiere equivalencia completa.

## Correcciones de dobles de prueba

Los cinco fallos reproducidos con HEAD provenían de fixtures incompatibles con
las interfaces actuales; las aserciones existentes de comportamiento se conservan.

- `test_dspace_contract_materialize.py`: usa instancias no persistidas del modelo
  real DSpaceContractSnapshot con effective_hash=None, sustituyendo namespaces
  sin ese atributo. Dos casos nuevos comprueban precedencia del hash efectivo
  aprobado y rechazo de evidencia incompleta aunque coincida el hash.
- `test_dspace_contract_sync_core.py`: AsyncMock con spec AsyncSession y un
  resultado SQLAlchemy síncrono simulado; los checkpoints pendientes contienen
  páginas previas incompletas con totalPages explícito. No se desactiva la
  comprobación del checkpoint. Un caso nuevo prueba que un checkpoint completo
  no llama al loader, persistencia ni commit.
- `test_dspace_contract_store.py`: el mock usa spec AsyncSession para que add sea
  síncrono y execute/flush asíncronos, eliminando el warning de corrutina olvidada.

No se modificó código de producción para acomodar mocks. Los fixtures ligados
al contrato aprobado conservan sus expectativas actualizadas de 57/55 y 45/12;
los snapshots históricos siguen conservando sus cifras originales.

## Comandos y resultados

Desde WSL, cwd `/home/keilyn/cat`:

```bash
task_repo=/home/keilyn/snibli-migration-audit
PYTHONPATH="$task_repo/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python -m pytest -q -W error -m 'not integration' "$task_repo/apps/api/tests/test_cataloging_contract.py" "$task_repo"/apps/api/tests/test_dspace_contract*.py "$task_repo"/apps/api/tests/test_snibli*.py
```

Resultado: **154 passed in 5.90s**, sin warnings. Ruff check y formato revisados
para los tres archivos corregidos; git diff --check y comparación de skills
contra HEAD sin cambios. No se ejecutaron pruebas de integración PostgreSQL.

El diff local incluye el contrato y su validación de orden, pruebas y ADR-013.
`local-contract.patch` se regeneró para incluir estas correcciones. La revisión
conserva la política de no escritura, aprobación humana, clave literal
`dc.subject.linguiscgroup`, ejes lingüísticos independientes y ausencia del
nuevo campo en subconjuntos de inferencia automática. La referencia de aplicación
`snibli-contract-2026-10-21` no se presenta como una nueva release de la skill.

## Límites de entrega

Sin commits, PR, despliegues, cambios PostgreSQL, promoción de baseline ACTIVE o
sincronizaciones programadas. Artefactos de skill v3.9.2 intactos. No se declara
equivalencia total de migración: srsc completo sigue UNKNOWN y las secciones
observadas en interfaz se limitan al borrador identificado, sin reconstruir una
respuesta HAL del endpoint 204. La futura release de skill no se generó en esta
fase; requiere su propio cambio revisable.
