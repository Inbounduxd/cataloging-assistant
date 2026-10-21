# Preservación local autorizada — 2026-10-21

El usuario autorizó expresamente crear un commit local con la auditoría, el
contrato y las candidatas, manteniendo v3.9.2 como vigente y sin push, PR o
despliegue. Esta autorización levanta únicamente la restricción anterior de
no crear commits para esa entrega.

Se prepara en la copia WSL de Inbounduxd/cataloging-assistant, rama
`codex/snibli-migration-audit`. La identidad de autor se obtiene de la
configuración Git existente del usuario en Windows y se aplica solo al comando
de commit; no se crea una identidad ni se modifica la configuración global.

Incluye código de auditoría/exportación/construcción, contrato local aprobado,
pruebas, ADR y documentación, evidencias raw y normalizadas, decisiones, informes
y las candidatas completas rc.1 y rc.2. Los informes anteriores describen cada
fase y se conservan como historial; sus declaraciones de ausencia de commit
corresponden al momento en que fueron generados.

La última regresión ampliada obtuvo 224 pruebas aprobadas; tras el último ajuste
documental de rc.2 se repitieron sus seis pruebas específicas, también aprobadas.
La revisión final del paquete confirmó los 225 miembros, reproducción exacta,
concordancia con el runtime local y checksums. Sin cambios posteriores de código,
no se repite la suite solo por crear el commit.

Las evidencias y fuentes incluidas en los paquetes conservan sus bytes originales,
incluidos CRLF y espacios históricos. .gitattributes desactiva la normalización
de texto y los avisos de whitespace únicamente en esas rutas para proteger sus
checksums entre Windows y WSL. El código de aplicación no queda exceptuado.

v3.9.2, CURRENT_RELEASE.md y el README del registro se mantienen intactos.
Las candidatas no se adoptan o instalan. Un commit local sin push no equivale a
preservación en GitHub ni autoriza publicación, DSpace writes, promoción de
baseline o sincronizaciones. No se crean PR ni se modifica producción.
