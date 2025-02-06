import tkinter as tk
from tkinter import ttk
from Interfaz import seleccionarFechas

def centrar_ventana(ventana):
    """
    Centra la ventana en la pantalla.
    """
    ventana.update()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2

    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# Crear la ventana principal
raiz = tk.Tk()
raiz.title("Seguidor Solar")
raiz.geometry("600x500")
raiz.iconbitmap("./Imagenes/panel-solar.ico")
centrar_ventana(raiz)

# Frame para datetime_picker
datetime_frame = ttk.LabelFrame(raiz, text="Selección de Fecha y Hora")
datetime_frame.pack(padx=10, pady=10, fill='x')

# Botón para abrir el datetime_picker
boton_abrir_datetime = ttk.Button(datetime_frame, text="Seleccionar Fecha y Hora",
                                 command=seleccionarFechas.crear_ventana_datetime)
boton_abrir_datetime.pack(pady=10)

# Resto de la interfaz (miFrame, miLabel, etc.)
miFrame = tk.Frame(raiz, width=500, height=600)
miFrame.pack()
miLabel = tk.Label(miFrame, text="Hola Mundo")
miLabel.place(x=100, y=100)

raiz.mainloop()