# Exportación local autenticada de SNIBLI

No requiere acceso al servidor ni a PostgreSQL. Se ejecuta en el equipo del
operador y solicita usuario/contraseña de DSpace en una terminal interactiva.
Reutiliza `ReadAuthenticatedDSpaceClient` y los métodos paginados existentes de
VERTICAL-022; toda persistencia se limita a archivos en una carpeta nueva.

## Ejecución en el WSL ya preparado

Pegar en una ventana de PowerShell, como una sola línea:

```powershell
wsl -e bash -lc 'cd /home/keilyn/cat && /home/keilyn/snibli-audit-venv/bin/python /home/keilyn/snibli-migration-audit/scripts/export_snibli_configuration.py'
```

El programa pide `Usuario DSpace` y después `Contraseña DSpace (oculta)`.
La contraseña no aparece al escribir, no forma parte del comando ni se guarda
en archivos. No introducirla en el chat. Si la terminal no puede ocultar la
entrada, el programa se detiene antes de hacer solicitudes.

El destino predeterminado es una carpeta nueva y única:

`/home/keilyn/snibli-migration-audit/reports/snibli-migration/authenticated-FECHA-ID/`

El programa imprime su ruta al terminar. Al informar que terminó, la exportación
puede revisarse desde este mismo entorno; no hace falta localizar archivos en
el servidor ni compartir secretos.

## Alternativa nativa PowerShell/CMD

Desde la raíz del checkout Windows, con Python 3.11 o superior:

```powershell
py -3 -m venv .venv-snibli
.\.venv-snibli\Scripts\python.exe -m pip install "httpx>=0.28,<0.29"
.\.venv-snibli\Scripts\python.exe scripts\export_snibli_configuration.py
```

No requiere activar PowerShell scripts ni modificar ExecutionPolicy. Esta
alternativa se implementó con APIs multiplataforma; la ejecución verificada en
esta sesión fue en WSL con Python 3.12.3. La sintaxis se verificó para 3.11.

## Qué se obtiene

- Todos los schemas y campos registrales visibles, incluyendo páginas por schema.
- Submission definitions, sections y forms configurados.
- Inventario de colecciones visibles para la cuenta, sin asignar por conjetura
  la antigua colección piloto a otra colección.
- Vocabularios y sus páginas de valores disponibles por REST.
- `export.json`: envelope `pages_by_surface` consumible por la auditoría existente,
  estado de autenticación, procedencia, errores y límites, sin material de sesión.
- `raw/*.response`: cuerpos JSON/HAL originales, con hashes y referencias por GET.
- `audit.json` y `audit.md`: cobertura, errores, warnings y estados PASS, FAIL,
  UNKNOWN, NOT_TESTED.
- `diff.json` cuando hay comparación observable: formularios/valores contra el
  artefacto v3.9.2 verificado o, si se proporciona `--baseline`, VERTICAL-022 contra
  un envelope anterior. Un fallo de login no genera un diff ficticio.

No es necesario tener un baseline anterior para esta primera captura. La release
preservada permite comparar los dos formularios configurados y vocabularios. Esa
referencia no se presenta como un snapshot ACTIVE del servicio desplegado.

## Colección piloto y observabilidad

Sin `--collection-uuid`, se exportan los inventarios globales. La pertenencia activa
a una colección queda NOT_TESTED/UNKNOWN y el snapshot de contrato no se declara
completo. El UUID y Handle históricos no se usan automáticamente.

Después de identificar y confirmar la colección correcta en `export.json`, se
puede repetir en otra carpeta:

```bash
python scripts/export_snibli_configuration.py --collection-uuid UUID_CONFIRMADO
```

Esto añade la colección, la definición activa y sus secciones enlazadas. HTTP 204
se conserva con el marcador nativo del collector y
`ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204`, sin interpretarlo como sección
vacía ni asignar automáticamente secciones globales a la colección.

Para vocabularios jerárquicos se conserva la respuesta de entries o el fallback
de nodos superiores que ya utiliza el proyecto ante HTTP 404/422. La captura de
nodos superiores no demuestra cobertura del árbol completo; los valores
jerárquicos quedan UNKNOWN. Otros errores no activan ese fallback.

## Cuenta administradora y autorización de esta ejecución

La cuenta aportada por el operador tiene privilegios administrativos. El nombre
del cliente `ReadAuthenticatedDSpaceClient` no reduce esos privilegios en DSpace:
la frontera de transporte del exportador impone el alcance de lectura.

El operador solicitó explícitamente esta captura local con esa cuenta. Se reutiliza
el login existente como excepción para esta herramienta manual; esto no amplía
ADR-018 (limitada a VERTICAL-025A), no habilita autenticación en otras rutas ni
modifica la configuración de la aplicación. El programa no se ejecutó con una
cuenta real durante el desarrollo; las comprobaciones de login son simuladas.

La frontera verifica el origen HTTPS exacto `www.iifl.unam.mx:443` y la base
`/server/api`. No admite un host distinto por CLI. Solo permite los GET explícitos
del inventario y la secuencia existente:

1. GET `/authn/status` para CSRF.
2. Un único POST exacto `/authn/login`.
3. GET `/authn/status` que confirme `authenticated=true`.

No se admiten otros POST, PUT, PATCH, DELETE, rutas de workflow o ítems, ni
redirecciones. No se siguen enlaces de respuestas hacia otros hosts. Tokens,
cookies y contraseña permanecen en memoria; no se exportan cuerpos ni headers
de autenticación. Si un cuerpo de configuración contiene el material de sesión
conocido, no se guarda y la captura queda parcial.

La autenticación puede crear una sesión y registros de acceso en DSpace; no se
modifican contenido, metadatos, permisos o configuración. No hay logout POST,
sincronización con PostgreSQL, promociones de baseline, scheduling o despliegues.

## Límites y resultados parciales

Por defecto: 10 segundos por operación, 180 segundos totales, 200 peticiones,
50 páginas por superficie, tamaño de página 100 y respuestas de hasta 4 MiB.
No hay retries automáticos. Las opciones de límites aceptan únicamente valores
acotados. Una carpeta existente nunca se sobrescribe.

Cada página completada se guarda antes de avanzar. Ante timeout, 401/403,
paginación inválida u otro error se conservan las respuestas ya obtenidas y el
expediente indica incompletitud. Una nueva ejecución usa una carpeta nueva;
no combina páginas de instantes distintos ni promueve snapshots.

Códigos de salida: 1 si hay FAIL; 2 si la captura se interrumpió, no pudo iniciarse
o faltan credenciales; 0 si terminó el inventario solicitado sin errores de captura
ni FAIL. El código 0 puede incluir UNKNOWN/NOT_TESTED: no certifica compatibilidad
completa. `snapshot_complete` distingue además la cobertura de pertenencia activa.

Los archivos pueden contener configuración y colecciones no públicas visibles a
la cuenta administradora; compartirlos solo para la revisión autorizada.
