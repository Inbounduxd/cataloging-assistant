# srsc: jerarquía pública recuperada — 2026-10-21

**PASS de captura del árbol alcanzable por HAL.** No se utilizaron credenciales,
cookies de una sesión de usuario ni inicio de sesión. Se realizaron 126 GET.

| Medida | Resultado |
|---|---:|
| Raíces | 12 |
| Nodos únicos | 665 |
| Relaciones padre-hijo | 653 |
| Hojas declaradas | 540 |
| Respuestas originales conservadas | 126 |
| Errores de captura o de recorrido | 0 |
| Fallos en verificación SHA-256 de respuestas | 0 |
| POST de login | 0 |

La raíz se obtuvo mediante la operación top documentada. Cada rama se siguió
por el enlace children anunciado en HAL. Se comprobó paginación, conteos,
identificadores duplicados/ciclos y límites de profundidad y nodos. La relación
HAL de las páginas hijas de esta instancia se llama **children**. Todos los
nodos incluyen selectable booleano y su indicador hasChildren.

Se conservan [export.json](export.json), [srsc-tree.json](srsc-tree.json),
[audit.json](audit.json), [audit.md](audit.md) y raw/*.response. La exportación
original tiene SHA-256
`af9f23beadacf6793b3495df28f38f59dec3b61034219e1dac518ba52a511f0e`.

## Alcance

capture_complete=true significa que terminó esta captura específica de srsc.
snapshot_complete=false es esperable: no se capturaron formularios, registro de
metadatos o membresía de colección en este modo. Los UNKNOWN del informe genérico
no invalidan la captura del árbol; corresponden a superficies fuera de su alcance.

La jerarquía actual expuesta por HAL ya no es una evidencia faltante. No se afirma
igualdad con el archivo XML del servidor, visibilidad de nodos que la API no
exponga o equivalencia histórica: la referencia v3.9.2 tampoco contiene el árbol
completo comparable. La captura recorre varias respuestas, no una transacción
atómica de la base de datos.

No se modifica retrospectivamente la candidata de skill v3.9.3-rc.1: su estado
UNKNOWN de srsc describe la evidencia que existía al construirla. Una futura
candidata deberá incorporar esta nueva evidencia y obtener un nuevo checksum.
No se promueve baseline ni se declara equivalencia completa de migración; el
endpoint de secciones activas sigue con la limitación HAL 204 conocida.

## Ejecución

WSL, cwd /home/keilyn/cat:

```bash
/home/keilyn/snibli-audit-venv/bin/python /home/keilyn/snibli-migration-audit/scripts/export_snibli_configuration.py --public-hierarchy srsc --max-seconds 600 --max-requests 500 --output /home/keilyn/snibli-migration-audit/reports/snibli-migration/srsc-hal-tree-20261021
```

Salida: capture_complete=true; snapshot_complete=false; 2 PASS, 0 FAIL,
3 UNKNOWN, 1 NOT_TESTED. Sin credenciales ni cambios de datos DSpace.

## Pruebas

12 casos nuevos de jerarquía: recorrido paginado, hashes raw, timeout, 204,
enlace inseguro, ciclo/duplicado, conteo incompleto, rama vacía contradictoria,
límite de solicitudes, límite de profundidad, restricciones de modo y recorrido
público sin autenticación y rechazo de flags numéricos ambiguos.
Regresión ampliada: **218 passed**, warnings tratados como errores.
Ruff y sintaxis Python 3.11 verificados. Sin commits, PR, despliegues o escrituras.
