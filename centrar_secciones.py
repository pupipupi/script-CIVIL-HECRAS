#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os


def centrar_secciones(input_file):

    if not os.path.exists(input_file):
        print("Archivo no encontrado")
        return

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_centrado{ext}"

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):

        line = lines[i]

        # Detectar inicio de geometría de sección
        if "#Sta/Elev" in line:

            new_lines.append(line)

            # número de puntos
            match = re.search(r'=(\s*)(\d+)', line)
            n_points = int(match.group(2))

            coords = []

            # leer puntos
            for j in range(1, n_points + 1):
                parts = lines[i + j].split()
                x = float(parts[0])
                y = float(parts[1])
                coords.append((x, y))

            # calcular centro
            xs = [c[0] for c in coords]
            xmin = min(xs)
            xmax = max(xs)
            centro = (xmin + xmax) / 2

            # recalcular
            new_coords = []
            for x, y in coords:
                new_x = x - centro
                new_coords.append((new_x, y))

            # escribir nuevos puntos
            for x, y in new_coords:
                new_lines.append(f"{x:.2f} {y:.2f}\n")

            i += n_points + 1
            continue

        else:
            new_lines.append(line)
            i += 1

    # guardar
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print("✅ Archivo centrado generado:")
    print(output_file)


def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py archivo.geo")
        return

    centrar_secciones(sys.argv[1])


if __name__ == "__main__":
    main()
