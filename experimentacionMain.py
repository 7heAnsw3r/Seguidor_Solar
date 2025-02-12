"""
Archivo principal para la ejecución del simulador de seguidor solar.

Este script obtiene la fecha y el rango de horas seleccionadas, calcula la 
posición solar y visualiza la trayectoria del panel y del sol en 3D.
"""

"""from src import sun_position, panel_position, datetime_picker, sun_path
from pytz import timezone
from datetime import datetime

# Obtener la fecha seleccionada desde `datetime_picker`
start_date = datetime.strptime(datetime_picker.st_fecha, "%Y-%m-%d")
start_date = start_date.replace(tzinfo=timezone("America/Guayaquil"))
print("Fecha de inicio:", start_date)

# Obtener la posición solar a partir de la fecha y las horas seleccionadas
times, azimuths, elevations, beta, alpha = sun_position.getSolarPosition(
    start_date, 
    start_hour=datetime_picker.start_t.hour, 
    end_hour=datetime_picker.end_t.hour
)

# Visualizar la trayectoria del panel solar en 3D
panel_position.visualizar_trayectoria_panel(times, azimuths, elevations, beta, alpha)

# Volver a calcular la posición solar para la trayectoria del sol
times, azimuths, elevations, beta, alpha = sun_position.getSolarPosition(
    start_date, 
    start_hour=datetime_picker.start_t.hour, 
    end_hour=datetime_picker.end_t.hour
)

# Imprimir en consola los datos de la trayectoria solar
for i in range(len(times)):
    print(f"Tiempo: {times[i]}, Azimut: {azimuths[i]}, Elevación: {elevations[i]}")

# Visualizar la trayectoria del sol en 3D
sun_path.graph_trayectoria_3d(times, azimuths, elevations)"""



"""
Archivo principal para la ejecución del simulador de seguidor solar.

Este script obtiene la fecha y el rango de horas seleccionadas, calcula la 
posición solar y visualiza la trayectoria del panel y del sol en 3D en una 
sola ventana.
"""

from Experimentacion import sun_position, panel_position, datetime_picker, sun_path
from pytz import timezone
from datetime import datetime, timedelta

start_date = datetime.strptime(datetime_picker.st_fecha, "%Y-%m-%d")
start_date = start_date.replace(tzinfo=timezone("America/Guayaquil"))
print(start_date)

times, azimuths, elevations, beta, alpha = sun_position.getSolarPosition(start_date, start_hour=datetime_picker.start_t.hour, end_hour=datetime_picker.end_t.hour)

# Llamar a la función para graficar la trayectoria
panel_position.visualizar_trayectoria_panel(times, azimuths, elevations, beta, alpha)

start_date = datetime.strptime(datetime_picker.st_fecha, "%Y-%m-%d")
start_date = start_date.replace(tzinfo=timezone("America/Guayaquil"))
times, azimuths, elevations, beta, alpha = sun_position.getSolarPosition(start_date, start_hour=datetime_picker.start_t.hour, end_hour=datetime_picker.end_t.hour)

for i in range(len(times)):
    print(f"Tiempo: {times[i]}, Azimut: {azimuths[i]}, Elevación: {elevations[i]}")

sun_path.graph_trayectoria_3d(times, azimuths, elevations)