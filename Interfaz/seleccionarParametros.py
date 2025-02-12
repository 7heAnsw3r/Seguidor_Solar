import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Variables globales para almacenar la fecha y las horas
st_fecha = None
start_t = None
end_t = None

def obtener_fecha_y_horas(callback):
    """
    Obtiene la fecha y las horas seleccionadas en la interfaz, las convierte al formato adecuado
    y llama al callback para actualizar la interfaz principal.

    Args:
        callback (function): Función que se ejecuta con la fecha y horas seleccionadas como parámetros.
    """
    global st_fecha, start_t, end_t, ventana  

    # Obtener la fecha seleccionada desde el calendario
    fecha_seleccionada = calendario.get_date()
    st_fecha = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y-%m-%d")

    # Obtener las horas de inicio y fin seleccionadas desde los comboboxes
    hora_inicio = combo_inicio.get()
    hora_fin = combo_fin.get()

    try:
        # Convertir las horas a formato de tiempo
        start_t = datetime.strptime(hora_inicio, "%H").time()
        end_t = datetime.strptime(hora_fin, "%H").time()
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese las horas en formato HH")

    # Llamar al callback para actualizar la interfaz con los valores seleccionados
    if callback:
        callback(st_fecha, start_t.strftime("%H:%M"), end_t.strftime("%H:%M"))

    # Cerrar la ventana de selección de fecha y horas
    ventana.destroy()

def actualizar_horas_fin(event=None):
    """
    Actualiza las opciones del combobox de hora fin para que solo muestre horas posteriores a la hora de inicio.

    Args:
        event (optional): Evento que dispara la actualización de las horas de fin.
    """
    hora_inicio = combo_inicio.get()
    try:
        # Buscar el índice de la hora de inicio seleccionada
        indice_inicio = horas.index(hora_inicio)
        # Mostrar solo las horas posteriores a la hora de inicio
        horas_fin = horas[indice_inicio + 1:]  # Tomar horas posteriores a la de inicio
        combo_fin['values'] = horas_fin
        combo_fin.current(0)  # Seleccionar la primera hora disponible
    except ValueError:
        pass  # Ignorar si la hora de inicio no es válida

def crear_ventana_datetime(callback):
    """
    Crea y muestra una ventana emergente para seleccionar una fecha y un rango de horas. 
    Luego llama al callback con la fecha y las horas seleccionadas.

    Args:
        callback (function): Función que se ejecuta con la fecha y horas seleccionadas como parámetros.
    """
    global ventana, calendario, combo_inicio, combo_fin, horas  
    
    # Crear la ventana emergente
    ventana = tk.Toplevel()  # Asegura que ventana esté definida
    ventana.title("Seleccionar Parámetros")
    ventana.geometry("400x400")

    # Crear un calendario para seleccionar la fecha
    calendario = Calendar(ventana, selectmode="day", year=2025, month=1, day=27)
    calendario.pack(pady=10)

    # Crear Combobox para seleccionar horas de inicio
    label_inicio = tk.Label(ventana, text="Hora de inicio:")
    label_inicio.pack(pady=5)
    horas = [f"{i:02d}" for i in range(24)]  # Lista de horas en formato 24h
    combo_inicio = ttk.Combobox(ventana, values=horas, state="readonly")
    combo_inicio.current(0)  # Establecer la primera hora como valor predeterminado
    combo_inicio.pack(pady=5)
    combo_inicio.bind("<<ComboboxSelected>>", actualizar_horas_fin)  # Llamar a la función al cambiar la hora de inicio

    # Crear Combobox para seleccionar horas de fin
    label_fin = tk.Label(ventana, text="Hora de fin:")
    label_fin.pack(pady=5)
    combo_fin = ttk.Combobox(ventana, values=horas, state="readonly")
    combo_fin.current(0)  # Establecer la primera hora como valor predeterminado
    combo_fin.pack(pady=5)

    # Botón para obtener la fecha y horas seleccionadas
    boton_seleccionar = tk.Button(ventana, text="Seleccionar Fecha y Horas", command=lambda: obtener_fecha_y_horas(callback))
    boton_seleccionar.pack(pady=10)
    
    # Ejecutar el mainloop de Tkinter para la ventana emergente
    ventana.mainloop()
