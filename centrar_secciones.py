"""
centrar_secciones.py
Centra las secciones transversales (#Sta/Elev) de un archivo .geo de HEC-RAS.
Para cada sección resta x_max/2 a cada estación, dejando el centro en 0.

Uso:
    python centrar_secciones.py <entrada> <salida>
Ejemplo:
    python centrar_secciones.py geo.txt geo_centrado.txt
"""

import sys
import re


def formatear_valor(v):
    if v == int(v):
        return f"{int(v):>7}"
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return f"{s:>7}"


def centrar_y_reconstruir(lineas_bloque):
    pares = []
    for linea in lineas_bloque:
        tokens = linea.split()
        if len(tokens) % 2 != 0:
            raise ValueError(f"Número impar de tokens en: '{linea}'")
        for i in range(0, len(tokens), 2):
            pares.append((float(tokens[i]), float(tokens[i + 1])))

    x_max = max(p[0] for p in pares)
    offset = x_max / 2.0
    pares_centrados = [(round(x - offset, 6), elev) for x, elev in pares]

    lineas_nuevas = []
    for i in range(0, len(pares_centrados), 5):
        grupo = pares_centrados[i:i + 5]
        linea = "  ".join(formatear_valor(sta) + formatear_valor(elev) for sta, elev in grupo)
        lineas_nuevas.append(linea + "\n")

    return lineas_nuevas


def procesar_archivo(ruta_entrada, ruta_salida):
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    resultado = []
    i = 0
    count = 0

    while i < len(lineas):
        linea = lineas[i]
        match = re.match(r'^#Sta/Elev=\s*(\d+)', linea)
        if match:
            n_pares = int(match.group(1))
            resultado.append(linea)
            i += 1
            n_lineas = (n_pares + 4) // 5
            bloque = [lineas[i + j].rstrip('\n') for j in range(n_lineas) if i + j < len(lineas)]
            try:
                resultado.extend(centrar_y_reconstruir(bloque))
                count += 1
            except Exception as e:
                print(f"  [ADVERTENCIA] Sección en línea {i}: {e}. Se conserva original.")
                resultado.extend(lb + "\n" for lb in bloque)
            i += n_lineas
        else:
            resultado.append(linea)
            i += 1

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.writelines(resultado)

    print(f"OK — {count} secciones centradas → {ruta_salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python centrar_secciones.py <entrada> <salida>")
        sys.exit(1)
    procesar_archivo(sys.argv[1], sys.argv[2])
