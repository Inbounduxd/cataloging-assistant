> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# UI Fidelity & Form Binding Contract v3.4

## Propósito

Este documento añade una capa de fidelidad de interfaz al perfil catalográfico v3.3
sin sustituir ninguna regla semántica, de evidencia, vocabulario o QA ya aceptada.

La identidad operativa de un control de formulario es:

`bindingId + uiLabel + metadataField`

- `bindingId`: identifica el control concreto dentro de un formulario.
- `uiLabel`: conserva literalmente el rótulo configurado en DSpace.
- `assistantLabel`: rótulo auxiliar que solo puede desambiguar la presentación humana.
- `metadataField`: clave canónica para DSpace/API (`dc.*`, `dcterms.*`, etc.).

Consulta `assets/dspace-form-contract-v1.json`.

## Autoridad de presentación

Cuando el objetivo sea revisión humana, copia manual o contraste con la interfaz DSpace:

1. usar literalmente `uiLabel` como rótulo base;
2. mostrar inmediatamente el `metadataField`;
3. conservar el orden de `formOrder → row → fieldIndex → metadataIndex`;
4. no traducir ni corregir silenciosamente etiquetas conocidas;
5. no colapsar dos controles solo porque comparten `metadataField`.

Ejemplos observados:

- `Titulo` → `dc.title`
- `Fecha de Creacion` → `dc.date.issued`
- `Lengua registrada (Agrupación lingüística)` → `dc.subject.linguiscgroup`

La fidelidad de UI **no cambia** la semántica del campo. Por ejemplo, el rótulo
`Fecha de Creacion` permanece ligado a `dc.date.issued`; no se remapea a
`dc.date.created` salvo cambio explícito del perfil institucional.

## Etiquetas repetidas

La UI reutiliza `Identificador` para múltiples claves. El contrato conserva:

`uiLabel = Identificador`

pero la salida humana puede usar `assistantLabel` para desambiguar:

- `Identificador — ISSN` (`dc.identifier.issn`)
- `Identificador — DOI` (`dc.identifier.doi`)
- `Identificador — URI` (`dc.identifier.uri`)

El sufijo es solo de presentación; nunca cambia la clave técnica.

## Claves compartidas por controles distintos

### `dc.format.medium`

- `Soporte` → `mediumPairs`
- `Tipo de extensión` → `extentTypePairs`

Ambos bindings deben conservarse por separado. Sigue aplicando `CAT-FORM-002`.

### `dc.subject`

- `Palabras Clave` → `srsc`, abierto (`closed: false`)
- `Tópicos (disciplinas, temas específicos)` → `topicsPairs`, cerrado

No fusionar ambos controles antes de la revisión humana. La validación de
vocabulario depende del binding, no solo de la clave `dc.subject`.

## UI Fidelity Mode

Cuando se invoque catalogación contra esta instancia con `formContract` conocido,
la presentación humana usa por defecto **UI Fidelity Mode**:

- incluye campos con valor sustentado;
- incluye campos obligatorios aunque estén pendientes;
- incluye campos que requieren decisión explícita;
- omite campos opcionales claramente no aplicables en la vista compacta;
- conserva el orden relativo exacto de los bindings incluidos;
- muestra `assistantLabel` cuando sea necesaria desambiguación, seguido de
  `metadataField`.

Para auditoría puede solicitarse **Formulario completo**, que renderiza todos los
bindings en orden.

## Estado `GENERADO`

`GENERADO` identifica contenido redactado por el asistente y no presente en la
fuente primaria ni verificado externamente.

Ejemplos:

- resumen evaluativo;
- nota explicativa generada;
- propuesta sintética de descripción.

Reglas:

1. `GENERADO` no equivale a `EXTRAÍDO` ni `VERIFICADO`.
2. Un contenido `GENERADO` no puede presentarse como abstract original.
3. `references/ABSTRACT_POLICY.md` sigue siendo normativa: si no existe abstract
   original, `dc.description.abstract` permanece vacío salvo PolicyDecision
   institucional explícita que cambie esa política.
4. Si un contenido generado se propone para un campo no autorizado por la política,
   usar `mappingStatus = POLICY_REVIEW` y exigir aprobación humana.

## Salida estructurada

Cuando haya bindings compartidos no serializar el formulario solo como:

`{metadataField: value}`

Usar objetos por binding, por ejemplo:

```json
{
  "bindingId": "traditionalpageone:r18:f0:m0",
  "uiLabel": "Lengua registrada (Agrupación lingüística)",
  "assistantLabel": "Lengua registrada (Agrupación lingüística)",
  "metadataField": "dc.subject.linguiscgroup",
  "suggestedValue": "...",
  "evidenceStatus": "EXTRAÍDO"
}
```

La transformación final al payload DSpace ocurre únicamente después de aprobación
humana y conforme al adapter de escritura de la versión concreta.
