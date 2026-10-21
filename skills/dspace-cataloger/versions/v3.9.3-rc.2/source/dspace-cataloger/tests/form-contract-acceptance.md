# Form Contract Acceptance v3.4

Estas pruebas son aditivas al Golden Set v3.3 y no sustituyen sus fixtures.

1. `Titulo` se conserva literalmente en UI Fidelity Mode.
2. `Titulo` aparece antes que `Autor`; `Autor` antes que `Fecha de Creacion`.
3. DOI e ISSN conservan `uiLabel=Identificador`, pero se desambiguan en presentación.
4. La clave emitida es exactamente `dc.subject.linguiscgroup`.
5. `Soporte` y `Tipo de extensión` no se colapsan aunque compartan `dc.format.medium`.
6. `Palabras Clave` y `Tópicos (disciplinas, temas específicos)` conservan bindings separados.
7. La validación de vocabulario de un binding cerrado exige coincidencia literal.
8. Un resumen evaluativo redactado por el asistente usa `evidenceStatus=GENERADO`.
9. Un resumen `GENERADO` no se mapea automáticamente a `dc.description.abstract`.
10. `Fecha de Creacion` permanece ligada a `dc.date.issued`.
11. El conflicto `dc.source` formulario↔scope note continúa como `CAT-FORM-003`.
12. Salidas estructuradas con claves compartidas incluyen `bindingId`.
13. Ninguna escritura se considera aprobada sin decisión humana explícita.
14. Los 10 fixtures del Golden Set v3.3 siguen siendo regresión obligatoria.
