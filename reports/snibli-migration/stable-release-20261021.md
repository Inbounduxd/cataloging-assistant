# Preparación de dspace-cataloger v3.9.3 estable

Fecha: 2026-10-21. Estado: paquete completo preparado para revisión mediante PR.
La adopción en el repositorio depende de revisar y fusionar el cambio de
`skills/dspace-cataloger/CURRENT_RELEASE.md`. No se instala ni despliega la skill.

El usuario respondió «Adelante» a la aceptación del piloto y la preparación de
v3.9.3 con un PR para cambiar el puntero vigente. La aceptación se conserva por
separado en `functional-pilot-20261021/acceptance.json`: no modifica la propuesta
ni su validación histórica, no autoriza fusionar este PR ni aplicar correcciones
en DSpace. La propuesta Article → Reseña queda aceptada como propuesta; el campo
comparativo continúa pendiente. No hubo adjudicación independiente de un gold set.

## Artefacto y procedencia

- Ruta: `skills/dspace-cataloger/versions/v3.9.3/`.
- Artefacto: `dspace-cataloger-v3.9.3.skill`, 407637 bytes, 229 archivos ZIP,
  49 documentos JSON, más fuente extraída exacta y manifiesto por archivo.
- SHA-256: `4ff74baa59049fd9ac9edd1b50458c58493bd2eb9c1482c4a6846f3456ad616e`.
- Padre directo: v3.9.3-rc.2,
  `c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae`.
- rc.1/rc.2 y su evidencia se preservaron mediante PR #87, ya fusionado.
  v3.9.2 y ambos candidatos se conservan sin cambios.
- El constructor valida el hash del padre, los hashes del piloto y el alcance
  de la aceptación. Rechaza permisos de escritura, despliegue o fusión del PR.
- ZIP determinista; los hashes de cada miembro coinciden con la fuente extraída.

El paquete actualiza versión, procedencia y orientación de release. Conserva
íntegros los vocabularios, esquemas, payload de contrato, respuestas HAL y los
23 casos históricos GR01–GR23. En contrato/perfil solo añade el estado de revisión
del puntero; no cambia sus bindings ni sus valores. El lock cambia skillVersion,
manteniendo el hash del contrato. Los estados de adopción dentro del paquete son
registros del momento de construcción; el puntero revisado gobierna la adopción.

## Alcance y pendientes

57 bindings, 55 claves únicas, 56 bindings originales conservados. Se incluye
`dc.type.genre` opcional con tres valores exactos y los tipos Códice, Reseña y
Documento Colonial. Se conservan literalmente `dc.subject.linguiscgroup`, los
controles distintos que comparten metadato y la separación entre lengua de
registro y lengua objeto de estudio. `srsc` conserva sus 665 nodos, 653 relaciones,
12 raíces y 126 respuestas HAL. Todas las decisiones futuras requieren revisión.

Siguen UNKNOWN la equivalencia histórica de `srsc` y la equivalencia completa
de la migración; las secciones activas por HAL siguen UNKNOWN_HTTP_204. El piloto
es un caso enfocado, sin evaluación de texto completo. No se ejecutaron pruebas
de integración PostgreSQL. Esta preparación no realiza solicitudes de red al
repositorio DSpace ni usa credenciales. Los cuatro GET públicos del piloto son
evidencia de la etapa anterior, conservada con sus cuerpos originales.

## Archivos del cambio

- `.gitattributes`: preservar bytes de la release estable.
- `scripts/build_snibli_skill_stable.py`: constructor offline reproducible.
- `apps/api/tests/test_snibli_skill_stable.py`: siete casos de preservación,
  integridad, determinismo, rechazo de alteraciones y alcance de autorización.
- `skills/dspace-cataloger/versions/v3.9.3/`: paquete, fuente y manifiesto.
- `skills/dspace-cataloger/CURRENT_RELEASE.md` y `README.md`: puntero propuesto,
  linaje y registro de versiones.
- `reports/snibli-migration/functional-pilot-20261021/`: piloto y aceptación.
- Este informe.

## Comandos y validación

Desarrollo y pruebas ejecutados dentro de WSL, iniciando desde `/home/keilyn/cat`
y usando exclusivamente el checkout `/home/keilyn/snibli-migration-audit`.
En los comandos siguientes `task_repo` apunta a ese checkout, `task_python` a
`/home/keilyn/snibli-audit-venv/bin/python` y `task_ruff` al Ruff del mismo venv.

```bash
cd /home/keilyn/cat
task_repo=/home/keilyn/snibli-migration-audit
task_python=/home/keilyn/snibli-audit-venv/bin/python
task_ruff=/home/keilyn/snibli-audit-venv/bin/ruff
"$task_ruff" format "$task_repo/scripts/build_snibli_skill_stable.py" "$task_repo/apps/api/tests/test_snibli_skill_stable.py"
"$task_python" "$task_repo/scripts/build_snibli_skill_stable.py" --output "$task_repo/skills/dspace-cataloger/versions/v3.9.3"
"$task_ruff" check "$task_repo/scripts/build_snibli_skill_stable.py" "$task_repo/apps/api/tests/test_snibli_skill_stable.py"
"$task_python" /mnt/c/Users/Jose\ Paul/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$task_repo/skills/dspace-cataloger/versions/v3.9.3/source/dspace-cataloger"
PYTHONPATH="$task_repo/apps/api/src" "$task_python" -m pytest -q -W error -m 'not integration' \
  "$task_repo/apps/api/tests/test_snibli_skill_stable.py" \
  "$task_repo/apps/api/tests/test_cataloging_contract.py" \
  "$task_repo"/apps/api/tests/test_dspace_contract*.py \
  "$task_repo"/apps/api/tests/test_snibli*.py \
  "$task_repo"/apps/api/tests/test_dspace_baseline*.py \
  "$task_repo/apps/api/tests/test_diagnostics_rules.py" \
  "$task_repo/apps/api/tests/test_profile_metrics.py" \
  "$task_repo/apps/api/tests/test_drafts.py" \
  "$task_repo/apps/api/tests/test_vocabulary_service.py" \
  "$task_repo/apps/api/tests/test_agent_read_only_tools.py" \
  "$task_repo/apps/api/tests/test_evidence_service.py"
```

Resultado: **231 passed in 18.98s**, warnings tratados como errores. Ruff y
quick_validate: PASS. Incluye reconstrucción determinista idéntica al paquete,
verificación de todos los hashes y regresiones de auditoría pública, timeouts,
redirecciones, drift, HTTP 204, exportación y reconciliación VERTICAL-022.
No se alteraron pruebas existentes para conseguir este resultado.

Para reproducir, usar un `--output` nuevo: el constructor rechaza sobrescribir
un directorio existente. El constructor no cambia los punteros ni publica nada;
el cambio del registro se revisa por separado en el mismo PR.
