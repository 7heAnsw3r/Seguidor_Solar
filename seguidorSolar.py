import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from datetime import datetime
from Interfaz.seleccionarParametros import crear_ventana_datetime
from Interfaz.generarReporte import generar_reporte
from Interfaz.calculoAngulos import getSolarPosition
from Interfaz.posicionSistema import visualizar_trayectoria_panel_y_sol

label_fecha = None
label_inicio = None
label_fin = None
boton_iniciar = None
botton_icono = None
main_area = None

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

def crear_boton_icono(parent, ruta_icono, comando):
    """Crea un botón con un icono."""
    try:
        icono = Image.open(ruta_icono).resize((40, 40), Image.Resampling.LANCZOS)  # Ajusta tamaño
        icono = ImageTk.PhotoImage(icono)
    except FileNotFoundError:
        print(f"Error: No se encontró el icono en {ruta_icono}")
        return None

    boton = tk.Button(parent, image=icono, command=comando, borderwidth=0, cursor="hand2", bg="#e4e4e4")
    boton.image = icono  # Guardar referencia para evitar que se borre

    return boton

def actualizar_parametros(fecha, hora_inicio, hora_fin):
    """Actualiza los valores seleccionados en la interfaz."""
    if label_fecha:
        label_fecha.config(text=f"Fecha: {fecha}")
    if label_inicio:
        label_inicio.config(text=f"Hora de inicio: {hora_inicio}")
    if label_fin:
        label_fin.config(text=f"Hora de fin: {hora_fin}")
    boton_iniciar.pack(pady=10)
    boton_icono.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)


def simulacion():
    times, azimuths, elevations, beta, alpha = getSolarPosition(
            label_fecha.cget("text"),
            label_inicio.cget("text"),
            label_fin.cget("text")
        )
    
    phi = alpha

    visualizar_trayectoria_panel_y_sol(times, azimuths, elevations, beta, phi)


def reporte():
    """Genera y guarda un reporte con los parámetros seleccionados."""
    if label_fecha and label_inicio and label_fin:
        fecha_str = label_fecha.cget("text").replace("Fecha: ", "")
        inicio_str = label_inicio.cget("text").replace("Hora de inicio: ", "")
        fin_str = label_fin.cget("text").replace("Hora de fin: ", "")

        # Convertir fecha a tipo `datetime.date`
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()  # Ajusta el formato si es necesario
        except ValueError:
            print(f"⚠️ Error: Formato de fecha inválido ({fecha_str}).")
            return

        # Convertir horas a enteros
        try:
            inicio = int(inicio_str.split(":")[0])  # Tomamos solo la hora
            fin = int(fin_str.split(":")[0])
        except ValueError:
            print(f"⚠️ Error: Formato de hora inválido ({inicio_str}, {fin_str}).")
            return

        # Llamar a la función que genera el reporte, ahora con las variables correctas
        reporte_texto = generar_reporte(fecha, inicio, fin)  # Aquí pasas las variables correctas

        # Guardar el reporte en un archivo
        ruta_reporte = f"Reporte_Solar_{fecha_str.replace('/', '-')}.txt"
        with open(ruta_reporte, "w", encoding="utf-8") as file:
            file.write(reporte_texto)

        print(f"✅ Reporte generado: {ruta_reporte}")

# Crear la ventana de bienvenida
bienvenida = tk.Tk()
bienvenida.title("Seguidor Solar")
bienvenida.geometry("500x250")
bienvenida.configure(bg="#f7faf9")
bienvenida.iconbitmap("./Imagenes/panel-solar.ico")
centrar_ventana(bienvenida)

# Panel superior para el mensaje de bienvenida
panel_superior = tk.Frame(bienvenida, bg="#4A4A4A", height=60)
panel_superior.pack(fill="x")

# Etiqueta de bienvenida
mensaje_bienvenida = tk.Label(panel_superior, text="¡Bienvenido al simulador de un \nSeguidor Solar!", 
                              font=("Helvetica", 20, "bold"), foreground="#FFFFFF", background="#4A4A4A")
mensaje_bienvenida.pack(pady=15)

# Descripción del sistema
mensaje_descripcion = tk.Label(bienvenida, text="Visualiza y analiza el movimiento de un seguidor solar de 2 grados de libertad.", font=("Helvetica", 12, "italic"), background="#f7faf9", wraplength=350, justify="center")
mensaje_descripcion.pack(pady=20)

# Botón para continuar
def abrir_principal():
    bienvenida.destroy()
    abrir_interfaz_principal()

boton_continuar = tk.Button(bienvenida, text="Iniciar Simulación", command=abrir_principal, font=("Arial", 12, "bold"), bg="#ffc133", fg="black", padx=10, pady=5, cursor="hand2")
boton_continuar.pack(pady=10)

# Función para abrir la ventana principal
def abrir_interfaz_principal():
    global label_fecha, label_inicio, label_fin, boton_iniciar, boton_icono, main_area

    raiz = tk.Tk()
    raiz.resizable(False, False)
    raiz.title("Seguidor Solar")
    raiz.geometry("1200x600")
    raiz.iconbitmap("./Imagenes/panel-solar.ico")
    centrar_ventana(raiz)

    # Panel izquierdo
    left_panel = tk.Frame(raiz, bg="#FFFFFF", width=300, height=600)
    left_panel.pack(side="left")
    left_panel.pack_propagate(False) 

    # Título en el panel izquierdo
    titulo_panel = tk.Frame(left_panel, bg="#4A4A4A")  # Puedes ajustar el color de fondo
    titulo_panel.pack(side="top", fill="x")  # Se expandirá horizontalmente
    titulo = tk.Label(titulo_panel, text="SIMULADOR DE UN\nSEGUIDOR SOLAR", font=("Helvetica", 20, "bold"), foreground="#FFFFFF", background="#4A4A4A")
    titulo.pack(pady=20, anchor="n")

    # Logo
    logo_path = r"./Imagenes/panel-solar.png"
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((120, 120))  # Ajustar tamaño
    logo_img = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(left_panel, image=logo_img, bg="#FFFFFF")
    logo_label.image = logo_img  # Mantener referencia
    logo_label.pack(pady=40)

    # Botón de selección de parámetros
    boton_abrir_datetime = tk.Button(left_panel, text="Selector de Parámetros", 
                                 command=partial(crear_ventana_datetime, actualizar_parametros), 
                                 font=("Arial", 12, "bold"), bg="#ffc133", fg="black", padx=10, pady=5, cursor="hand2")
    boton_abrir_datetime.pack(pady=10)

    # Labels para mostrar los valores seleccionados
    label_fecha = tk.Label(left_panel, text="Fecha: --", font=("Arial", 10), bg="#FFFFFF")
    label_fecha.pack(pady=5)

    label_inicio = tk.Label(left_panel, text="Hora de inicio: --", font=("Arial", 10), bg="#FFFFFF")
    label_inicio.pack(pady=5)

    label_fin = tk.Label(left_panel, text="Hora de fin: --", font=("Arial", 10), bg="#FFFFFF")
    label_fin.pack(pady=5)

    # Botón de inio de simulación
    boton_iniciar = tk.Button(left_panel, text="Iniciar Simulación!", 
                          font=("Arial", 12, "bold"), bg="#ffc133", 
                          fg="black", padx=10, pady=5, cursor="hand2", 
                          command=simulacion) 
    boton_iniciar.pack(pady=10)
    boton_iniciar.pack_forget()

    # --- Main Content Area --- 
    main_area = tk.Frame(raiz, width=900, height=600, bd=0, relief="solid",highlightbackground="#4A4A4A", highlightcolor="#4A4A4A", highlightthickness=3, bg="#e4e4e4")
    main_area.pack(side="right")
    main_area.pack_propagate(False) 

    # Botón de generación de reporte
    ruta_icono = r"./Imagenes/imprimir.ico"
    boton_icono = crear_boton_icono(main_area, ruta_icono, reporte)
    boton_icono.place_forget()

    raiz.mainloop()
bienvenida.mainloop()
