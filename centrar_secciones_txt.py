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
            n_points = int(match.group(1))

            coords = []

            # Leer todas las líneas del bloque
            block_lines = lines[i+1:i+1+n_points]

            all_numbers = []

            # Extraer TODOS los números
            for bl in block_lines:
                nums = re.findall(r'-?\d+\.\d+', bl)
                all_numbers.extend(nums)

            # Convertir a pares (X,Y)
            for j in range(0, len(all_numbers), 2):
                x = float(all_numbers[j])
                y = float(all_numbers[j+1])
                coords.append((x, y))

            # Calcular centro
            xs = [c[0] for c in coords]
            xmin = min(xs)
            xmax = max(xs)
            centro = (xmin + xmax) / 2

            # Reescribir respetando formato original
            idx = 0
            for bl in block_lines:

                nums = re.findall(r'-?\d+\.\d+', bl)

                new_line = bl

                for n in nums:
                    if idx % 2 == 0:
                        # es X
                        x_old = float(n)
                        x_new = x_old - centro

                        # mantener formato largo
                        decimals = len(n.split('.')[-1])
                        x_new_str = f"{x_new:.{decimals}f}"

                        new_line = new_line.replace(n, x_new_str, 1)

                    idx += 1

                new_lines.append(new_line)

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
