# Revisión guiada de SNIBLI — 2026-10-21

Estado: PENDIENTE. Esta guía no constituye aprobación institucional ni evidencia
de que las superficies pendientes se hayan observado.

## Acceso

Usar la sesión del navegador en https://www.iifl.unam.mx/SNIBLI/home.
Introducir las credenciales únicamente en el sitio institucional. No incluir
contraseñas, tokens o cookies en capturas, documentos o respuestas del chat.

Colección objetivo: **Lingüística Maayat'aan, Maya**,
https://www.iifl.unam.mx/SNIBLI/collections/3ce3afb3-94ed-4f60-bfda-0a1242c4d689,
Handle `123456789/393`. La API autenticada ya confirmó la definición `traditional`.

## Comprobación sin escrituras

1. Verificar la identidad de la colección en su página pública.
2. Buscar una vista existente de configuración o previsualización que permita
   consultar las secciones de `traditional` sin guardar cambios. Registrar los
   títulos, identificadores si son visibles y su orden, junto con URL y fecha.
   No suponer que una pantalla de edición de metadatos de un ítem equivale al
   formulario de depósito activo.
3. Si la única vía ofrecida es iniciar un depósito, detener esa comprobación:
   puede crear un workspace/borrador mediante POST. No crear ni eliminar ítems,
   borradores o workflows como parte de esta auditoría.
4. Si existe un selector o explorador de `srsc` accesible sin crear registros,
   expandir sus ramas y registrar etiquetas y relaciones padre-hijo. Indicar si
   quedan ramas cerradas, paginación o carga pendiente. Ver solo los nodos raíz
   no demuestra que se haya recuperado el árbol completo.
5. Registrar cada hallazgo con su fuente. Si la interfaz no expone una vista
   segura o completa, conservar UNKNOWN y solicitar evidencia de configuración
   al responsable institucional; no convertir ausencia de observación en FAIL.

## Decisiones institucionales

| ID | Pregunta | Estado |
|---|---|---|
| C1 | ¿Es intencional que `dc.type.genre` tenga la etiqueta «¿Es un texto comparativo?» y los valores Sí / No / Incluye Datos de Diferentes Lenguas? ¿Cuál es su definición institucional? | PENDIENTE |
| C2 | ¿Se acepta el orden observado tras la inserción, conservando las identidades de los 56 controles originales? | PENDIENTE |
| C3 | ¿Se aceptan literalmente Códice, Reseña y Documento Colonial en `common_types`? | PENDIENTE |

Registrar nombre y función de quien decide, fecha, respuesta y fundamento. No
rellenar `decision.json` como aprobado solo por continuar el trabajo técnico.

## Registro de evidencia pendiente

| Superficie | Evidencia disponible | Evidencia adicional necesaria | Resultado actual |
|---|---|---|---|
| Secciones activas | Definición `traditional`; endpoint de secciones HTTP 204 | Membresía y orden completos mediante vista de configuración o evidencia independiente identificada | UNKNOWN |
| Jerarquía `srsc` | Consulta entries HTTP 422; fallback de nodos superiores | Árbol completo y relaciones, con alcance y procedencia verificables | UNKNOWN |
| Semántica del campo adicional | Configuración HAL capturada | Confirmación institucional C1 | PENDIENTE |

La coincidencia offline de 57 controles, 55 claves y 17 vocabularios planos con
la candidata ya está documentada en `../candidate-validation-2026-10-21/summary.md`.
Esta revisión no sustituye esa evidencia ni elimina los FAIL respecto de v3.9.2.
No promover baseline, modificar la skill o activar escrituras/sincronizaciones.
