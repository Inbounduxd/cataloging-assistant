# Borrador de solicitud técnica — no enviado

**Ya no es necesario enviar esta solicitud para conocer el árbol actual:**
posteriormente se recuperó por enlaces REST/HAL. Ver
[evidencia del recorrido](srsc-hal-tree-20261021/summary.md). Se conserva este
borrador como historial; solo sería pertinente pedir el XML o una referencia
histórica si se exige esa comparación adicional.

Asunto: Evidencia de lectura del vocabulario srsc para auditoría de SNIBLI

Para completar la auditoría de compatibilidad de SNIBLI solicitamos una
exportación de lectura del vocabulario controlado **srsc** en la instancia
cuya API verificada es `https://www.iifl.unam.mx/server/api`.

La consulta autenticada a entries devolvió HTTP 422 y el fallback de top solo
permitió observar nodos superiores. Por eso no podemos verificar la jerarquía
completa. No se solicita modificar el repositorio ni habilitar permisos nuevos.

Necesitamos, preferentemente:

1. La definición completa de srsc en su formato nativo disponible (por ejemplo,
   XML/JSON de configuración), incluyendo identificadores, valores, etiquetas,
   relaciones padre-hijo y reglas de selección que existan.
2. Si la evidencia se obtiene mediante REST, cuerpos originales HAL+JSON de
   todas las páginas/ramas y sus URLs de origen sin secretos, con HTTP status,
   paginación, conteos y errores, distinguiendo nodos raíz y descendientes.
3. Fecha de extracción con zona horaria, identificación de instancia y versión
   DSpace, método empleado y alcance de la exportación. Si es posible, checksum
   SHA-256 del archivo entregado.
4. Confirmación del vínculo entre ese vocabulario y el control Palabras Clave
   (`dc.subject`) de la definición traditional en la colección
   `3ce3afb3-94ed-4f60-bfda-0a1242c4d689`, Handle `123456789/393`.

Si la interfaz o API solo expone una parte del árbol, agradeceremos que se
indique explícitamente el límite. Una lista de nodos raíz o un conjunto de
resultados de búsqueda no se considerará exportación completa por sí solo.

No incluir contraseñas, cookies, cabeceras Authorization, tokens o datos de
cuentas. No necesitamos acceso SSH ni conexión a PostgreSQL. Si se requiere
una extracción del servidor, debe realizarla el responsable autorizado y
compartir únicamente la configuración necesaria para esta comprobación.

Hasta recibir esta evidencia, srsc y la equivalencia completa de migración
permanecerán UNKNOWN. Gracias.

---

## Criterios locales de recepción

- Conservar el archivo recibido íntegro, su origen y checksum.
- Verificar cobertura de páginas y ramas, identificadores y relaciones sin
  convertir valores desconocidos en vacíos.
- Comparar literalmente contra la referencia disponible; documentar faltantes,
  duplicados y relaciones discrepantes sin renombrar términos automáticamente.
- Incorporar un informe nuevo con el alcance probado y mantener los originales.
- No modificar DSpace ni promover automáticamente el baseline o la skill.
