import tkinter as tk
from PIL import Image, ImageTk
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
    raiz.geometry("1200x600")
    raiz.configure(bg="#e6f2ff")  # Fondo azul claro
    raiz.iconbitmap("./Imagenes/panel-solar.ico")
    centrar_ventana(raiz)

    # Estilos
    style = ttk.Style()
    style.configure("TFrame", background="#e6f2ff")
    style.configure("TLabelFrame", background="#cce0ff", font=("Arial", 12, "bold"))
    style.configure("TButton", font=("Arial", 10, "bold"), background="#4da6ff", foreground="black")

     # Panel izquierdo
    left_panel = tk.Frame(raiz, bg="#ADD8E6", width=300)  # Fondo azul claro con borde
    left_panel.pack(side=tk.LEFT, fill=tk.Y, pady=10)

    # Título en el panel izquierdo
    title_label = tk.Label(left_panel, text="SIMULADOR DE UN \n SEGUIDOR SOLAR", bg="#ADD8E6", font=("Arial", 18, "bold"), fg="black")
    title_label.pack(pady=10)

    # Logo
    logo_path = r"C:\Users\User\Desktop\EPN\4. CUARTO SEMESTRE\1. METODOS NUMERICOS\4. PROYECTOS\Seguidor_Solar\Imagenes\panel-solar.png"
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((120, 120))  # Ajustar tamaño
    logo_img = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(left_panel, image=logo_img, bg="#ADD8E6")
    logo_label.image = logo_img  # Mantener referencia
    logo_label.pack(pady=40)

    # Botón de selección de parámetros
    boton_abrir_datetime = ttk.Button(left_panel, text="Selector de Parámetros", command=seleccionarFechas.crear_ventana_datetime, style="TButton")
    boton_abrir_datetime.pack(pady=10)

    # Botón de generación de reporte
    report_button = ttk.Button(left_panel, text="Generar Reporte", style="TButton") 
    report_button.pack(pady=10)

    # --- Main Content Area --- 
    main_area = tk.Frame(raiz, bg="white")  # White background
    main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    raiz.mainloop()

bienvenida.mainloop()
