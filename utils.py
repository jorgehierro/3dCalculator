import math
import re

def leer_gcode(uploaded_file):
    # uploaded_file es un objeto UploadedFile, no una ruta
    return uploaded_file.read().decode("utf-8", errors="ignore")

def redondear_a_15min_superior(cadena):
    # extraer horas, minutos y segundos
    match = re.search(r'(\d+)h\s+(\d+)m\s+(\d+)s', cadena)
    if not match:
        raise ValueError("Formato inválido. Se esperaba algo como '1h 50m 44s'")
    
    horas, minutos, segundos = map(int, match.groups())
    total_segundos = horas*3600 + minutos*60 + segundos
    
    # 15 minutos = 900 segundos
    total_redondeado = math.ceil(total_segundos / 900) * 900
    
    # convertir de nuevo a h, m, s
    h = total_redondeado // 3600
    m = (total_redondeado % 3600) // 60
    s = total_redondeado % 60
    
    return f"{h}h{m}m"

def leer_parametros(contenido):

    tiempo = contenido.find("estimated printing time (normal mode)")
    tiempo_impresion = contenido[tiempo + 39: tiempo + 60].split("\n", 1)[0]
    tiempo_impresion = redondear_a_15min_superior(tiempo_impresion)

    filamento = contenido.find("filament_type =")
    cadena_filamento = contenido[filamento: filamento + 28 + 50].split("\n", 1)[0]

    match = re.search(r'(PLA|PETG)', cadena_filamento)
    if match:
        filamento = match.group(1)  # el texto que coincide (PLA o PETG)

    gramos = contenido.find("total filament used [g]")
    gramos = float(contenido[gramos:].split("\n", 1)[0].split("=")[1])
    gramos = math.ceil(gramos / 5) * 5

    return tiempo_impresion, filamento, gramos