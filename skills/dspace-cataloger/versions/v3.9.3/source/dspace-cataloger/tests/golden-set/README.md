# Golden Set Regression Suite

Estos fixtures codifican **reglas semánticas esperadas**, no copias de las
fuentes completas.

Objetivo:

- detectar regresiones de política;
- comprobar que una nueva versión no vuelva a cometer errores ya resueltos;
- separar pruebas de adquisición, mapeo, vocabularios y QA.

Estados:

`PILOT_ACCEPTED` significa que el tratamiento del caso fue aceptado durante el
piloto. No equivale automáticamente a política institucional definitiva.

Una implementación del MVP debe poder ejecutar estos fixtures como pruebas de
regresión de reglas y producir PASS/FAIL por expectativa.


## Extensión v3.5

GR11–GR20 codifican aprendizajes surgidos de catalogación real: separación de
lengua del documento/lengua objeto, jerarquía CLIN, ramas opcionales, recursos
multientidad, variantes con autoridad, alias, gaps de vocabulario, abstract
autoral, keywords, fechas editoriales y tratamiento de subtítulos.

## v3.9.2 re-derived additive fixtures
- GR21 and GR22 carry forward the documented v3.9.1 semantic patch.
- GR23: ORCID is evidence-only; its fragments cannot be ISSN candidates.
