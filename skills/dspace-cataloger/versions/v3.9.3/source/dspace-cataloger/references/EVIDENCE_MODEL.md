> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Evidence Model v3.1

## Jerarquía de fuerza de evidencia

### PRIMARY

Metadato explícito en la versión publicada o en XML/JATS estructurado:
título, autor, DOI, abstract, keyword, fecha, páginas, licencia.

### STRONG

Información inequívoca en introducción, métodos, resultados o conclusiones que
describe directamente el objeto del recurso.

### SUPPORTING

Información repetida o contextual en el cuerpo que refuerza una asignación,
pero no basta por sí sola para una decisión delicada.

### WEAK

Mención incidental, nota lateral o contexto no central.

### EXCLUDE_FOR_SUBJECT

Bibliografía/referencias y menciones que no describen el contenido del recurso.

## Fusión de fuentes

Cuando landing, XML y PDF difieran:

1. no reconciliar silenciosamente;
2. conservar las variantes;
3. registrar la discrepancia;
4. priorizar la versión publicada para presentación bibliográfica, salvo que
   una política institucional indique lo contrario;
5. solicitar revisión humana en discrepancias sustantivas.

## Resumen

Solo poblar `dc.description.abstract` si existe un resumen/abstract en la fuente
o en una representación oficial.

Un resumen generado por el modelo debe llamarse `resumen analítico generado`,
mantenerse fuera de `dc.description.abstract` y no confundirse con el original.
