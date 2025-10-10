import math
import re
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import streamlit as st

# CONFIG
doc_excel_token = st.secrets.get("Doc_Excel", "")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Agregar scopes aquí
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

gc = gspread.authorize(creds)

sh = gc.open_by_key(doc_excel_token)

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

    #Los cambios de filamento tienen el código M600 en el GCODE. Buscamos todos
    cambios_filamento = re.findall("M600", contenido)
    #Restamos uno porque se define el código M600 al final del GCODE: change_filament_gcode = M600
    cambios_filamento = len(cambios_filamento) - 1

    return tiempo_impresion, filamento, gramos, cambios_filamento

def filamentos_disponibles(inventario, tipo_filamento):
    if inventario == "Pano":
        CantidadesPano = sh.worksheet("CantidadesPano")
        data_Pano = CantidadesPano.get_all_records()
        df_pano = pd.DataFrame(data_Pano)
        df_pano = df_pano[['Tipo', 'Marca', 'Color', 'Cantidad']]
        return(list(set(df_pano[df_pano['Tipo'] == tipo_filamento]['Marca'])))
    else:
        CantidadesHierro = sh.worksheet("CantidadesHierro")
        data_Hierro = CantidadesHierro.get_all_records()
        df_hierro = pd.DataFrame(data_Hierro)
        df_hierro = df_hierro[['Tipo', 'Marca', 'Color', 'Cantidad']]
        return(list(set(df_hierro[df_hierro['Tipo'] == tipo_filamento]['Marca'])))

def colores_disponibles(inventario, tipo_filamento, marca_filamento):
    if inventario == "Pano":
        CantidadesPano = sh.worksheet("CantidadesPano")
        data_Pano = CantidadesPano.get_all_records()
        df_pano = pd.DataFrame(data_Pano)
        df_pano = df_pano[['Tipo', 'Marca', 'Color', 'Cantidad']]
        return(list(set(df_pano[(df_pano['Tipo'] == tipo_filamento) & (df_pano['Marca'] == marca_filamento)]['Color'])))
    else:
        CantidadesHierro = sh.worksheet("CantidadesHierro")
        data_Hierro = CantidadesHierro.get_all_records()
        df_hierro = pd.DataFrame(data_Hierro)
        df_hierro = df_hierro[['Tipo', 'Marca', 'Color', 'Cantidad']]
        return(list(set(df_hierro[(df_hierro['Tipo'] == tipo_filamento) & (df_hierro['Marca'] == marca_filamento)]['Color'])))