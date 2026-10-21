> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# dspace-cataloger — propuesta de actualización v3.5
## Knowledge & Cataloguing Governance Patch

**Base:** dspace-cataloger v3.4  
**Estrategia de merge:** aditiva; preservar contratos v3.4, Golden Set y UI Fidelity.  
**Objetivo:** incorporar hallazgos empíricos derivados de la catalogación real de recursos multilingües, artículos con vocabularios controlados incompletos y recursos con múltiples entidades lingüísticas.

---

## 1. Regla normativa CLIN para lenguas indígenas de México

### 1.1 Jerarquía normativa primaria

Para recursos relativos a lenguas indígenas nacionales de México, adoptar como autoridad primaria el **Catálogo de las Lenguas Indígenas Nacionales (CLIN), INALI**.

Jerarquía normativa:

**Familia lingüística → Agrupación lingüística → Variante lingüística**

El nivel **Rama lingüística** NO forma parte de la jerarquía normativa principal del CLIN.

### 1.2 Rama lingüística como enriquecimiento secundario

`dc.subject.linguisticBranch` debe tratarse como:

- nivel genealógico complementario;
- opcional;
- no-CLIN;
- sustentado por una autoridad lingüística secundaria explícita;
- nunca inferido por mera similitud terminológica.

Modelo interno recomendado:

`LinguisticFamily → LinguisticBranch? → LinguisticGroup → LinguisticVariant`

donde `?` indica nivel opcional de enriquecimiento.

### 1.3 Prioridad de autoridades

1. **CLIN / INALI** para Familia, Agrupación, Variante y autodenominaciones.
2. **Vocabulario local DSpace** para la serialización final del valor.
3. **Fuente lingüística secundaria acreditada** para Rama, cuando se utilice.
4. Si existe conflicto entre la fuente y el vocabulario cerrado, no aproximar: marcar `PENDIENTE` o `QA_HUMANO`.

---

## 2. Separar lengua del documento de lengua objeto de estudio

### 2.1 Lengua de registro

`dc.description.registeredLanguage` se interpreta como **lengua de redacción/registro del recurso**, no como la lista de lenguas estudiadas.

Ejemplo:

- artículo redactado en español sobre 12 lenguas indígenas:
  - `dc.description.registeredLanguage = Español`
  - `dc.language.iso6391 = spa`
  - las lenguas objeto del estudio se expresan mediante `dc.subject.linguiscgroup`.

### 2.2 Agrupación lingüística

`dc.subject.linguiscgroup` representa la **agrupación lingüística de la que trata el recurso**.

No duplicar en este campo la lengua de redacción salvo que también sea objeto explícito de estudio.

### 2.3 Uso de lengua

`dc.description.languageUsage` debe evaluarse separadamente de las dos dimensiones anteriores.

No clasificar automáticamente como bilingüe o multilingüe un recurso solo porque:
- contenga un título/resumen paralelo;
- cite ejemplos aislados;
- mencione muchas lenguas.

La clasificación debe reflejar el **uso lingüístico sustantivo del recurso**, documentado por evidencia.

---

## 3. Recursos lingüísticos multientidad

Cuando un recurso estudie múltiples lenguas:

- permitir múltiples valores en:
  - `dc.subject.linguiscgroup`
  - `dc.subject.linguisticFamily`
  - `dc.subject.linguisticBranch`
  - `dc.subject.linguisticVariant`
- no reducir el recurso a una sola lengua por conveniencia de catalogación;
- no repetir familias o ramas idénticas innecesariamente en la salida final;
- conservar internamente las relaciones entre entidades aunque DSpace serialice campos repetibles independientes.

### 3.1 Modelo interno de relaciones

```json
{
  "linguisticEntities": [
    {
      "sourceLabel": "Tsotsil",
      "group": "Tsotsil",
      "family": "Maya",
      "branch": "Tseltalano",
      "variant": null,
      "authority": {
        "group": "CLIN/local vocabulary",
        "family": "CLIN/local vocabulary",
        "branch": "secondary genealogical authority",
        "variant": null
      },
      "evidenceState": "VERIFICADO"
    }
  ]
}
```

Esto evita combinaciones cruzadas incorrectas cuando los campos DSpace se serializan como listas planas.

---

## 4. Variantes lingüísticas: política conservadora

No convertir automáticamente:

- localidades;
- regiones;
- nombres comunitarios;
- etiquetas dialectales usadas libremente por autores;

en `dc.subject.linguisticVariant`.

Solo asignar una variante cuando exista:

1. evidencia explícita en la fuente;
2. correspondencia autorizada con CLIN o autoridad aceptada;
3. coincidencia válida con el vocabulario DSpace.

Si la fuente dice, por ejemplo, “Valles centrales”, “Tumbalá”, “Zinacantán” o “Tlahuitoltepec” y no existe correspondencia exacta en el vocabulario de variantes, conservar la evidencia en notas y marcar la variante como `PENDIENTE`.

---

## 5. Normalización de exónimos, autodenominaciones y alias

Distinguir siempre:

- término usado por la fuente;
- término autorizado por CLIN;
- término autorizado por DSpace;
- autodenominación.

Ejemplos observados:

- `Purépecha` → DSpace puede autorizar `Tarasco (Purépecha)`.
- autodenominación `p'urhepecha`/`púrhepecha` debe permanecer en el campo correspondiente si está autorizada.
- `Ngigua` no debe transformarse silenciosamente a `Chocholteco`; la equivalencia requiere validación de autoridad y aprobación humana.

Registrar estas reconciliaciones como decisiones explícitas de QA.

---

## 6. Vocabularios cerrados: no sustitución por proximidad

Regla obligatoria:

> Si un valor fuente no existe en un vocabulario cerrado, no sustituirlo por la opción semánticamente “más cercana”.

Ejemplo:

- fuente: CC BY 3.0
- vocabulario: solo CC BY 4.0
- resultado: `PENDIENTE / VOCABULARY_GAP`
- prohibido: sustituir CC BY 3.0 por CC BY 4.0.

Crear/usar un registro de brechas:

```json
{
  "type": "VOCABULARY_GAP",
  "metadataField": "dc.rights.license",
  "sourceValue": "CC BY 3.0",
  "authorizedMatch": null,
  "action": "HUMAN_REVIEW"
}
```

---

## 7. Abstract: fuente antes que generación

Cuando exista resumen/abstract autoral accesible:

1. preferir el texto original;
2. marcar como `EXTRAÍDO`;
3. no sustituirlo por una paráfrasis generada;
4. si se produce una síntesis catalográfica adicional, mantenerla separada y marcarla `GENERADO`.

`GENERADO` nunca debe confundirse con el valor autoral de `dc.description.abstract`.

---

## 8. Palabras clave vs. tópicos inferidos

Mantener tres capas distintas:

1. **Palabras clave autorales** → `EXTRAÍDO`.
2. **Tópicos controlados DSpace** → `NORMALIZADO/VERIFICADO`.
3. **Términos inferidos por el asistente** → `INFERIDO` o `GENERADO`, nunca presentados como keywords del autor.

No inventar “palabras clave” cuando la publicación no las proporciona.

---

## 9. Cobertura geográfica: objeto de estudio ≠ procedencia editorial

Distinguir:

- `dc.coverage.countryFound`: procedencia/localización del ejemplar o recurso según política local;
- `dc.coverage.country`, `state`, `region`, `community`: cobertura espacial del contenido.

No inferir `countryFound` automáticamente desde:
- sede de la editorial;
- dominio web;
- afiliación del autor.

Los lugares estudiados sí pueden alimentar cobertura cuando estén sustentados por la fuente.

---

## 10. Fechas editoriales

Distinguir:

- fecha del fascículo;
- fecha de publicación online-first;
- fecha de recepción;
- fecha de aceptación;
- fecha de revisión.

Para `dc.date.issued`, usar la fecha de publicación correspondiente a la manifestación catalogada según la política de la colección. Conservar fechas editoriales adicionales solo si existe binding apropiado o en notas.

---

## 11. Títulos y subtítulos

No dividir automáticamente un título por la presencia de dos puntos.

Asignar `dc.title.subtitle` solo cuando:
- la fuente editorial distingue explícitamente título/subtítulo; o
- la política catalográfica local lo exige inequívocamente.

---

## 12. QA lingüístico obligatorio

### CAT-LING-001 — CLIN hierarchy
Familia/Agrupación/Variante deben respetar la jerarquía CLIN cuando el recurso trate lenguas indígenas de México.

### CAT-LING-002 — Branch provenance
Toda Rama lingüística debe indicar autoridad secundaria o quedar pendiente.

### CAT-LING-003 — Document vs subject language
No confundir lengua de redacción con agrupación lingüística estudiada.

### CAT-LING-004 — Variant authority
No convertir topónimos o etiquetas locales en variantes CLIN sin reconciliación autorizada.

### CAT-LING-005 — Multi-entity integrity
En recursos multilingües, preservar internamente la relación grupo–familia–rama–variante.

### CAT-VOC-004 — No nearest substitute
Prohibida la sustitución aproximada en vocabularios cerrados.

### CAT-ABS-002 — Extracted abstract precedence
Si existe abstract autoral, debe prevalecer como valor EXTRAÍDO.

### CAT-SUBJ-002 — Author keywords provenance
Los términos inferidos no pueden presentarse como palabras clave del autor.

### CAT-GEO-001 — Coverage/provenance separation
No derivar countryFound de la sede editorial sin política explícita.

---

## 13. Nuevos fixtures para Golden Set

Añadir casos de regresión:

- **GR11** — Artículo con lengua de redacción ≠ lenguas estudiadas.
- **GR12** — Recurso con 10+ agrupaciones lingüísticas y 5 familias.
- **GR13** — Rama genealógica no perteneciente al CLIN.
- **GR14** — Variante mencionada por localidad pero sin coincidencia CLIN.
- **GR15** — Alias/autodenominación (`Purépecha` / `Tarasco (Purépecha)`).
- **GR16** — Vocabulario cerrado sin versión exacta de licencia (CC BY 3.0 vs 4.0).
- **GR17** — Abstract autoral disponible + síntesis generada separada.
- **GR18** — Palabras clave autorales ausentes pero tópicos inferibles.
- **GR19** — Fecha online-first diferente de fecha del fascículo.
- **GR20** — Recurso con título con dos puntos que no implica `dc.title.subtitle`.

---

## 14. Fuentes de autoridad recomendadas

### Primarias
- Instituto Nacional de Lenguas Indígenas (INALI), **Catálogo de las Lenguas Indígenas Nacionales: Variantes lingüísticas de México con sus autodenominaciones y referencias geoestadísticas**.
- Diario Oficial de la Federación, publicación del CLIN (14 de enero de 2008).
- Atlas de las Lenguas Indígenas de México, INALI.

### Locales
- `dspace_cataloguing_profile_v3.json`
- `dspace_form_contract_v1`
- vocabularios DSpace de la instancia.

### Secundarias
- Bibliografía lingüística especializada para subgrupos o ramas genealógicas no modeladas por CLIN.

---

## 15. Compatibilidad

Esta actualización NO modifica:

- `dc.subject.linguiscgroup` literal;
- UI Fidelity Mode;
- `bindingId`;
- `assistantLabel`;
- estados de evidencia existentes;
- `autoWrite=false`;
- `humanApprovalRequired=true`;
- política de no aproximación en vocabularios cerrados;
- Golden Set v3.3/v3.4 existente.

Es una extensión semántica y de QA.
