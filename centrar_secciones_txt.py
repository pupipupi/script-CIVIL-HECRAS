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

        # Detectar bloque de sección
        if "#Sta/Elev" in line:

            new_lines.append(line)

            match = re.search(r'=\s*(\d+)', line)
            if not match:
                print("⚠️ Error leyendo número de puntos")
                return

            n_points = int(match.group(1))

            coords = []

            # Leer coordenadas
            for j in range(1, n_points + 1):
                parts = lines[i + j].split()
                x = float(parts[0])
                y = float(parts[1])
                coords.append((x, y))

            # Calcular centro geométrico
            xs = [c[0] for c in coords]
            xmin = min(xs)
            xmax = max(xs)
            centro = (xmin + xmax) / 2

            # Reescribir centrado
            for x, y in coords:
                new_x = x - centro
                new_lines.append(f"{new_x:.2f} {y:.2f}\n")

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
