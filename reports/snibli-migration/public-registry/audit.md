# Revisión pública del registro SNIBLI — 2026-10-20

**PASS: 54/54 claves del contrato coinciden exactamente con el perfil de registro
preservado dentro de dspace-cataloger v3.9.2.** La equivalencia completa de la
migración sigue sin establecerse.

Se reutilizaron `DSpaceClient.get_metadata_schemas_page`,
`get_metadata_fields_page`, el parser paginado del cliente y el motor
`diff_contract_snapshots` de VERTICAL-022. No se ejecutó el collector con
persistencia, autenticación, promoción de snapshots ni jobs de sincronización.

## Evidencia observada

- 18 esquemas: 1 página.
- 293 campos de registro: 3 páginas de hasta 100 registros.
- 455 colecciones públicas: 5 páginas de hasta 100 registros.
- 54 claves esperadas: 54 presentes, sin discrepancias de ID, clave,
  element/qualifier o scopeNote. `dc.subject.linguiscgroup` permanece literal.
- Ninguna de las 455 colecciones públicas coincide con el UUID histórico
  `e9a8f44f-a8d3-4d22-b02a-cf590285bac6` ni el Handle `123456789/4`.

El inventario valida números de página, estabilidad de totales y recuentos finales.
También verifica claves de metadatos y UUID de colecciones únicos. Cada campo
conserva el schema explícito embebido en HAL; no se dedujo por nombre.

## Diff y alcance

`diff.json` contiene `scope: PUBLIC_REGISTRY_54_KEYS_ONLY`,
`full_contract_comparison: false`, baseline y observación normalizadas, hashes
semánticos y `changes: []`. La baseline procede del asset
`metadataRegistryForTraditionalForms` del perfil incluido en el artefacto
verificado v3.9.2, no del snapshot ACTIVE del servicio desplegado.

Los otros 239 campos actuales quedan fuera de esa comparación: no se dispone
del registro bruto histórico completo de 292 campos para identificar la diferencia
global de uno. No se declaran todos esos campos como adiciones.

`inventory.json` conserva páginas HAL brutas, endpoints con sus parámetros,
timestamps UTC, SHA-256 y referencias a las respuestas originales `.response`.
Se hicieron 9 GET, sin credenciales ni cookies, sin proxies de entorno, sin
redirecciones ni retries, exclusivamente a los tres endpoints públicos del host
verificado. Límites: 12 segundos por página, 90 por ejecución, 4 MiB por respuesta,
10 páginas por superficie y 20 peticiones como máximo.

No encontrar la piloto significa que no es visible con sus referencias históricas
en este inventario público; no prueba su eliminación ni autoriza asignar otra por
parecido de nombre. El administrador debe confirmar la correspondencia.

Las pruebas anteriores siguen en 62 aprobadas; en esta fase solo se generó
evidencia pública, sin cambios en código de producto. No se repitieron suites
sin modificaciones que lo justificaran. El análisis se ejecutó en WSL desde
`/home/keilyn/cat` con:

```bash
/home/keilyn/snibli-audit-venv/bin/python /tmp/snibli_public_registry.py
```

El script de análisis se conserva también en el workspace Windows como
`tmp/snibli_public_registry.py`. Formularios efectivos, 56 bindings, valores de
vocabularios, permisos y GR01–GR23 live siguen pendientes. Las superficies de
configuración requieren autenticación, por lo que no se ejecutaron más solicitudes
contra ellas ni se intentó iniciar sesión.

Sin cambios en producción, PostgreSQL, variables de despliegue, skill o tareas
programadas. Sin commits ni PR.
