"""
Módulo para la selección de fecha y horas en la interfaz gráfica.

Este módulo permite a los usuarios seleccionar una fecha y un rango de horas
utilizando `tkinter` y `tkcalendar`. Los valores seleccionados se almacenan 
en variables globales y pueden ser utilizados en otras partes del programa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

# Variables globales para almacenar la fecha y las horas seleccionadas
st_fecha = None
start_t = None
end_t = None


def obtener_fecha_y_horas():
    """
    Obtiene la fecha y las horas seleccionadas por el usuario y las almacena en variables globales.
    """
    global st_fecha, start_t, end_t

    # Obtener la fecha seleccionada del calendario
    fecha_seleccionada = calendario.get_date()
    st_fecha = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y-%m-%d")

    # Obtener las horas de inicio y fin seleccionadas en los comboboxes
    hora_inicio = combo_inicio.get()
    hora_fin = combo_fin.get()

    try:
        # Convertir las horas a formato `time`
        start_t = datetime.strptime(hora_inicio, "%H").time()
        end_t = datetime.strptime(hora_fin, "%H").time()
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese las horas en formato HH:MM")

    # Cerrar la ventana principal (opcional)
    ventana.destroy()


def actualizar_horas_fin(event=None):
    """
    Actualiza las opciones del combobox de hora fin para que solo muestre horas posteriores a la hora de inicio.

    Args:
        event (tk.Event, opcional): Evento de cambio en el combobox de hora de inicio.
    """
    hora_inicio = combo_inicio.get()
    try:
        # Obtener el índice de la hora de inicio en la lista de horas
        indice_inicio = horas.index(hora_inicio)

        # Filtrar solo las horas posteriores a la de inicio
        horas_fin = horas[indice_inicio + 1:]
        combo_fin['values'] = horas_fin
        combo_fin.current(0)  # Seleccionar la primera hora disponible
    except ValueError:
        pass  # Ignorar si la hora de inicio no es válida


# --- Creación de la Ventana de Selección ---
ventana = tk.Tk()
ventana.title("Selector de Fecha y Horas")
ventana.geometry("400x400")

# Crear un calendario para seleccionar la fecha
calendario = Calendar(ventana, selectmode="day", year=2025, month=1, day=27)
calendario.pack(pady=10)

# --- Crear Combobox para seleccionar horas de inicio y fin ---
label_inicio = tk.Label(ventana, text="Hora de inicio:")
label_inicio.pack(pady=5)

# Lista de horas en formato 24 horas
horas = [f"{i:02d}" for i in range(24)]
combo_inicio = ttk.Combobox(ventana, values=horas, state="readonly")
combo_inicio.current(0)  # Seleccionar la primera hora por defecto
combo_inicio.pack(pady=5)

# Asociar el evento de actualización de horas de fin al cambiar la hora de inicio
combo_inicio.bind("<<ComboboxSelected>>", actualizar_horas_fin)

label_fin = tk.Label(ventana, text="Hora de fin:")
label_fin.pack(pady=5)

combo_fin = ttk.Combobox(ventana, values=horas, state="readonly")
combo_fin.current(0)  # Seleccionar la primera hora por defecto
combo_fin.pack(pady=5)

# Botón para confirmar la selección de fecha y horas
boton_seleccionar = tk.Button(ventana, text="Seleccionar Fecha y Horas", command=obtener_fecha_y_horas)
boton_seleccionar.pack(pady=10)

# Iniciar el bucle de la ventana para la interacción del usuario
ventana.mainloop()

# Imprimir los valores seleccionados en la consola (para depuración)
print("Fecha seleccionada:", st_fecha)
print("Hora de inicio:", start_t)
print("Hora de fin:", end_t)
