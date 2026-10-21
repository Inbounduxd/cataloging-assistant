# Revisión de la captura autenticada SNIBLI — 2026-10-20

**El login funcionó. Hay drift observable respecto del contrato preservado
v3.9.2.** La captura parcial contiene evidencia suficiente para comparar la
configuración de formularios y vocabularios, aunque no la pertenencia activa de
la colección ni la jerarquía completa de `srsc`.

## Cobertura y motivo de los flags

Se hicieron 64 solicitudes con el cliente existente: un POST de login y el resto
GET. Se capturaron 18 schemas, 293 campos, 12 definiciones, 46 secciones,
15 formularios, 455 colecciones visibles y páginas de 22 vocabularios.

`capture_complete: false` procede del HTTP 422 de `srsc/entries`. El fallback
permitido a nodos superiores respondió HTTP 200 y se conservó, sin declararlo árbol
completo. `snapshot_complete: false` procede de no haber seleccionado colección;
faltan la definición activa y sus secciones enlazadas. No hubo fallo de contraseña
ni hace falta repetir el login para revisar esta evidencia.

## Formularios configurados: FAIL / SCHEMA_DRIFT

- Referencia: 56 bindings, 54 claves únicas.
- Observación: 57 bindings, 55 claves únicas.
- Se conservan los 56 bindings originales; no se observan eliminaciones.
- Sus etiquetas, required, repeatable, tipo de control y asociación/cierre de
  vocabulario coinciden. Hay 29 cambios de posición tras la inserción.
- Binding adicional en `traditionalpageone`, posición `[0,13,0,0]`:
  `dc.type.genre`, etiqueta **¿Es un texto comparativo?**, dropdown, opcional,
  no repetible y cerrado, asociado a `genrePairs`.
- El campo está registrado como ID 293, element `type`, qualifier `genre`,
  scopeNote literal `Genero del recurso`. No es un binding sin registro.
- `genrePairs` contiene `Sí`, `No`, `Incluye Datos de Diferentes Lenguas`.

La asociación entre `dc.type.genre`, esa pregunta y esos valores requiere revisión
humana semántica. No se reinterpretó ni normalizó automáticamente.

## Vocabularios: FAIL / VOCABULARY_DRIFT

De los 21 vocabularios de referencia: 19 coinciden literalmente, uno difiere y
uno queda UNKNOWN. En `common_types` se conservan los 23 valores de referencia
y aparecen tres valores más, para un total de 26:

- `Códice`
- `Reseña`
- `Documento Colonial`

`srsc` queda UNKNOWN por cobertura jerárquica incompleta. El nuevo `genrePairs`
se documenta como asociación del binding adicional; no se inventó una referencia
histórica para sus valores.

## Corrección del diagnóstico y procedencia

El reporte original clasificó los formularios UNKNOWN porque el comparador
utilizaba las claves esperadas como si fueran el registro observado. Eso generó
una advertencia errónea para `dc.type.genre`, que sí está registrado.
Se corrigió la herramienta para consultar el registro capturado y para mantener
como FAIL una diferencia estructural observable aunque falte otra superficie.
Se añadieron dos pruebas que reproducen ese caso, sin cambiar expectativas de
pruebas existentes. La suite seleccionada termina en 87 pruebas aprobadas.

`export.json`, `audit.json`, `audit.md`, `diff.json` y los cuerpos `.response`
originales no se sobrescribieron. La revisión corregida está en
`review.audit.json` y `review.diff.json`; incluye hashes de los archivos fuente y
usa VERTICAL-022 para el diff de bindings configurados. Este análisis fue offline:
no hizo login ni nuevas peticiones, y no necesitó acceder a contraseñas o tokens.

La referencia es el artefacto preservado v3.9.2, no un snapshot ACTIVE desplegado;
esta evidencia no determina cuándo se introdujeron los cambios ni si fueron parte
de la migración. No se declara equivalencia completa.

## Pendiente

El operador identificó la colección **Lingüística Maayat'aan, Maya**, UUID
`3ce3afb3-94ed-4f60-bfda-0a1242c4d689`, Handle `123456789/393`. Su identidad
coincide con el inventario guardado. La consulta pública de su definición activa
devolvió HTTP 401; queda pendiente capturar esa pertenencia con una nueva sesión
interactiva. La sesión anterior no se guardó y la contraseña no está disponible
para el asistente. No se deduce equivalencia con la antigua piloto. El UUID y Handle históricos tampoco aparecen en las 455
colecciones visibles con esta sesión; no se eligió un reemplazo por nombre.
Revisar y aprobar expresamente el campo adicional y las nuevas opciones antes
de actualizar cualquier contrato, skill o configuración. No se hizo ningún cambio
de contenido, PostgreSQL, producción o skill, ni commits o PR.


Comando para la captura con la colección ya indicada, en PowerShell:

```powershell
wsl -e bash -lc 'cd /home/keilyn/cat && /home/keilyn/snibli-audit-venv/bin/python /home/keilyn/snibli-migration-audit/scripts/export_snibli_configuration.py --collection-uuid 3ce3afb3-94ed-4f60-bfda-0a1242c4d689'
```

Solicita otra vez la contraseña oculta porque no se conservaron credenciales ni
sesión. Se genera otra carpeta, sin mezclar páginas con la captura anterior.
Un resultado parcial puede persistir por `srsc` y por HTTP 204 de secciones,
si lo devuelve la instancia. Esas limitaciones no deben convertirse en PASS.
