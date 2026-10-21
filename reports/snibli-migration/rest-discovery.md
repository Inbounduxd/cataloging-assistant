# Descubrimiento público de REST SNIBLI — 2026-10-20

Actualización posterior: se completaron las páginas públicas de registro y
colecciones. Las 54 claves del contrato coinciden con el perfil preservado de
v3.9.2; no hubo coincidencias del UUID o Handle piloto entre las 455 colecciones
públicas. Ver `public-registry/audit.md`, `inventory.json` y el diff limitado en
`public-registry/diff.json`. Los recuentos y páginas parciales descritos debajo
corresponden al momento del descubrimiento inicial. El diagnóstico agregado
`audit.json`/`audit.md` fue complementado: 7 PASS, 2 FAIL, 1 UNKNOWN, 6 NOT_TESTED.

REST verificada mediante GET y HAL+JSON: **https://www.iifl.unam.mx/server/api**.
La compatibilidad completa de la migración permanece **UNKNOWN**.

La ruta se obtuvo de evidencia explícita: el HTML declara base `/SNIBLI/` y enlaza
`main.c6d5cfd5ea7ee9be.js`; ese bundle ejecuta `fetch("assets/config.json")`.
La configuración declara `rest.baseUrl = https://www.iifl.unam.mx/server`.
Esa dirección redirige con HTTP 308 a `/server/`, cuya página HAL Browser declara
`entryPoint: window.location.pathname + 'api'`. La entrada resultante devuelve
HTTP 200, Content-Type `application/hal+json` y `type: root`.
No se derivó la API del frontend ni se probaron rutas REST por conjetura.

## Resultados

- **PASS**: la raíz declara DSpace 7.6.6, nombre `Respositorio Ind`, UI institucional
  `https://www.iifl.unam.mx/SNIBLI` y servidor `https://www.iifl.unam.mx/server`.
- **FAIL**: el UUID piloto histórico `e9a8f44f-a8d3-4d22-b02a-cf590285bac6`
  devuelve HTTP 404. Es un fallo de recuperación de la referencia, no prueba de
  eliminación ni de sustitución de la base.
- **FAIL**: el resolver PID anunciado en HAL, con `id=123456789/4`, devuelve
  HTTP 404. No se asignó otro Handle ni UUID por semejanza de nombres.
- **UNKNOWN**: el registro anuncia 293 campos frente a 292 históricos. Se capturó
  una de 15 páginas; todavía no se determinó la diferencia semántica. Los 18
  schemas caben en una sola página. La lista de colecciones anuncia 455 entradas;
  se capturó únicamente la primera página, sin buscar reemplazos automáticamente.
- **UNKNOWN**: submission definitions, forms, sections y vocabularies devuelven
  HTTP 401. El estado de autenticación confirma `authenticated: false`.
- **UNKNOWN**: los 56 bindings, las 54 claves del contrato, el orden activo,
  vocabularios y GR01–GR23 requieren evidencia adicional. No se generó `diff.json`.

`audit.json` y `audit.md` contienen la ejecución de la CLI con la REST explícita:
6 PASS, 1 FAIL, 1 UNKNOWN, 6 NOT_TESTED. El proceso devolvió código 1 por el 404
de la colección piloto. `public-only/` conserva el diagnóstico anterior.

## Evidencia y límites

`rest-discovery.json` conserva fechas UTC, endpoints, estados, redirecciones,
hashes SHA-256 y referencias a los cuerpos originales en `discovery/`.
Los assets se analizaron como texto; no se ejecutó JavaScript remoto.
Se hicieron exclusivamente GET anónimos, con límite de 12 segundos y 4 MiB por
respuesta, sin seguir redirecciones entre orígenes. El resolver PID se consultó
con curl sin configuración local, cookies, credenciales, proxies ni redirecciones.
Su cuerpo HTTP 404 vacío se preservó; el intento de interpretarlo como JSON
falló y no se trató como HAL válido.

## Siguiente evidencia necesaria

Un operador autorizado debe confirmar la correspondencia de la colección piloto
por UUID y Handle y explicar los 404. Después se necesitan exportaciones HAL
completas del baseline aprobado y de la instancia nueva, mediante VERTICAL-022,
además de los valores de vocabularios. La cuenta de lectura debe provisionarse
en un entorno autorizado; no enviar contraseñas por el chat. El job existente
persiste en PostgreSQL y continúa fuera de esta auditoría local sin escrituras.

La URL verificada queda como evidencia para revisión. No se cambiaron variables,
producción, PostgreSQL, skill, permisos ni sincronizaciones; no hubo login,
commits o PR. El código no cambió en esta fase: siguen vigentes las 62 pruebas
aprobadas de la validación anterior.
