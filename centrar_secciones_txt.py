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

            # Leer coordenadas originales
            for j in range(1, n_points + 1):
                coord_line = lines[i + j]

                # capturar formato exacto
                m = re.match(r'(\s*)([-\d\.]+)(\s+)([-\d\.]+)(.*)', coord_line)

                if not m:
                    new_lines.append(coord_line)
                    continue

                x_str = m.group(2)
                y_str = m.group(4)

                x = float(x_str)
                y = float(y_str)

                coords.append((x, y, coord_line, m))

            # calcular centro
            xs = [c[0] for c in coords]
            xmin = min(xs)
            xmax = max(xs)
            centro = (xmin + xmax) / 2

            # reescribir manteniendo formato
            for x, y, original_line, m in coords:

                new_x = x - centro

                # mantener largo original del número
                new_x_str = f"{new_x:.{len(m.group(2).split('.')[-1])}f}"
                new_x_str = new_x_str.rjust(len(m.group(2)))

                new_line = (
                    m.group(1) +
                    new_x_str +
                    m.group(3) +
                    m.group(4) +
                    m.group(5)
                )

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
