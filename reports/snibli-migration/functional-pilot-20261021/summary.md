# Piloto funcional de rc.2 — 2026-10-21

**Resultado técnico: PASS; revisión humana: PENDING.**
Se aplicó la skill rc.2 en modo standalone de propuesta, sin modificar DSpace.
Esta es una evaluación focalizada de un registro real, no una recatalogación
completa o una nueva adjudicación independiente del Golden Set.

## Caso y fuentes

Registro: [Handle 123456789/733](https://www.iifl.unam.mx/SNIBLI/items/ba2d355b-a2de-4c29-8fbf-0c9c335c6452),
una reseña de «Argumentos cuantitativos y cualitativos en sociolingüística».

Fuente editorial primaria:
https://ela.enallt.unam.mx/index.php/ela/article/view/632.
Su metadato estructurado `DC.Type.articleType` contiene literalmente `Reseñas`.
DSpace conserva actualmente `dc.type = Article`.

La pertenencia a la colección piloto Maya quedó comprobada mediante el enlace
HAL mappedCollections (7 colecciones mapeadas, una página completa). No es la
colección propietaria: owningCollection es Lingüística p'uhrépecha,
UUID `2b1a6e73-92d4-45e4-970d-6186d8c895fe`, Handle `123456789/137`.
Esto no se interpreta como error de pertenencia ni como evidencia de la lengua
de redacción o del objeto primario del documento.

Se guardaron cuatro respuestas originales: ítem, owningCollection,
mappedCollections y página editorial. Solo GET públicos, sin credenciales.
Los hashes y tamaños están en [source-manifest.json](source-manifest.json).
El visor web no pudo recuperar la página editorial; la solicitud local acotada
sí respondió HTTP 200 y permitió conservar el HTML original.

## Propuesta para revisión

| Control | Actual | Propuesta | Fundamento y límite |
|---|---|---|---|
| Tipo documental, dc.type | Article | Reseña | Naturaleza explícita en metadato editorial y valor literal aprobado en common_types; no se confunde revista con artículo |
| ¿Es un texto comparativo?, dc.type.genre | Ausente | Pendiente, sin valor sugerido | La ficha no prueba una de las tres opciones; no se elige No por defecto ni se infiere por contar lenguas |
| Lengua de registro | Español | Conservar Español | Extraído del registro; no es una verificación independiente del texto completo ni del idioma de la interfaz editorial |
| Agrupación lingüística | Ocho valores registrados | Sin adiciones o eliminaciones sugeridas | No se valida pertinencia individual con el texto completo ni se propaga la lengua de registro |
| Palabras clave, dc.subject/srsc | Valores de clave compartida | Pendiente | No se deduce el widget original desde el metadato almacenado ni se traduce a categorías cercanas |
| Tópicos, dc.subject/topicsPairs | Incluye Sociolingüística | Sociolingüística como candidato literal | Coincide con topicsPairs; no sustituye otros valores del registro y requiere revisión antes de reubicar/copiar |
| Extensión | páginas 207-213 | Conservar | Las 802 páginas del título son del libro reseñado, no de la reseña |

Todos los controles conservan humanDecision=PENDING, finalValue=null y
requiresHumanApproval=true. El campo comparativo no se completa y no se escribe
ninguna corrección. La discrepancia documental se registra en QA como una
corrección del registro pendiente, no como un fallo de la skill al detectarla.

Los vocabularios usados en este piloto son los fijados dentro del paquete rc.2.
No se afirma que se hayan revalidado todas sus entradas en vivo para una futura
operación de copia. El árbol actual srsc existe en la candidata, pero no convierte
todos los términos de dc.subject en valores de ese vocabulario.

## Validación técnica

El paquete usado tiene SHA-256
`c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae`.
Se verificó su identidad y se validó [proposal.json](proposal.json) contra
catalog-draft.schema.json, leído directamente de ese ZIP.

[validation.json](validation.json) registra nueve controles aprobados: integridad,
esquema, tipo literal permitido, abstención comparativa, separación lingüística,
bindings distintos para clave compartida, extensión del recurso correcto,
decisiones humanas pendientes y propuesta sin escrituras.

Reproducción offline desde WSL, cwd /home/keilyn/cat:

```bash
/home/keilyn/snibli-audit-venv/bin/python /home/keilyn/snibli-migration-audit/reports/snibli-migration/functional-pilot-20261021/prepare_pilot.py
```

Ruff y validación del esquema: PASS. No cambió código de aplicación ni paquete;
no se repitió la regresión de 224 pruebas para generar este informe.

## Estado de entrega

El piloto técnico está terminado y la propuesta real queda disponible para
revisión humana. No se preparó o promovió una versión estable a partir de una
aceptación humana inventada. No se creó commit, PR, despliegue o escritura en
DSpace durante esta fase; los archivos quedan locales en la rama
codex/snibli-functional-pilot. v3.9.2 continúa vigente y rc.2 permanece intacta.
