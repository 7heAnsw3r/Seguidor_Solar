from src import sun_position, panel_position, datetime_picker, sun_path
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