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

# Crear la ventana de bienvenida
bienvenida = tk.Tk()
bienvenida.title("Seguidor Solar")
bienvenida.geometry("500x250")
bienvenida.configure(bg="#e6f2ff")
bienvenida.iconbitmap("./Imagenes/panel-solar.ico")
centrar_ventana(bienvenida)

# Etiqueta de bienvenida
mensaje_bienvenida = ttk.Label(bienvenida, text="¡Bienvenido al simulador de un Seguidor Solar!", font=("Arial", 14, "bold"), foreground="#004080", background="#e6f2ff")
mensaje_bienvenida.pack(pady=25)

# Descripción del sistema
mensaje_descripcion = ttk.Label(bienvenida, text="Visualiza y analiza el movimiento de un seguidor solar de 2 grados de libertad.", font=("Arial", 12), background="#e6f2ff", wraplength=350, justify="center")
mensaje_descripcion.pack(pady=35)

# Botón para continuar
def abrir_principal():
    bienvenida.destroy()
    abrir_interfaz_principal()

boton_continuar = ttk.Button(bienvenida, text="Iniciar Simulación", command=abrir_principal)
boton_continuar.pack()

# Función para abrir la ventana principal
def abrir_interfaz_principal():
    raiz = tk.Tk()
    raiz.title("Seguidor Solar")
    raiz.geometry("600x500")
    raiz.configure(bg="#e6f2ff")  # Fondo azul claro
    raiz.iconbitmap("./Imagenes/panel-solar.ico")
    centrar_ventana(raiz)

    # Estilos
    style = ttk.Style()
    style.configure("TFrame", background="#e6f2ff")
    style.configure("TLabelFrame", background="#cce0ff", font=("Arial", 12, "bold"))
    style.configure("TButton", font=("Arial", 10, "bold"), background="#4da6ff", foreground="white")

    # Frame para datetime_picker
    datetime_frame = ttk.LabelFrame(raiz, text="Selección de Fecha y Hora", padding=10)
    datetime_frame.pack(padx=10, pady=10, fill='x')

    # Botón para abrir el datetime_picker
    boton_abrir_datetime = ttk.Button(datetime_frame, text="Seleccionar Fecha y Hora", 
                                    command=seleccionarFechas.crear_ventana_datetime)
    boton_abrir_datetime.pack(pady=10)

    # Frame principal
    miFrame = ttk.Frame(raiz, padding=20)
    miFrame.pack(pady=20)

    raiz.mainloop()

bienvenida.mainloop()
