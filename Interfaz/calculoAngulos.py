from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timedelta
import pytz
import numpy as np

def Rxyz(alpha, beta, gamma):
    """
    Calcula la matriz de rotación 3D Rxyz(α, β, γ).

    Args:
      alpha: Ángulo de rotación alrededor del eje X (en grados).
      beta: Ángulo de rotación alrededor del eje Y (en grados).
      gamma: Ángulo de rotación alrededor del eje Z (en grados).

    Returns:
      np.array: Matriz de rotación 3D.
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
    Calcula posiciones solares y ángulos para una fecha específica y rango de horas.

    Args:
      start_date (datetime): Fecha y hora de inicio para la simulación.
      start_hour (int): Hora de inicio del cálculo.
      end_hour (int): Hora de fin del cálculo.
      latitude (float): Latitud para la posición geográfica.
      longitude (float): Longitud para la posición geográfica.

    Returns:
      tuple: Tupla con los siguientes elementos:
          - times (list): Lista de tiempos de simulación.
          - azimuths (list): Lista de ángulos azimutales.
          - elevations (list): Lista de ángulos de elevación.
          - beta (list): Lista de ángulos de pitch.
          - alpha (list): Lista de ángulos de roll.
    """
    # Definir la zona horaria (ajústalo según tu ubicación)
    timezone = pytz.timezone('America/Guayaquil')
    times = []
    azimuths = []
    elevations = []
    beta = []  # Pitch
    alpha = []  # Roll

    time_interval = timedelta(minutes=10)

    # Crear el rango de tiempos basado en la hora de inicio y fin
    if isinstance(start_date, str):  
      start_date = datetime.strptime(start_date, "%Y-%m-%d")  # Ajusta el formato según tu fecha

    start_time = datetime.combine(start_date, datetime.min.time()).replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end_time = datetime.combine(start_date, datetime.min.time()).replace(hour=end_hour, minute=0, second=0, microsecond=0)

    # Asociar la zona horaria a las fechas
    start_time = timezone.localize(start_time)
    end_time = timezone.localize(end_time)

    current_time = start_time

    while current_time <= end_time:
        az = get_azimuth(latitude, longitude, current_time)
        el = get_altitude(latitude, longitude, current_time)

        # Convertir a radianes para los cálculos
        az_rad = np.radians(az)
        el_rad = np.radians(el)

        # --- Calcular beta (roll) y alpha (pitch) usando la matriz de rotación ---

        # 1. Calcular la matriz de rotación Rxyz(α, β, γ)
        gamma = 0            # (Asumimos gamma = 0 en este caso)
        # Calculamos beta y alpha
        val = np.cos(el_rad) * np.sin(az_rad)
        beta_rad_temp = np.arcsin(val)
        beta_deg_temp = np.degrees(beta_rad_temp)

        val_fi1 = -(np.cos(el_rad) * np.cos(az_rad)) / np.cos(beta_rad_temp)
        alpha_rad_temp = np.arcsin(val_fi1)
        alpha_deg_temp = np.degrees(alpha_rad_temp)

        R = Rxyz(alpha_deg_temp, beta_deg_temp, gamma)

        # 2. Obtener los elementos de la matriz
        R31 = R[2, 0]
        R11 = R[0, 0]
        R21 = R[1, 0]
        R32 = R[2, 1]
        R33 = R[2, 2]

        # 3. Calcular beta (pitch)
        beta_rad = np.arctan2(-R31, np.sqrt(R11**2 + R21**2))
        beta_deg = np.degrees(beta_rad)

        # 4. Calcular alpha (roll)
        alpha_rad = np.arctan2(R32, R33)
        alpha_deg = np.degrees(alpha_rad)

        # ---------------------------------------------------------------

        times.append(current_time)
        azimuths.append(az)
        elevations.append(el)
        beta.append(beta_deg)  # Pitch
        alpha.append(alpha_deg)  # Roll

        current_time += time_interval

    return times, azimuths, elevations, beta, alpha