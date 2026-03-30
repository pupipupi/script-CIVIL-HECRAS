Cargar el archivo de entrada *.GEO exportado desde CIVIL a HECRAS pero cambiar el nombre a "input.txt"
Si ya existe un archivo "input.txt" se debe eliminar previamente.

Ir a "Actions" y correr.

Luego de que corra el script buscar en el resultado del proceso "Subir resultado" y luego la línea "Artifacts download URL: ...".
Pinchar en el link y descargar el nuevo archivo .txt.

Copiar la información de este .txt descargado y pegarla en una copia del archivo .GEO que genera HECRAS.
Luego importar este archivo .GEO nuevo en HECRAS como "GIS format" en "Geometric Data".
Seleccionar "SI (metric) units" y luego "Finished - Import Data".

En HECRAS se debe corregir solo los "Reach Legnths", ya que estan corridos. El ultimo corte debe tener distancia 0

Para volver a transformar otro archivo se debe repetir el proceso.
