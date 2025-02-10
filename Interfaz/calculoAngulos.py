"""
Módulo para el cálculo de ángulos en un seguidor solar.

Contiene funciones para calcular la matriz de rotación en 3D (`Rxyz`)
y la posición solar (`getSolarPosition`) con base en coordenadas geográficas
y un rango de tiempo definido.
"""

from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timedelta
import pytz
import numpy as np


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


def getSolarPosition(
    start_date: datetime,
    start_hour: int = 6,
    end_hour: int = 18,
    latitude: float = -0.2105367,
    longitude: float = -78.491614
):
    """
    Calcula la posición solar en un rango de tiempo específico.

    Args:
        start_date (datetime): Fecha y hora de inicio para la simulación.
        start_hour (int, opcional): Hora de inicio del cálculo (por defecto 6 AM).
        end_hour (int, opcional): Hora de fin del cálculo (por defecto 6 PM).
        latitude (float, opcional): Latitud del lugar de observación (por defecto -0.2105367, Quito).
        longitude (float, opcional): Longitud del lugar de observación (por defecto -78.491614, Quito).

    Returns:
        tuple: Contiene cinco listas con los siguientes datos:
            - times (list): Lista de tiempos de simulación.
            - azimuths (list): Lista de ángulos azimutales del sol.
            - elevations (list): Lista de ángulos de elevación solar.
            - beta (list): Lista de ángulos de pitch del panel solar.
            - alpha (list): Lista de ángulos de roll del panel solar.
    """
    # Definir la zona horaria (Ecuador - Guayaquil)
    timezone = pytz.timezone('America/Guayaquil')

    # Listas para almacenar los resultados
    times = []
    azimuths = []
    elevations = []
    beta = []  # Pitch
    alpha = []  # Roll

    # Intervalo de tiempo entre cálculos (10 minutos)
    time_interval = timedelta(minutes=10)

    # Convertir start_date a datetime si es un string
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Definir la hora de inicio y fin dentro de la fecha dada
    start_time = datetime.combine(start_date, datetime.min.time()).replace(hour=start_hour, minute=0, second=0)
    end_time = datetime.combine(start_date, datetime.min.time()).replace(hour=end_hour, minute=0, second=0)

    # Asociar la zona horaria
    start_time = timezone.localize(start_time)
    end_time = timezone.localize(end_time)

    current_time = start_time

    while current_time <= end_time:
        # Obtener el azimut y la elevación solar usando pysolar
        az = get_azimuth(latitude, longitude, current_time)
        el = get_altitude(latitude, longitude, current_time)

        # Convertir a radianes para cálculos
        az_rad = np.radians(az)
        el_rad = np.radians(el)

        # --- Cálculo de beta (pitch) y alpha (roll) usando la matriz de rotación ---

        # Suponemos gamma = 0 en este caso
        gamma = 0
        
        # Calcular beta (pitch) con la ecuación trigonométrica
        val = np.cos(el_rad) * np.sin(az_rad)
        beta_rad_temp = np.arcsin(val)
        beta_deg_temp = np.degrees(beta_rad_temp)

        # Calcular alpha (roll) con la ecuación trigonométrica
        val_fi1 = -(np.cos(el_rad) * np.cos(az_rad)) / np.cos(beta_rad_temp)
        alpha_rad_temp = np.arcsin(val_fi1)
        alpha_deg_temp = np.degrees(alpha_rad_temp)

        # Obtener la matriz de rotación combinada
        R = Rxyz(alpha_deg_temp, beta_deg_temp, gamma)

        # Extraer elementos de la matriz de rotación
        R31 = R[2, 0]
        R11 = R[0, 0]
        R21 = R[1, 0]
        R32 = R[2, 1]
        R33 = R[2, 2]

        # Calcular beta (pitch) usando arctan2
        beta_rad = np.arctan2(-R31, np.sqrt(R11**2 + R21**2))
        beta_deg = np.degrees(beta_rad)

        # Calcular alpha (roll) usando arctan2
        alpha_rad = np.arctan2(R32, R33)
        alpha_deg = np.degrees(alpha_rad)

        # ---------------------------------------------------------------

        # Guardar valores en las listas
        times.append(current_time)
        azimuths.append(az)
        elevations.append(el)
        beta.append(beta_deg)  # Pitch
        alpha.append(alpha_deg)  # Roll

        # Avanzar en el tiempo por intervalos de 10 minutos
        current_time += time_interval

    return times, azimuths, elevations, beta, alpha
