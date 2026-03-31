"""
centrar_secciones.py
Centra las secciones transversales de un archivo .geo de HEC-RAS.
Ajusta: #Sta/Elev, #Mann, Bank Sta, Levee (campo X).
"""

import sys
import re


def formatear_valor(v):
    if v == int(v):
        return f"{int(v):>7}"
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return f"{s:>7}"


def centrar_sta_elev(lineas_bloque, offset):
    pares = []
    for linea in lineas_bloque:
        tokens = linea.split()
        if len(tokens) % 2 != 0:
            raise ValueError(f"Tokens impares: '{linea}'")
        for i in range(0, len(tokens), 2):
            pares.append((float(tokens[i]), float(tokens[i + 1])))

    pares_c = [(round(x - offset, 6), elev) for x, elev in pares]

    lineas_nuevas = []
    for i in range(0, len(pares_c), 5):
        grupo = pares_c[i:i + 5]
        linea = "  ".join(formatear_valor(sta) + formatear_valor(elev) for sta, elev in grupo)
        lineas_nuevas.append(linea + "\n")
    return lineas_nuevas


def ajustar_mann(linea, offset):
    """#Mann tiene grupos de 3: sta, n, flag. Ajusta solo el primer valor de cada grupo."""
    tokens = linea.split()
    # Formato: #Mann= N , 0 , 0
    # La línea de datos siguiente tiene triples: sta  n  flag
    return linea  # encabezado, no tocar


def ajustar_mann_datos(linea, offset):
    """Ajusta los valores X en la línea de datos de Manning (cada 3er valor: x, n, flag)."""
    tokens = linea.split()
    if len(tokens) % 3 != 0:
        return linea  # no tiene el formato esperado, dejar igual
    nuevos = []
    for i in range(0, len(tokens), 3):
        x = round(float(tokens[i]) - offset, 6)
        n = tokens[i+1]
        flag = tokens[i+2]
        nuevos.extend([formatear_valor(x), f"{n:>8}", f"{flag:>7}"])
    return "  ".join(nuevos) + "\n"


def ajustar_bank_sta(linea, offset):
    """Bank Sta=x1,x2 → restar offset a cada valor."""
    m = re.match(r'^(Bank Sta=)([\d.\-]+),([\d.\-]+)(.*)', linea)
    if m:
        x1 = round(float(m.group(2)) - offset, 6)
        x2 = round(float(m.group(3)) - offset, 6)
        def fmt(v):
            if v == int(v): return str(int(v))
            return f"{v:.2f}".rstrip('0').rstrip('.')
        return f"{m.group(1)}{fmt(x1)},{fmt(x2)}{m.group(4)}\n"
    return linea


def ajustar_levee(linea, offset):
    """Levee=flag,,,flag2,x,,, → ajustar el campo X en posición 4 (índice 4)."""
    partes = linea.rstrip('\n\r').split(',')
    # Formato: Levee=val,,,val,X,,,
    # El valor X está en el índice 4
    if len(partes) >= 5 and partes[4].strip() != '':
        try:
            x = round(float(partes[4]) - offset, 6)
            def fmt(v):
                if v == int(v): return str(int(v))
                return f"{v:.2f}".rstrip('0').rstrip('.')
            partes[4] = fmt(x)
        except ValueError:
            pass
    return ','.join(partes) + "\n"


def procesar_archivo(ruta_entrada, ruta_salida):
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    resultado = []
    i = 0
    count = 0
    offset_actual = None  # offset de la sección activa

    while i < len(lineas):
        linea = lineas[i]
        linea_strip = linea.strip()

        # --- Detectar #Sta/Elev ---
        match_sta = re.match(r'^#Sta/Elev=\s*(\d+)', linea)
        if match_sta:
            n_pares = int(match_sta.group(1))
            resultado.append(linea)
            i += 1
            n_lineas = (n_pares + 4) // 5
            bloque = [lineas[i + j].rstrip('\n') for j in range(n_lineas) if i + j < len(lineas)]

            # Calcular offset desde los datos reales
            pares = []
            for lb in bloque:
                tokens = lb.split()
                for k in range(0, len(tokens), 2):
                    pares.append(float(tokens[k]))
            x_min = min(pares)
            x_max = max(pares)
            offset_actual = (x_min + x_max) / 2.0

            try:
                resultado.extend(centrar_sta_elev(bloque, offset_actual))
                count += 1
            except Exception as e:
                print(f"  [ADVERTENCIA] Sección línea {i}: {e}. Se conserva original.")
                resultado.extend(lb + "\n" for lb in bloque)
                offset_actual = None
            i += n_lineas
            continue

        # --- Detectar #Mann (encabezado, no tocar) ---
        if linea_strip.startswith('#Mann=') and offset_actual is not None:
            resultado.append(linea)
            i += 1
            # La siguiente línea son los datos de Manning
            if i < len(lineas):
                resultado.append(ajustar_mann_datos(lineas[i], offset_actual))
                i += 1
            continue

        # --- Bank Sta ---
        if linea_strip.startswith('Bank Sta=') and offset_actual is not None:
            resultado.append(ajustar_bank_sta(linea, offset_actual))
            i += 1
            continue

        # --- Levee ---
        if linea_strip.startswith('Levee=') and offset_actual is not None:
            resultado.append(ajustar_levee(linea, offset_actual))
            i += 1
            continue

        # --- Nuevo bloque de sección (resetear offset) ---
        if linea_strip.startswith('Type RM Length'):
            offset_actual = None

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
