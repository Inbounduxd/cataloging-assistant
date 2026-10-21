# dspace-cataloger v3.9.3-rc.2 — 2026-10-21

**LOCAL_CANDIDATE_NOT_ADOPTED_NOT_REPOSITORY_PRESERVED**.
El usuario aprobó preparar esta candidata con el srsc recuperado. No se interpreta
esa aprobación como adopción, instalación, publicación, commit, PR o despliegue.

## Artefacto completo

Ruta: `skills/dspace-cataloger/versions/v3.9.3-rc.2/`.

- Paquete: `dspace-cataloger-v3.9.3-rc.2.skill`.
- Fuente completa: `source/dspace-cataloger/`.
- Manifiesto: `manifest.json`, con hashes de cada miembro y datos de procedencia.
- SHA-256: `c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae`.
- Tamaño: 401872 bytes; 225 miembros, 46 JSON válidos.
- Padre directo: rc.1 local, checksum
  `d4bcb41c342f31150a1da7244550b319de1ae2a71a83b401bd2f05222feffa49`.

## Qué incorpora

srsc actual expuesto por HAL: **665 nodos seleccionables, 653 relaciones y 12
raíces**. Se incluyen el árbol normalizado, el export original y las 126
respuestas HAL sin credenciales. La captura original es
`reports/snibli-migration/srsc-hal-tree-20261021/`, SHA-256 de export.json
`af9f23beadacf6793b3495df28f38f59dec3b61034219e1dac518ba52a511f0e`.

El constructor nuevo reconstruye nodos y relaciones desde las páginas originales,
comprueba hashes, paginación, ramas, raíces y ausencia de duplicados/ciclos, y
rechaza discrepancias con el árbol normalizado. Los valores del índice respetan
selectable; no se infiere esa propiedad por ser padre u hoja. Se conserva el
contexto jerárquico completo en assets/srsc-tree.json.

El índice de vocabularios y el perfil se actualizan conjuntamente. El contrato
sigue en 57 bindings/55 claves. El payload ejecutable y su hash permanecen iguales
a rc.1; no se habilita inferencia, propagación lingüística, escritura o mutaciones.
GR01–GR23 se conservan byte por byte, incluida la protección ORCID/ISSN. La captura
del árbol no constituye nueva adjudicación del Golden Set.

La documentación actual distingue PASS_CURRENT_HAL_CAPTURE de equivalencia
histórica UNKNOWN. La referencia de secciones activas por HAL sigue limitada por
HTTP 204, y fullMigrationEquivalence sigue UNKNOWN. La captura demuestra el árbol
alcanzable durante su recorrido, no un snapshot atómico o equivalencia byte a byte
con el XML del servidor.

## Validación y reproducción

WSL, cwd `/home/keilyn/cat`:

```bash
task_repo=/home/keilyn/snibli-migration-audit
PYTHONPATH="$task_repo/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python "$task_repo/scripts/build_snibli_skill_rc2.py" --output /tmp/snibli-rc2-review-new
```

La salida debe ser una carpeta nueva; no permite sobrescribirla. El ZIP utiliza
orden y timestamps fijos. Los inputs son rc.1 fijada por checksum y la captura
guardada; no hay red ni autenticación durante la construcción.

Seis pruebas nuevas: reconstrucción de la captura raw; concordancia de activos,
payload, lock y Golden Set; ZIP determinista y JSON válidos; rechazo de raw
alterado; rechazo de relaciones alteradas aunque el envelope se vuelva a hashear;
rechazo de un padre distinto.

Regresión ampliada: **224 passed**, warnings tratados como errores. Tras el
ajuste final de procedencia/aprobación y etiqueta de ancestro en la guía, se
repitieron las seis pruebas específicas: **6 passed**. Quick_validate de
skill-creator, Ruff y git diff --check: PASS.

## Preservación y revisión

La rc.1 conserva su checksum y no se modificó. v3.9.2, README.md y
CURRENT_RELEASE.md siguen idénticos a HEAD. No se afirma preservación en GitHub
de candidatas locales sin commit. No se modificó producción ni PostgreSQL,
no se promovió baseline ni se activó sincronización.

El nuevo constructor y sus seis pruebas son los archivos de código añadidos en
esta fase; no cambió la API ejecutable. El paquete y su manifiesto constituyen
la entrega revisable. Adoptar o publicar requiere una acción futura separada.
