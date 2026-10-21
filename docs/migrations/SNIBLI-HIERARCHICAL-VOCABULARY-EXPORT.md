# Exportar vocabularios jerárquicos SNIBLI por HAL

La operación entries sin filtro puede responder 422 en un vocabulario no
scrollable. Eso no demuestra que su jerarquía sea inaccesible. Usar top y seguir
los enlaces children de sus nodos, con la API institucional explícita.

## Ejecución pública en PowerShell

Desde la raíz de la copia local, en una sola línea:

```powershell
python scripts/export_snibli_configuration.py --public-hierarchy srsc --max-seconds 600 --max-requests 500 --output "reports/snibli-migration/srsc-tree-new"
```

La carpeta debe ser nueva. Este modo no solicita credenciales ni inicia sesión;
solo consulta el árbol indicado. La ejecución realizada el 2026-10-21 ya recuperó
665 nodos, 653 relaciones y 12 raíces en 126 GET. No hace falta repetirla para
revisar la evidencia guardada en reports/snibli-migration/srsc-hal-tree-20261021/.

Si un despliegue requiere autenticación para la misma superficie, el modo
`--hierarchy-only srsc` reutiliza el cliente de sesión ya autorizado con entrada
oculta de contraseña. No combinar los modos de jerarquía con collection-uuid o
baseline: no pretenden generar un snapshot global. El exportador general también
recorre los vocabularios declarados jerárquicos en lugar de tratar top como árbol.

## Límites y evidencia

Se conserva cada cuerpo raw, URL, fecha, HTTP status y SHA-256. El archivo
export.json incluye vocabulary_evidence.srsc.tree con nodos, relaciones, errores y
completitud. Rechaza enlaces fuera del origen HTTPS institucional y rutas ajenas;
el transporte sigue bloqueando redirecciones y operaciones de escritura.

Límites existentes: 4 MiB por respuesta, timeout por operación hasta 30 s, total
hasta 600 s, solicitudes hasta 500, páginas hasta 100 por rama y size hasta 100.
El recorrido añade techo de 10000 nodos y profundidad 32. Errores, ciclos,
duplicados, ramas pendientes o límites agotados producen UNKNOWN, conservando
los datos parciales. No se convierten ramas desconocidas en listas vacías válidas.

capture_complete expresa solo el alcance solicitado. snapshot_complete sigue
false en un árbol aislado porque no hay evidencia global de contrato. Un árbol
completo expuesto no equivale a un XML byte-idéntico del servidor ni prueba su
igualdad con una configuración histórica ausente. OAI-PMH puede complementar
los valores usados en registros, pero no sustituye esta definición de vocabulario.

Referencias técnicas:
- https://github.com/DSpace/RestContract/blob/main/vocabularies.md
- https://github.com/DSpace/RestContract/blob/main/vocabularyEntryDetails.md
- https://www.openarchives.org/OAI/openarchivesprotocol.html
