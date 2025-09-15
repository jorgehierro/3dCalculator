import re
from dataclasses import dataclass


#Definición de configuración de la impresora
@dataclass
class Configuracion:
    precio_kw: float = 0.15                 # €/kWh
    consumo_maquina: float = 0.4            # kW
    precio_cambio_filamento: float = 0.12   # €/cambio
    precio_mantenimiento: float = 0.15      # €/hora
    precio_hora_diseno: float = 15          # €/hora diseño/gestiones
    precio_hora_post: float = 8             # €/hora postprocesado

# Diccionario de filamentos (€/kg)
filamentos = {
    "PLA": 13, #Precio original 13. Inflamos un 30% -> 16.9
    "PETG": 14, #Precio original 14. Inflamos un 30% -> 18.2
    'PLA-plus': 19 #Precio original 19. Inflamos un 30% -> 24
}

#Función auxiliar

def parse_tiempo(tiempo_str: str) -> float:
    """
    Convierte un string tipo '3h12m' en horas decimales.
    """
    match = re.match(r'(\d+)h(\d+)m', tiempo_str)
    if not match:
        raise ValueError("Formato de tiempo inválido. Usa 'xhym' (ejemplo: '3h12m')")
    horas, minutos = int(match.group(1)), int(match.group(2))
    return horas + minutos / 60


#Cálculo de los costes

def precio_base_impresion(tipo_filamento: str, tiempo_impresion: str, cantidad_filamento: float, cambios_filamento: int,
                          cfg: Configuracion = Configuracion()) -> float:
    """
    Calcula el coste base de la impresión:
    - Filamento usado
    - Consumo eléctrico
    - Mantenimiento/desgaste
    - Cambios de filamento
    """
    horas = parse_tiempo(tiempo_impresion)

    coste_filamento = filamentos[tipo_filamento] / 1000 * cantidad_filamento
    coste_energia = horas * cfg.precio_kw * cfg.consumo_maquina
    coste_mantenimiento = horas * cfg.precio_mantenimiento
    coste_cambios = cambios_filamento * cfg.precio_cambio_filamento

    return coste_filamento + coste_energia + coste_mantenimiento + coste_cambios


def precio_mano_obra(tiempo_diseño: float, tiempo_postprocesado: float,
                     cfg: Configuracion = Configuracion()) -> float:
    """
    Calcula el coste de la mano de obra:
    - Diseño / gestiones
    - Postprocesado
    """
    return cfg.precio_hora_diseno * tiempo_diseño + cfg.precio_hora_post * tiempo_postprocesado


def precio_total(tipo_filamento: str, tiempo_impresion: str, cantidad_filamento: float, cambios_filamento: int,
                 tiempo_diseño: float, tiempo_postprocesado: float, unidades: int,
                 cfg: Configuracion = Configuracion()):
    """
    Calcula el coste total y el coste unitario.
    Devuelve (coste_total, coste_unitario)
    """
    coste_impresion = precio_base_impresion(tipo_filamento, tiempo_impresion, cantidad_filamento, cambios_filamento, cfg)
    coste_mano_obra = precio_mano_obra(tiempo_diseño, tiempo_postprocesado, cfg)

    coste_total = coste_impresion + coste_mano_obra
    coste_unitario = coste_impresion + coste_mano_obra / unidades

    return coste_total, coste_unitario, coste_impresion, coste_mano_obra
