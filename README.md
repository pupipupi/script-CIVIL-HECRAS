# Procesar TXT

Sirve para transformar un archivo de exportacion HECRAS generado por CIVIL. Permite corregir la orientación del flujo y dibujar el perfil longitudinal invertido simplemente cambiando el nombre de las "STATION" de los "River Station".

Cargar el archivo de entrada *.GEO exportado desde CIVIL a HECRAS pero cambiar el nombre y extensión a "input.txt"
Si ya existe un archivo "input.txt" se debe eliminar previamente.

Ir a "Actions" y correr "Procesar TXT".

Luego de que corra el script buscar en el resultado del proceso "Subir resultado" y luego la línea "Artifacts download URL: ...".
Pinchar en el link y descargar el .zip que contiene el nuevo archivo .txt transformado y el archivo .txt con el nombre de las estaciones originales.

Copiar la información de este .txt transformado y pegarla en una copia del archivo .GEO que genera HECRAS.
Luego importar este archivo .GEO nuevo en HECRAS como "GIS format" en "Geometric Data".
Seleccionar "SI (metric) units" y luego "Finished - Import Data". Deberían aparecer la geometría sin problemas.

En HECRAS se debe corregir solo los "Reach Lengths" y moverlos todos 1 espacio hacia arriba, ya que estan corridos. La última sección debe tener distancia cero aguas abajo.
Además se debe poner en la descripción de los transversales la información del .txt con las estaciones originales. Para ambas ediciones se accede desde "Tables" en "Geometric Data".

Para volver a transformar otro archivo se debe repetir el proceso.



# Centrar Secciones HEC-RAS

Sirve para centrar las secciones de un archivo de geometría de HECRAS ya que al ser importado desde el CIVIL el 0 queda a la izquierda y no en el centro. Simplemente cambia el valor de x de cada sección.

Cargar el archivo de entrada *.g01 exportado desde la geometría de HECRAS pero cambiar el nombre y extensión a "geo.txt"
Si ya existe un archivo "geo.txt" se debe eliminar previamente.

Ir a "Actions" y correr "Centrar Secciones HEC-RAS".

Luego de que corra el script buscar en el resultado del proceso "Guardar geo_centrado.txt como artefacto descargable" y luego la línea "Artifacts download URL: ...".
Pinchar en el link y descargar el .zip que contiene el nuevo archivo .txt transformado.

Copiar la información de este .txt transformado y pegarla en una copia del archivo .g01 que genera HECRAS.
Luego importar este archivo .g01 nuevo en HECRAS como "HEC-RAS format" en "Geometric Data".
Seleccionar "SI (metric) units" y luego "Finished - Import Data". Deberían aparecer la geometría sin problemas.

Para volver a transformar otro archivo se debe repetir el proceso.

