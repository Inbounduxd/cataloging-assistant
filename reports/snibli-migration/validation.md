# Revisión de implementación y validación — 2026-10-20

## Candidata rc.2 con srsc — 2026-10-21

Se construyó v3.9.3-rc.2 desde rc.1 verificada y los 665 nodos/653 relaciones de
srsc. Incluye los 126 cuerpos originales y validación de reconstrucción del
árbol. Regresión ampliada: 224 passed; seis casos específicos repetidos tras el
último ajuste documental: 6 passed. Skill validada, ZIP y 46 JSON válidos.
Ver reconciliation-proposal/skill-release-rc2.md para checksum y comandos.
v3.9.2 y rc.1 intactas; sin adopción, commits, PR o despliegue.

## Actualización: srsc recuperado por jerarquía HAL — 2026-10-21

El exportador recorre top/children con evidencias y límites. La captura pública
srsc-hal-tree-20261021 terminó con 665 nodos, 653 relaciones y 12 raíces; 126 GET,
cero login y cero errores, hashes raw verificados. Regresión ampliada: 218 passed.
El árbol actual ya está disponible. No se inventa equivalencia con la referencia
histórica incompleta ni se reescribe la skill rc.1. Ver la nueva summary.md y
docs/migrations/SNIBLI-HIERARCHICAL-VOCABULARY-EXPORT.md.

## Revisión final de consumidores — 2026-10-21

Se corrigió además el límite histórico 44 en baseline_diagnose para reutilizar
45/12 del contrato aprobado. Se añadió una regresión que rechaza el límite
anterior. Selección ampliada con consumidores: **195 passed**, `-W error`.
Ver `reconciliation-proposal/final-review.md` para comandos y dependencias del
entorno. srsc permanece UNKNOWN, skill intacta y sin despliegue o commits.

## Actualización 2026-10-21: cambio local aprobado y regresión revisada

El usuario aprobó C1–C3: campo comparativo, tres tipos documentales y orden.
Contrato local `snibli-contract-2026-10-21`: 57 bindings, 55 claves y primer
formulario con 45 bindings. Tres casos nuevos cubren hash efectivo, evidencia
incompleta y checkpoint completo. Los cinco fallos preexistentes se corrigieron
en los dobles de prueba sin debilitar las aserciones ni cambiar sincronización.
Selección ampliada: **154 passed**, `-W error`, sin warnings.

El selector Palabras Clave del borrador 2050 es un autocompletado; abrirlo vacío
no proporciona el árbol completo de srsc, que sigue UNKNOWN. Ver
`reconciliation-proposal/review-completion.md`, `decision.json` y el diff
`local-contract.patch`. Sin commits, PR, producción, cambios de skill v3.9.2,
baseline ACTIVE o sincronizaciones. Las secciones siguientes son historial.

## Actualización 2026-10-21: candidata integrada en auditoría explícita

La CLI implementa `--candidate` junto con `--observed`, validando una referencia
de revisión sin adoptarla, activar runtime o ocultar la diferencia contra la
release preservada. Las 56 identidades históricas y políticas de no escritura
deben conservarse; referencias inseguras o inconsistentes se rechazan.

La comparación offline real está en `candidate-validation-2026-10-21/`: PASS
para los 57 controles, 55 claves e identidad actual de colección. Coinciden los
17 vocabularios planos asociados; srsc y las secciones activas siguen UNKNOWN.
Los dos FAIL contra v3.9.2 se muestran en el mismo informe y se conserva salida 1.
No hay aprobación, promoción ni cambio de contrato runtime implícitos.

13 pruebas nuevas en `test_snibli_candidate_reference.py`; la selección completa
termina en **100 passed**, Ruff PASS. Ver `summary.md` de esa carpeta para el
comando, archivos y límites. No cambió código de producción API o skill; no hubo
red, credenciales, PostgreSQL, commits, PR o despliegues en esta fase.

## Última actualización: propuesta de conciliación preparada

Se añadió `reconciliation-proposal/` con `proposal.md`,
`candidate-contract.json`, `decision.json` y `validation.json`. La candidata
describe los 57 controles observados y sus 55 claves, conserva las 56 referencias
históricas y las políticas de no escritura y aprobación humana. Incluye el
binding adicional y las tres adiciones literales a `common_types` como cambios
propuestos, sin activar runtime o asignar una versión futura de skill.

Estado: CANDIDATE_REVIEW_REQUIRED / PENDING_HUMAN_REVIEW. La intención semántica
institucional del nuevo control sigue pendiente; no se inventó una aprobación a
partir de la instrucción de continuar. HTTP 204 de secciones y jerarquía parcial
de `srsc` se mantienen sin resolver. La propuesta no promueve un baseline ACTIVE.

La validación documental verificó los 57 controles, 55 claves registradas,
identidades únicas, los 64 cuerpos raw por SHA-256 y el checksum de la release
v3.9.2, sin modificar las fuentes. PASS se limita a fidelidad de esta candidata;
la equivalencia completa permanece UNKNOWN. No cambió código ni se repitieron
pruebas; se mantienen 87 aprobadas. Sin red, credenciales, escrituras DSpace/SQL,
commits, PR, cambios de skill, despliegue o cron.

## Última actualización: colección y definición confirmadas

La captura `authenticated-20261021T055428Z-8a836a27/` confirma la colección
«Lingüística Maayat'aan, Maya», UUID `3ce3afb3-94ed-4f60-bfda-0a1242c4d689`,
Handle `123456789/393`, y la definición `traditional` mediante consulta autenticada.
El enlace de sus secciones devuelve HTTP 204, conservado como
`ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204`; `srsc/entries` devuelve 422 y
su fallback solo observa nodos superiores. Esas son las limitaciones pendientes,
no un fallo de autenticación. No se recomiendan más ejecuciones idénticas.

La segunda captura reproduce exactamente los controles configurados y resultados
de vocabularios de la primera. Permanecen el binding adicional `dc.type.genre`,
29 desplazamientos de orden y las tres adiciones a `common_types`. Las 54 claves
de referencia siguen presentes con IDs y scopeNote idénticos. No se declara
pertenencia completa de secciones ni equivalencia total con un baseline ACTIVE.

La revisión offline con hashes de ambas capturas está en `review.audit.md`,
`review.audit.json` y `review.diff.json` dentro de esa segunda carpeta. Los
originales no se sobrescribieron. No cambió código ni se repitieron pruebas sin
causa; se mantienen 87 pruebas aprobadas. El siguiente paso es revisión humana
del drift y evidencia autorizada de la pertenencia activa no observable por REST.
No hubo escrituras DSpace/PostgreSQL, cambios de skill/despliegue, commits o PR.

## Última actualización: captura autenticada real revisada

El operador ejecutó el exportador y guardó
`authenticated-20261021T054455Z-3f4b1023/`. El login fue exitoso. Las 64 peticiones
conservaron inventarios de registro, configuración, colecciones y vocabularios.
El flag parcial procede del 422 de `srsc/entries` (fallback a nodos superiores,
sin árbol completo) y de no haber seleccionado colección en esa primera corrida.

Hay drift comprobable frente a la release preservada: 57 bindings y 55 claves
en los dos formularios configurados, conservando los 56 bindings originales;
se añade `dc.type.genre` con etiqueta «¿Es un texto comparativo?» y `genrePairs`.
Hay 29 desplazamientos de posición y ningún otro cambio en las dimensiones
comparadas de los bindings compartidos. `common_types` conserva sus 23 valores y
añade «Códice», «Reseña» y «Documento Colonial». De los vocabularios de referencia,
19 coinciden, uno difiere y `srsc` queda UNKNOWN.

El comparador tenía una clasificación incorrecta: confundía las claves esperadas
con el registro observado y marcaba el binding adicional como no registrado y
UNKNOWN. Ahora consulta el registro capturado y clasifica el drift observable
como FAIL, sin ocultarlo por warnings de otra superficie. Se añadieron dos pruebas
de regresión: **87 passed** en la selección completa y Ruff PASS. No se cambiaron
las expectativas de pruebas anteriores ni el cliente o código de producción.

Los archivos originales de esa corrida permanecen intactos. La revisión está en
`authenticated-20261021T054455Z-3f4b1023/review.audit.md`, `review.audit.json` y
`review.diff.json`, con hashes de procedencia y VERTICAL-022 para el diff acotado
de bindings. No se presenta esa referencia como un snapshot ACTIVE histórico.

El operador identificó la colección actual «Lingüística Maayat'aan, Maya», UUID
`3ce3afb3-94ed-4f60-bfda-0a1242c4d689`, Handle `123456789/393`, verificada en el
inventario. Su consulta de definición activa sin sesión devuelve 401; falta una
captura autenticada con ese UUID explícito. No se infiere equivalencia con la
antigua piloto. No se retuvieron contraseñas ni tokens para repetir el login.
No se modificaron DSpace, PostgreSQL, despliegue, skill o cron; sin commits ni PR.

## Última actualización: exportador local autenticado preparado

El operador informó que dispone de una cuenta administradora de DSpace y solicitó
obtener la configuración desde un script local. Se añadió
`scripts/export_snibli_configuration.py`, con contraseña interactiva oculta,
reutilización del cliente de login existente y persistencia exclusivamente en
archivos locales. No se utilizó una cuenta real durante esta sesión.

La herramienta bloquea en transporte todo destino distinto de la REST HTTPS
verificada y todo método distinto de los GET explícitos y un único POST exacto
de login. Los permisos administrativos de la cuenta no se presentan como permisos
de solo lectura: es el transporte de esta herramienta el que impone esa frontera.
No se modificó ADR-018 ni se amplió la autenticación de otras capacidades.

Exporta los inventarios globales y sus páginas, y opcionalmente la pertenencia
activa de una colección indicada explícitamente. Compara formularios y valores
observables contra v3.9.2 sin necesitar un snapshot histórico previo; no confunde
esa referencia preservada con el ACTIVE desplegado. HTTP 204, jerarquías parciales
y fallos de red o autorización se mantienen como evidencia incompleta.

Se añadieron 23 pruebas en `test_snibli_configuration_export.py`. La selección
anterior más ese archivo termina en **85 passed**, sin red real ni PostgreSQL.
Ruff, ayuda CLI y sintaxis Python 3.11: PASS. Entorno de ejecución: WSL, Python
3.12.3; no se afirma validación nativa de Windows ni autenticación institucional
real. La guía operativa es `docs/migrations/SNIBLI-AUTHENTICATED-LOCAL-EXPORT.md`.

Comando de la selección anterior, agregando:

```bash
"$REPO/apps/api/tests/test_snibli_configuration_export.py"
```

Ayuda CLI comprobada sin credenciales ni tráfico de red:

```bash
python3 "$REPO/scripts/export_snibli_configuration.py" --help
```

La ejecución autenticada queda para el operador en su terminal. No debe introducir
su contraseña en el chat. Siguen sin crearse commits, PR o tareas programadas ni
cambios en producción, PostgreSQL, despliegue o skill. Los resultados públicos
anteriores conservan su alcance; aún no existe una captura autenticada real.

## Última actualización: registro y colecciones públicos paginados

Se completó el inventario público con el cliente existente: 18 schemas (una
página), 293 campos (tres páginas) y 455 colecciones (cinco páginas), en nueve GET.
Las 54 claves del contrato coinciden exactamente con IDs, identidad y scopeNote
del perfil incluido en la release v3.9.2 verificada. El diff acotado está en
`public-registry/diff.json`; no presenta cambios y declara explícitamente que no
es una comparación del contrato completo ni contra el ACTIVE desplegado.

Ninguna de las 455 colecciones públicas presenta el UUID o Handle históricos.
El diagnóstico agregado ahora contiene 7 PASS, 2 FAIL (las dos comprobaciones de
la referencia piloto), 1 UNKNOWN y 6 NOT_TESTED. Ver `public-registry/audit.md` e
`inventory.json` para las respuestas brutas, procedencia y límites. Formularios
activos y vocabularios continúan requiriendo evidencia autorizada. No cambió
código de producto ni se ejecutó autenticación o persistencia en PostgreSQL.
Las secciones siguientes conservan la historia de comprobaciones anteriores.

## Actualización: REST pública identificada

Se verificó `https://www.iifl.unam.mx/server/api` mediante configuración pública y
el entry point anunciado por el HAL Browser del backend. La raíz responde con
HAL+JSON y declara DSpace 7.6.6. El UUID piloto histórico y el resolver del Handle
histórico devolvieron HTTP 404; las superficies de formularios y vocabularios
requieren autenticación (HTTP 401). El registro anuncia 293 campos, frente a 292
históricos, sin comparación semántica completa todavía.

Ver `rest-discovery.md` y `rest-discovery.json` para la cadena de descubrimiento,
evidencia y límites. `audit.json` y `audit.md` ahora corresponden a la ejecución con
REST explícita: 6 PASS, 1 FAIL, 1 UNKNOWN, 6 NOT_TESTED. El diagnóstico público
anterior se conserva en `public-only/`. No se generó diff ni se modificó runtime.
Las menciones siguientes a REST pendiente describen el estado histórico inicial;
siguen pendientes autenticación de lectura autorizada, correspondencia de la
colección y capturas comparables. No cambió código en esta fase.

## Estado actualizado: fallos locales corregidos

Tras la autorización «Adelante», se corrigieron las fixtures de los tres archivos
de pruebas existentes, sin modificar las aserciones ni el código de producción:

- `test_dspace_contract_snapshot.py`: `_paged` copia en profundidad sus valores
  para representar respuestas HTTP independientes. Se añadió una prueba que impide
  volver a compartir estado entre las superficies global y por esquema.
- `test_dspace_contract_resolution.py`: la fixture utiliza los helpers existentes
  `live_dspace_label` y `live_dspace_selector_label`. Una comprobación literal fija
  el par `Identificador` / `ISSN`; tres casos negativos rechazan el label confundido
  con el selector, el selector ausente y un selector incorrecto.
- `test_dspace_contract_sync_204.py`: el mock acepta el argumento posicional
  `session`, conforme a la firma real. Tres casos negativos comprueban que HTTP
  401, 403 y 500 se propagan y no crean evidencia falsa de secciones no observables.

La misma selección de ocho archivos de pruebas documentada abajo, con ocho casos
adicionales, termina en **62 passed**. Ruff y `git diff --check`: PASS. Se ejecutó
en WSL desde `/home/keilyn/cat`, con el entorno aislado ya preparado. Comando:

```bash
REPO=/home/keilyn/snibli-migration-audit
PYTHONPATH="$REPO/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python -m pytest \
  "$REPO/apps/api/tests/test_snibli_migration_audit.py" \
  "$REPO/apps/api/tests/test_cataloging_contract.py" \
  "$REPO/apps/api/tests/test_dspace_contract_snapshot.py" \
  "$REPO/apps/api/tests/test_dspace_contract_live_reconciliation.py" \
  "$REPO/apps/api/tests/test_dspace_contract_client.py" \
  "$REPO/apps/api/tests/test_dspace_contract_client_surfaces.py" \
  "$REPO/apps/api/tests/test_dspace_contract_resolution.py" \
  "$REPO/apps/api/tests/test_dspace_contract_sync_204.py" -q --tb=short
```

Además de los archivos añadidos originalmente, ahora hay cambios revisables en
esos tres archivos de pruebas. Los tres fallos descritos en el expediente inicial
de abajo están resueltos. Siguen pendientes la REST real y la validación de la
migración con evidencia autorizada. El diagnóstico público anterior no se ha
reclasificado como comparación completa. No se hicieron nuevos accesos a DSpace,
ni cambios en PostgreSQL, producción, configuración, skill o tareas programadas.
No se crearon commits ni PR.

## Expediente inicial (histórico, antes de corregir las fixtures)

Repositorio solicitado: `Inbounduxd/cataloging-assistant`.
Commit de partida: `29227ddf8e27a1f27803d0241f3dd4c64b2b72be`.
Checkout de ejecución: `/home/keilyn/snibli-migration-audit` en WSL.
Comandos de desarrollo ejecutados desde `/home/keilyn/cat`, conforme a AGENTS.md
y a la decisión del usuario de conservar WSL. No se ejecutó Python nativo Windows.
Existe una copia para revisión en Windows en `tmp/snibli-migration-audit`.

## Resultado observado

- URL pública institucional: HTTP 200; sin redirección observada.
- Release v3.9.2: SHA-256, 118470 bytes, CRC ZIP, 86 archivos y 36 JSON verificados.
- Contrato local: 56 bindings y 54 claves únicas, `dc.subject.linguiscgroup`
  literal, lengua de registro independiente, aprobación humana y escritura bloqueada.
- El contrato Python aún declara `dspace-cataloger-v3.9.1`; el registro de release
  declara v3.9.2. La CLI advierte la diferencia sin cambiar ninguno.
- Resultado de la ejecución pública: 5 PASS, 0 FAIL, 1 UNKNOWN, 7 NOT_TESTED.
- REST nueva, identidad de instancia, contrato efectivo, vocabularios y Golden Set
  sobre la instancia nueva: sin verificar. No se suministraron API ni credenciales.
- No se generó `diff.json`: no hay dos exportaciones HAL comparables de la migración.
  La conciliación histórica de 2026-08-26 no se presentó como evidencia nueva.

## Archivos añadidos

- `scripts/audit_snibli_migration.py`: CLI estándar Python 3.11+, red pública GET
  limitada, validación local de release y comparación de exportaciones VERTICAL-022.
- `apps/api/tests/test_snibli_migration_audit.py`: 22 pruebas nuevas simuladas.
- `docs/migrations/SNIBLI-LOCAL-AUDIT-CLI.md`: uso PowerShell/CMD, formato de
  exportaciones, seguridad, cobertura y límites.
- `reports/snibli-migration/audit.json` y `audit.md`: diagnóstico público real.
- `reports/snibli-migration/validation.md`: este expediente de implementación.

Se reutilizan `contract_payload`, `build_contract_snapshot`,
`diff_contract_snapshots` y el normalizador de bindings existente. No se creó un
collector paralelo de formularios/metadatos ni se ejecutó `contract_job`, pues
escribe snapshots locales en PostgreSQL. El cliente autenticado existente queda
reservado para el procedimiento operativo aprobado; la CLI no recibe ni transmite
credenciales. La comparación offline no constituye captura autenticada nueva.

## Comandos principales

Preparación, en WSL desde `/home/keilyn/cat`:

```bash
git clone https://github.com/Inbounduxd/cataloging-assistant.git /home/keilyn/snibli-migration-audit
python3 -m venv --system-site-packages /home/keilyn/snibli-audit-venv
/home/keilyn/snibli-audit-venv/bin/python -m pip install 'respx>=0.22,<0.23' 'ruff>=0.12,<0.13'
```

Python de ejecución: 3.12.3. Ruff: 0.12.12. Respx: 0.22.0.
La CLI no necesita esas dependencias; se instalaron en el entorno aislado para
las pruebas de cliente existentes y lint. Se comprobó además la sintaxis Python
3.11 con `ast.parse(feature_version=(3, 11))` en la CLI y sus dos módulos de contrato.
No se afirma haber probado el runtime 3.11 ni la ejecución nativa Windows.

Con `REPO=/home/keilyn/snibli-migration-audit`:

```bash
python3 "$REPO/scripts/audit_snibli_migration.py" --offline
python3 "$REPO/scripts/audit_snibli_migration.py" --timeout 5
/home/keilyn/snibli-audit-venv/bin/ruff format "$REPO/scripts/audit_snibli_migration.py" "$REPO/apps/api/tests/test_snibli_migration_audit.py"
/home/keilyn/snibli-audit-venv/bin/ruff check --config "$REPO/apps/api/pyproject.toml" "$REPO/scripts/audit_snibli_migration.py" "$REPO/apps/api/tests/test_snibli_migration_audit.py"
PYTHONPATH="$REPO/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python -m pytest "$REPO/apps/api/tests/test_snibli_migration_audit.py" -q
```

Lint: PASS. Pruebas nuevas: **22 passed**.

Regresión seleccionada, sin PostgreSQL ni solicitudes externas:

```bash
PYTHONPATH="$REPO/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python -m pytest \
  "$REPO/apps/api/tests/test_snibli_migration_audit.py" \
  "$REPO/apps/api/tests/test_cataloging_contract.py" \
  "$REPO/apps/api/tests/test_dspace_contract_snapshot.py" \
  "$REPO/apps/api/tests/test_dspace_contract_live_reconciliation.py" \
  "$REPO/apps/api/tests/test_dspace_contract_client.py" \
  "$REPO/apps/api/tests/test_dspace_contract_client_surfaces.py" \
  "$REPO/apps/api/tests/test_dspace_contract_resolution.py" \
  "$REPO/apps/api/tests/test_dspace_contract_sync_204.py" -q --tb=short
```

Resultado: **51 passed, 3 failed**. Los fallos se reprodujeron por separado,
sin importar la CLI nueva. `git diff --exit-code HEAD -- apps/api/src skills` y
la misma comprobación para los tres archivos de pruebas existentes no mostraron
cambios. No se modificaron pruebas ni producción para hacerlos pasar.

1. `test_registry_coverage_mismatch_makes_snapshot_incomplete`: esperaba incompleto,
   obtuvo completo. La fixture comparte la lista `registry` entre la superficie
   global y por esquema; eliminar de una también modifica la otra.
2. `test_valid_204_reconciliation_overlay_is_accepted`: el validador devuelve
   `resolved_binding_label_mismatch`. La fixture usa etiquetas de presentación
   donde el código actual espera el label bruto DSpace y selector por separado.
3. `test_active_sections_204_is_persisted_as_unobservable_not_raised`: el mock
   `_raise_204` solo admite kwargs, pero el collector pasa `session` posicional.

La primera tentativa de regresión no tuvo `PYTHONPATH` y falló al importar el
paquete; se corrigió el comando, sin modificar los tests existentes. El primer
import de la fixture en la prueba nueva se corrigió a import relativo del paquete.
Las primeras observaciones de Ruff se corrigieron únicamente en archivos nuevos.

## Pendientes para la revisión humana

Identificar y autorizar la REST real; aportar capturas completas de VERTICAL-022 y
vocabularios con su procedencia; confirmar colección, ítems, bitstreams y permisos;
ejecutar GR01–GR23 en el entorno aprobado; resolver los tres fallos de regresión
existentes y revisar la diferencia de versión declarada. Mientras tanto, la
migración no queda declarada compatible. Los tests Golden de ingesta con base de
datos se excluyeron para respetar la prohibición de modificar PostgreSQL.

No se crearon commits, PR, despliegues, escrituras DSpace/PostgreSQL, cambios de
variables o artefactos de skill, ni sincronizaciones o tareas programadas.
