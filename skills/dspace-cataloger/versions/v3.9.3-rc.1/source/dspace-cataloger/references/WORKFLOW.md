> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Workflow v3.5

1. Ingreso de una o más fuentes.
2. Identificación de origen y tipo de entrada.
3. Si falta URL o está rota: Bibliographic Discovery + Identity Match.
3. Preservación de archivo/fila/URL original.
4. Hash/MIME/metadata técnica cuando aplique.
5. Adaptación a Evidence Corpus.
6. Si existe URL: landing + full-text discovery.
7. Si existe PDF/EPUB: extracción directa.
8. Si existe DSpace Item: metadata + bitstreams.
9. Fusión de evidencias.
10. Segmentación: front matter, cuerpo, conclusiones, referencias.
11. Extracción catalográfica.
12. Mapeo al formulario real DSpace.
13. Resolución de binding/UI mediante `assets/dspace-form-contract-v1.json` cuando aplique.
14. Validación contra vocabularios cerrados por binding.
15. Autoridades/crosswalks externos cuando proceda. Para lenguas indígenas de México: CLIN/INALI para Familia–Agrupación–Variante; Rama solo con autoridad secundaria.
16. Preservación de relaciones lingüísticas multientidad antes de serializar campos repetibles.
17. QA.
18. Mesa del catalogador.
19. Golden Set + pruebas de formContract / aprendizaje de correcciones.
20. Staging/escritura solo con aprobación explícita.
21. Auditoría.

## Interfaz arquitectónica

`Input Adapters → Evidence Corpus → Cataloguing Core → DSpace Adapter`

El Cataloguing Core no debe depender de HTTP, Google Sheets ni formato de
archivo específico.


## v3.3 — Cierre por campo

Antes de cerrar un registro:

- asignar `mappingStatus`;
- registrar gaps;
- registrar discrepancias;
- aplicar PolicyDecision cuando corresponda;
- capturar `humanDecision` por campo;
- conservar `finalValue`.

El Golden Set debe ejecutarse como regresión semántica antes de publicar una
nueva versión de la skill.
