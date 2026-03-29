#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reenumerar líneas STATION: de un archivo de abajo hacia arriba.
El último STATION (más abajo en el archivo) se convierte en 1, 
el penúltimo en 2, y así sucesivamente.

Uso:
    python reenumerar_stations.py archivo_entrada.txt [archivo_salida.txt]

Si no se especifica archivo_salida, se creará automáticamente como:
    archivo_entrada_transformado.txt
"""

import re
import sys
import os


def reenumerar_stations(input_file, output_file=None):
    """
    Reenumera las líneas STATION: de un archivo de abajo hacia arriba
    comenzando desde 1.
    """

    # Validar que el archivo existe
    if not os.path.exists(input_file):
        print(f"❌ Error: No se encontró el archivo: {input_file}")
        return None

    # Crear nombre de salida automático si no se especifica
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_transformado{ext}"

    # Leer el archivo completo
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return None

    # Encontrar todas las líneas que contienen "STATION:" y sus posiciones
    station_positions = []
    # Patrón: STATION: seguido de espacios y un número (puede tener decimales)
    station_pattern = re.compile(r'^(\s*STATION:\s*)([\d\.]+)(.*)$')

    for i, line in enumerate(lines):
        match = station_pattern.match(line)
        if match:
            station_positions.append({
                'line_index': i,
                'prefix': match.group(1),      # "STATION: "
                'old_number': match.group(2),   # número original
                'suffix': match.group(3)        # resto de la línea (si hay)
            })

    if not station_positions:
        print("⚠️  No se encontraron líneas STATION: en el archivo")
        return None

    print(f"📊 Se encontraron {len(station_positions)} líneas STATION:")

    # Mostrar mapeo de cambios
    print("\n📝 Mapeo de reenumeración (de abajo hacia arriba):")
    print("-" * 55)

    # Reenumerar: el último elemento (más abajo en el archivo) será el 1
    total_stations = len(station_positions)
    for i, station in enumerate(station_positions):
        new_number = total_stations - i  # De abajo hacia arriba
        old_number = station['old_number']
        station['new_number'] = new_number
        # Solo mostrar los primeros y últimos 5 para no saturar la consola
        if i < 5 or i >= total_stations - 5:
            print(f"  STATION: {old_number} → STATION: {new_number}")
        elif i == 5:
            print(f"  ... ({total_stations - 10} más) ...")

    # Crear las nuevas líneas modificadas
    new_lines = lines.copy()
    for station in station_positions:
        new_line = f"{station['prefix']}{station['new_number']}{station['suffix']}\n"
        new_lines[station['line_index']] = new_line

    # Guardar el archivo resultante
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")
        return None

    print(f"\n✅ ¡Listo! Archivo transformado guardado en:")
    print(f"   {os.path.abspath(output_file)}")
    print(f"\n📈 Resumen:")
    print(f"   • Total de líneas procesadas: {len(lines)}")
    print(f"   • Total de STATION reenumerados: {total_stations}")
    print(f"   • STATION más alto ahora es: {total_stations}")
    print(f"   • STATION más bajo ahora es: 1")

    return output_file


def main():
    # Verificar argumentos de línea de comandos
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nEjemplos de uso:")
        print("  python reenumerar_stations.py mi_archivo.txt")
        print("  python reenumerar_stations.py entrada.txt salida.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    reenumerar_stations(input_file, output_file)


if __name__ == "__main__":
    main()
