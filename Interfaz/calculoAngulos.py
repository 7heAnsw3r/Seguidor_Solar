"""
Módulo para el cálculo de la posición solar y la transformación de ángulos.

Este módulo utiliza `pysolar` para calcular el azimut y la elevación del sol 
en función de la fecha, hora y ubicación geográfica. También incluye funciones
para calcular la matriz de rotación en 3D para ajustar la orientación del panel solar.
"""

from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timedelta
import numpy as np
import pytz


def Rxyz(alpha, beta, gamma):
    """
    Calcula la matriz de rotación 3D Rxyz(α, β, γ).

    Args:
        alpha (float): Ángulo de rotación alrededor del eje X (en grados).
        beta (float): Ángulo de rotación alrededor del eje Y (en grados).
        gamma (float): Ángulo de rotación alrededor del eje Z (en grados).

    Returns:
        np.array: Matriz de rotación 3D de tamaño (3x3).
    """
    # Convertir los ángulos a radianes
    alpha_rad = np.radians(alpha)
    beta_rad = np.radians(beta)
    gamma_rad = np.radians(gamma)

    # Matrices de rotación individuales
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha_rad), -np.sin(alpha_rad)],
        [0, np.sin(alpha_rad), np.cos(alpha_rad)]
    ])

    Ry = np.array([
        [np.cos(beta_rad), 0, np.sin(beta_rad)],
        [0, 1, 0],
        [-np.sin(beta_rad), 0, np.cos(beta_rad)]
    ])

    Rz = np.array([
        [np.cos(gamma_rad), -np.sin(gamma_rad), 0],
        [np.sin(gamma_rad), np.cos(gamma_rad), 0],
        [0, 0, 1]
    ])

    # Multiplicar las matrices en el orden correcto: Rz(γ) * Ry(β) * Rx(α)
    R = np.dot(Rz, np.dot(Ry, Rx))
    
    return R


def getSolarPosition(start_date: str, start_hour: str, end_hour: str, latitude: float = -0.2105367, longitude: float = -78.491614):
    """
    Calcula la posición del sol (azimut, elevación) durante un intervalo de tiempo.

    Args:
        start_date (str): Fecha de inicio en formato "YYYY-MM-DD".
        start_hour (str): Hora de inicio en formato "HH:MM".
        end_hour (str): Hora de fin en formato "HH:MM".
        latitude (float): Latitud geográfica de la ubicación. Por defecto es -0.2105367 (Quito).
        longitude (float): Longitud geográfica de la ubicación. Por defecto es -78.491614 (Quito).

    Returns:
        tuple: Tupla que contiene las listas de:
            - times (list): Lista de tiempos de simulación.
            - azimuths (list): Lista de valores de azimut.
            - elevations (list): Lista de valores de elevación.
            - beta (list): Lista de valores de ángulo β.
            - alpha (list): Lista de valores de ángulo α.
    """
    # Listas para almacenar los resultados
    times = []
    azimuths = []
    elevations = []
    beta = []
    alpha = []

    # Intervalo de tiempo de 10 minutos
    time_interval = timedelta(minutes=10)

    # LIMPIAR Y CONVERTIR LOS DATOS RECIBIDOS
    start_date = str(start_date).replace("Fecha: ", "").strip()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    if isinstance(start_hour, str):  
        start_hour = start_hour.replace("Hora de inicio: ", "").strip().split(":")[0]
    start_hour = int(start_hour)  # Convertir a entero si aún no lo es

    if isinstance(end_hour, str):  
        end_hour = end_hour.replace("Hora de fin: ", "").strip().split(":")[0]
    end_hour = int(end_hour)  # Convertir a entero si aún no lo es

    # Definir la zona horaria de Quito (UTC-5)
    timezone = pytz.timezone("America/Guayaquil")

    # Combinar correctamente la fecha con la hora de inicio y fin
    start_time = datetime.combine(start_date, datetime.min.time()).replace(hour=start_hour, minute=0, second=0, microsecond=0)
    start_time = timezone.localize(start_time)  # Convertir a timezone-aware

    end_time = datetime.combine(start_date, datetime.min.time()).replace(hour=end_hour, minute=0, second=0, microsecond=0)
    end_time = timezone.localize(end_time)  # Convertir a timezone-aware

    # Inicializar el tiempo actual en el tiempo de inicio
    current_time = start_time

    # Bucle para iterar sobre el intervalo de tiempo
    while current_time <= end_time:
        # Asegurarse de que current_time tiene la zona horaria
        current_time = timezone.localize(current_time) if current_time.tzinfo is None else current_time

        # Obtener el azimut y la elevación del sol
        az = get_azimuth(latitude, longitude, current_time)
        el = get_altitude(latitude, longitude, current_time)

        # Convertir azimut y elevación a radianes
        az_rad = np.radians(az)
        el_rad = np.radians(el)

        # Ángulo de rotación alrededor del eje Z
        gamma = 0
        
        # Calcular los ángulos β y α para la orientación del panel solar
        val = np.cos(el_rad) * np.sin(az_rad)
        beta_rad_temp = np.arcsin(val)
        beta_deg_temp = np.degrees(beta_rad_temp)

        val_fi1 = -(np.cos(el_rad) * np.cos(az_rad)) / np.cos(beta_rad_temp)
        alpha_rad_temp = np.arcsin(val_fi1)
        alpha_deg_temp = np.degrees(alpha_rad_temp)

        # Obtener la matriz de rotación
        R = Rxyz(alpha_deg_temp, beta_deg_temp, gamma)

        # Extraer los ángulos de la matriz de rotación
        R31 = R[2, 0]
        R11 = R[0, 0]
        R21 = R[1, 0]
        R32 = R[2, 1]
        R33 = R[2, 2]

        # Calcular los ángulos finales β y α
        beta_rad = np.arctan2(-R31, np.sqrt(R11**2 + R21**2))
        beta_deg = np.degrees(beta_rad)

        alpha_rad = np.arctan2(R32, R33)
        alpha_deg = np.degrees(alpha_rad)

        # Guardar los resultados
        times.append(current_time)
        azimuths.append(az)
        elevations.append(el)
        beta.append(beta_deg)
        alpha.append(alpha_deg)

        # Avanzar al siguiente intervalo de tiempo
        current_time += time_interval

    # Devolver los resultados calculados
    return times, azimuths, elevations, beta, alpha

