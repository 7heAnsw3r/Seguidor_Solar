import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Variables globales para almacenar la fecha y las horas
st_fecha = None
start_t = None
end_t = None

def obtener_fecha_y_horas(callback):
    global st_fecha, start_t, end_t, ventana  

    fecha_seleccionada = calendario.get_date()
    st_fecha = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%Y-%m-%d")

    hora_inicio = combo_inicio.get()
    hora_fin = combo_fin.get()

    try:
        start_t = datetime.strptime(hora_inicio, "%H").time()
        end_t = datetime.strptime(hora_fin, "%H").time()
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese las horas en formato HH")

    # Llamar al callback para actualizar la interfaz con los valores seleccionados
    if callback:
        callback(st_fecha, start_t.strftime("%H:%M"), end_t.strftime("%H:%M"))

    ventana.destroy()

def crear_ventana_datetime(callback):
    global ventana, calendario, combo_inicio, combo_fin, horas  
    ventana = tk.Toplevel()  # Asegura que ventana esté definida
    ventana.title("Seleccionar Parámetros")
    ventana.geometry("400x400")

    calendario = Calendar(ventana, selectmode="day", year=2025, month=1, day=27)
    calendario.pack(pady=10)

    label_inicio = tk.Label(ventana, text="Hora de inicio:")
    label_inicio.pack(pady=5)
    horas = [f"{i:02d}" for i in range(24)]
    combo_inicio = ttk.Combobox(ventana, values=horas, state="readonly")
    combo_inicio.current(0)
    combo_inicio.pack(pady=5)

    label_fin = tk.Label(ventana, text="Hora de fin:")
    label_fin.pack(pady=5)
    combo_fin = ttk.Combobox(ventana, values=horas, state="readonly")
    combo_fin.current(1)  
    combo_fin.pack(pady=5)

    boton_seleccionar = tk.Button(ventana, text="Seleccionar Fecha y Horas", 
                                  command=lambda: obtener_fecha_y_horas(callback))
    boton_seleccionar.pack(pady=10)
    ventana.mainloop()