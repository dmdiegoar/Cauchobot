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




from itertools import permutations

nnn


def generate_combinations(base_pattern, char_position):
    for perm in permutations(numbers + words):
        if (all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1)) and 
            all(words[i] <= words[i+1] for i in range(len(words)-1))):
            perm_list = list(perm)
            if char_position == 'middle':
                new_perm = []
                for i, item in enumerate(perm_list):
                    new_perm.append(item)
                    if i % 2 == 1 and i != len(perm_list) - 1:  # Insert character after each word except the last
                        new_perm.append(char)
                all_combinations.append(''.join(new_perm))
            else:  # char_position == 'end'
                all_combinations.append(''.join(perm_list) + char)

# Generar combinaciones para cada estructura
for pattern in [
    ['number', 'word'],  # Número, palabra
    ['word', 'number'],  # Palabra, número
]:
    for i in range(2):  # 2 para las dos variaciones de posición del carácter
        if i == 0:
            generate_combinations(pattern, 'middle')
        else:
            generate_combinations(pattern, 'end')

# Imprimir todas las combinaciones
print(f"Total de combinaciones: {len(all_combinations)}")
for combo in all_combinations:
    print(combo)
