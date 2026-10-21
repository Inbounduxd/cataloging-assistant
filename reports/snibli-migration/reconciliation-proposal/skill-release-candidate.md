# Skill v3.9.3-rc.1 — candidata local

Estado: **LOCAL_CANDIDATE_NOT_ADOPTED_NOT_REPOSITORY_PRESERVED**.
Preparación autorizada por el usuario tras la propuesta explícita de nueva release.
No se modifican v3.9.2 ni los punteros de versión vigente.

## Entrega

Directorio: `skills/dspace-cataloger/versions/v3.9.3-rc.1/`.

- Artefacto completo: `dspace-cataloger-v3.9.3-rc.1.skill`.
- Fuente completa: `source/dspace-cataloger/`, 95 miembros del paquete.
- Manifiesto externo: checksum del ZIP, tamaño, hashes individuales y procedencia.
- SHA-256: `d4bcb41c342f31150a1da7244550b319de1ae2a71a83b401bd2f05222feffa49`.
- Tamaño: 156588 bytes. ZIP y todos los JSON validados.

## Cambios y fidelidad

Contrato de formularios con 57 bindings/55 claves; perfil de instancia con
proyección explícita de evidencia capturada (no nueva captura live); registro
de claves y vocabularios coherentes. genrePairs y common_types incluyen las
aprobaciones C1/C3; se conserva el orden aprobado C2. La clave
`dc.subject.linguiscgroup` no cambia.

El hash del contrato ejecutable local se calcula sobre su JSON canónico y se
incluye junto con el payload. No se identifica un commit inexistente ni un
runtime desplegado. El nombre histórico runtime-contract-lock-v3.9.json se
conserva como ruta compatible, con contenido actualizado explícito para la candidata.

El padre directo es el artefacto verificado v3.9.2, SHA-256
`b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede`.
Los activos primarios reemplazados se incluyen también como copias históricas
dentro del paquete; las referencias heredadas remiten al documento actual para
URL, conteos, orden y hash. Se preservan GR01–GR23 byte por byte y sus reglas,
incluida la protección ORCID/ISSN. No se presenta su retención como nueva
adjudicación o evaluación humana de los cambios.

## Reproducción y pruebas

En WSL desde `/home/keilyn/cat`, usando el entorno de auditoría:

```bash
task_repo=/home/keilyn/snibli-migration-audit
PYTHONPATH="$task_repo/apps/api/src" /home/keilyn/snibli-audit-venv/bin/python "$task_repo/scripts/build_snibli_skill_candidate.py" --output /tmp/snibli-skill-review-new
```

La salida debe ser un directorio nuevo. El constructor no permite sobrescribirlo.
El ZIP usa orden de miembros y timestamps fijos para reproducción determinista.
Los inputs incluyen la candidata histórica, decision.json, padre verificado y
payload ejecutable local; modificar uno puede cambiar el checksum de salida.

Cinco pruebas nuevas verifican fidelidad de GR01–GR23, consistencia de perfil,
contrato/vocabularios/hash, empaquetado determinista, rechazo sin aprobación y
rechazo de drift literal del runtime. Regresión ampliada: **200 passed**, `-W error`.
Tras corregir el padre directo heredado en el manifiesto se repitieron los cinco
casos específicos: **5 passed**. Validador quick_validate de skill-creator: PASS.
Ruff y git diff --check verificados. No se alteraron pruebas históricas de Golden Set.

## Límites

srsc completo sigue UNKNOWN, con values=null, no una lista vacía inventada.
Las secciones HAL siguen no observables por HTTP 204; la evidencia visual queda
limitada al borrador 2050. La candidata no declara equivalencia completa.
No habilita escritura, OCR, mutaciones de agente, inferencia del campo nuevo,
promoción de baseline ni sincronización. No se creó commit, PR, instalación,
publicación o despliegue. Por gobernanza, sin commit no se declara preservada en
GitHub ni cambia CURRENT_RELEASE.md. La adopción será una acción futura separada.

Skill utilizada para preparar y validar: skill-creator, ubicada en
`C:/Users/Jose Paul/.codex/skills/.system/skill-creator/SKILL.md`.
