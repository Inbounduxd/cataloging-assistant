# Entrega de auditoría local SNIBLI — 2026-10-21

**Candidata actual de revisión: v3.9.3-rc.2**, que incorpora el srsc capturado y
sus respuestas HAL originales. Ver [informe de rc.2](reconciliation-proposal/skill-release-rc2.md).
No se adoptó ni desplegó. Las cifras y candidatas anteriores de este documento
se conservan como historial.

**Actualización posterior:** se recuperó la jerarquía pública alcanzable de srsc
por REST/HAL: 665 nodos, 653 relaciones y 12 raíces, 126 GET, sin login ni errores.
Ver [nueva evidencia](srsc-hal-tree-20261021/summary.md). La falta de captura del
árbol actual indicada abajo queda resuelta; la equivalencia histórica sigue sin
referencia completa. El contenido siguiente conserva el diagnóstico previo.

**Conclusión: diagnóstico parcial entregado; equivalencia completa de migración UNKNOWN.**
La preparación local está terminada. La evidencia disponible respalda el cambio
de contrato aprobado, pero no permite certificar toda la instancia.

## Resultados

| Alcance | Resultado |
|---|---|
| Página institucional | PASS, HTTP 200 en el diagnóstico público guardado |
| Skill preservada v3.9.2 | PASS de integridad; permanece vigente e intacta |
| Contrato local aprobado | PASS: 57 bindings y 55 claves únicas |
| Captura autenticada frente a candidata | Coinciden 57 bindings, 55 claves, colección y 17 vocabularios planos |
| Diferencias frente a v3.9.2 | Dos FAIL de comparación histórica: nuevo control/orden y valores documentales; cambios aprobados por el usuario |
| srsc completo | UNKNOWN; entries devolvió 422 y el fallback solo aportó nodos superiores |
| Secciones activas por HAL | UNKNOWN por HTTP 204; el borrador 2050 aporta evidencia visual independiente y limitada a ese caso |
| Identidad completa de base de datos | UNKNOWN; coincidencia de UUID/Handle no basta para probarla |

Las comparaciones offline describen la captura conservada, no una comprobación
en tiempo real de todos los cambios posteriores en DSpace.

## Cambio aprobado y candidata

El usuario aprobó el nuevo control `dc.type.genre`, sus valores Sí / No /
Incluye Datos de Diferentes Lenguas, la adición de Códice / Reseña /
Documento Colonial a common_types y el orden observado. Se conserva literalmente
`dc.subject.linguiscgroup`, la separación de ejes lingüísticos, la aprobación
humana y la prohibición de escritura automática.

Contrato de aplicación propuesto: `snibli-contract-2026-10-21`.
Skill candidata local: `v3.9.3-rc.1`, no adoptada, instalada o desplegada.
Artefacto: 156588 bytes, SHA-256
`d4bcb41c342f31150a1da7244550b319de1ae2a71a83b401bd2f05222feffa49`.
El padre v3.9.2 y CURRENT_RELEASE.md permanecen intactos. Sin commit no se
declara la nueva candidata preservada en GitHub.

## Evidencias entregadas

- [Diagnóstico público](audit.md) y [datos](audit.json).
- [Comparación autenticada offline](authenticated-candidate-review-20261021/audit.md),
  [datos](authenticated-candidate-review-20261021/audit.json) y
  [diferencias](authenticated-candidate-review-20261021/diff.json).
- [Decisiones humanas](reconciliation-proposal/decision.json) y
  [observación del borrador 2050](reconciliation-proposal/workspace-2050-observation.md).
- [Diff de código rastreado](reconciliation-proposal/local-contract.patch).
- [Informe de candidata de skill](reconciliation-proposal/skill-release-candidate.md).
- [Solicitud técnica preparada](SOLICITUD-EVIDENCIA-SRSC.md), sin enviar.

Los scripts nuevos y sus pruebas se conservan como archivos locales; el patch
de código rastreado no incluye automáticamente esos archivos sin seguimiento.
Ver validation.md e informes de revisión para el historial de archivos y comandos.

## Validación

Regresión de contrato, auditoría, consumidores y empaquetado: 200 pruebas
aprobadas con warnings tratados como errores. Después se corrigió la comprobación
local que seguía exigiendo 56/54 y se ejecutaron 71 pruebas del conjunto de
auditoría/exportación/candidata, todas aprobadas. Estos son conjuntos distintos;
no se suman como si fueran pruebas únicas de una sola ejecución. Ruff y
git diff --check verificados. No se ejecutó integración PostgreSQL.

## Cierre y siguiente acción

La entrega parcial se puede revisar ahora. Para cerrar srsc debe recibirse y
validarse su jerarquía completa con procedencia verificable; después se añadirá
un informe nuevo, sin reescribir las capturas históricas. Si el acceso continúa
limitado, mantener UNKNOWN y la conclusión parcial.

No hay commits, PR, cambios productivos, escrituras en DSpace/PostgreSQL,
promoción de baseline o activación de sincronizaciones. La autorización de
preparación no se interpreta como autorización para publicar o adoptar.
