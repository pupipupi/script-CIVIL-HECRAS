Cargar el archivo de entrada *.GEO exportado desde CIVIL a HECRAS pero cambiar el nombre y extensión a "input.txt"
Si ya existe un archivo "input.txt" se debe eliminar previamente.

Ir a "Actions" y correr.

Luego de que corra el script buscar en el resultado del proceso "Subir resultado" y luego la línea "Artifacts download URL: ...".
Pinchar en el link y descargar el .zip que contiene el nuevo archivo .txt transformado y el archivo .txt con el nombre de las estaciones originales.

Copiar la información de este .txt transformado y pegarla en una copia del archivo .GEO que genera HECRAS.
Luego importar este archivo .GEO nuevo en HECRAS como "GIS format" en "Geometric Data".
Seleccionar "SI (metric) units" y luego "Finished - Import Data". Deberían aparecer la geometría sin problemas.

En HECRAS se debe corregir solo los "Reach Lengths" y moverlos todos 1 espacio hacia arriba, ya que estan corridos. La última sección debe tener distancia cero aguas abajo.
Además se debe poner en la descripción de los transversales la información del .txt con las estaciones originales. Para ambas ediciones se accede desde "Tables" en "Geometric Data".

Para volver a transformar otro archivo se debe repetir el proceso.
