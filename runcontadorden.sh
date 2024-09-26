#!/bin/bash



# Activar el entorno virtual
source /home/ubuntu/pyrofex/bin/activate
# Cambiar el directorio a la ubicación de los scripts
cd /home/ubuntu/libros

# Lista de nombres de archivos Python que deseas ejecutar
archivos_py=("contador_de_ordenes.py")

# Iterar sobre cada archivo Python en la lista
for archivo_py in "${archivos_py[@]}"; do
    # Verificar si el script está en ejecución buscando el identificador en la lista de procesos
    if pgrep -fl "$archivo_py" >/dev/null; then
        echo "El archivo $archivo_py ya está en ejecución."
    else
        # Si no está en ejecución, iniciar el archivo Python
        echo "Iniciando $archivo_py"
        /home/ubuntu/pyrofex/bin/python3 "$archivo_py" &
        echo "Se inició $archivo_py a $(date)" >> /ruta/a/tu/log_de_ejecucion.log
    fi
    # Esperar un segundo antes de continuar con la siguiente iteración
    sleep 1
done

exit