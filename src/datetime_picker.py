import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Variables globales para almacenar la fecha y las horas
st_fecha = None
start_t = None
end_t = None


def obtener_fecha_y_horas():
    global st_fecha, start_t, end_t  # Usar variables globales

    # Obtiene la fecha seleccionada
    fecha_seleccionada = calendario.get_date()
    st_fecha = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y-%m-%d")

    # Obtiene las horas de inicio y fin
    hora_inicio = combo_inicio.get()
    hora_fin = combo_fin.get()

    try:
        start_t = datetime.strptime(hora_inicio, "%H").time()
        end_t = datetime.strptime(hora_fin, "%H").time()

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese las horas en formato HH:MM")

    # Cerrar la ventana principal (opcional)
    ventana.destroy()


def actualizar_horas_fin(event=None):
    """Actualiza las opciones del combobox de hora fin
    para que solo muestre horas posteriores a la hora de inicio."""
    hora_inicio = combo_inicio.get()
    try:
        indice_inicio = horas.index(hora_inicio)
        horas_fin = horas[indice_inicio + 1:]  # Tomar horas posteriores a la de inicio
        combo_fin['values'] = horas_fin
        combo_fin.current(0)  # Seleccionar la primera hora disponible
    except ValueError:
        pass  # Ignorar si la hora de inicio no es válida


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Selector de Fecha y Horas")
ventana.geometry("400x400")

# Crear un calendario
calendario = Calendar(ventana, selectmode="day", year=2025, month=1, day=27)
calendario.pack(pady=10)

# Crear Combobox para seleccionar horas de inicio y fin
label_inicio = tk.Label(ventana, text="Hora de inicio:")
label_inicio.pack(pady=5)
horas = [f"{i:02d}" for i in range(24)]  # Lista de horas en formato 24h
combo_inicio = ttk.Combobox(ventana, values=horas, state="readonly")
combo_inicio.current(0)  # Establecer la primera hora como valor predeterminado
combo_inicio.pack(pady=5)
combo_inicio.bind("<<ComboboxSelected>>", actualizar_horas_fin)  # Llamar a la función al cambiar la hora de inicio

label_fin = tk.Label(ventana, text="Hora de fin:")
label_fin.pack(pady=5)
combo_fin = ttk.Combobox(ventana, values=horas, state="readonly")
combo_fin.current(0)  # Establecer la primera hora como valor predeterminado
combo_fin.pack(pady=5)

# Botón para obtener la fecha y horas seleccionadas
boton_seleccionar = tk.Button(ventana, text="Seleccionar Fecha y Horas", command=obtener_fecha_y_horas)
boton_seleccionar.pack(pady=10)

ventana.mainloop()

print("Fecha seleccionada:", st_fecha)
print("Hora de inicio:", start_t)
print("Hora de fin:", end_t)