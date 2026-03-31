#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os


def centrar_secciones_txt(input_file):

    if not os.path.exists(input_file):
        print("❌ Archivo no encontrado")
        return

    output_file = "geo_centrado.txt"

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):

        line = lines[i]

        if "#Sta/Elev" in line:

            new_lines.append(line)

            match = re.search(r'=\s*(\d+)', line)
            if not match:
                print("⚠️ No se pudo leer número de puntos")
                return

            n_points = int(match.group(1))

            block_lines = lines[i+1:i+1+n_points]

            all_numbers = []
            number_positions = []

            # Extraer números con posición exacta
            for line_idx, bl in enumerate(block_lines):
                for m in re.finditer(r'-?\d+\.\d+', bl):
                    all_numbers.append(float(m.group()))
                    number_positions.append((line_idx, m.start(), m.end(), m.group()))

            # Tomar SOLO los X (pares)
            xs = all_numbers[::2]

            if not xs:
                print("⚠️ No se encontraron coordenadas")
                return

            xmin = min(xs)
            xmax = max(xs)
            centro = (xmin + xmax) / 2

            # Crear copia editable
            new_block_lines = block_lines.copy()

            count = 0

            for idx, (line_idx, start, end, original_str) in enumerate(number_positions):

                # Solo modificar X (pares)
                if idx % 2 == 0:

                    x_old = float(original_str)
                    x_new = x_old - centro

                    # Mantener formato original
                    decimals = len(original_str.split('.')[-1])
                    new_str = f"{x_new:.{decimals}f}"
                    new_str = new_str.rjust(len(original_str))

                    line = new_block_lines[line_idx]

                    new_line = (
                        line[:start] +
                        new_str +
                        line[end:]
                    )

                    new_block_lines[line_idx] = new_line

            # Agregar bloque modificado
            new_lines.extend(new_block_lines)

            i += n_points + 1
            continue

        else:
            new_lines.append(line)
            i += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("✅ Archivo generado:")
    print(output_file)


def main():
    if len(sys.argv) < 2:
        print("Uso: python centrar_secciones_txt.py geo.txt")
        return

    centrar_secciones_txt(sys.argv[1])


if __name__ == "__main__":
    main()
