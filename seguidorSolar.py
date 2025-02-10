"""
Módulo para la interfaz gráfica del simulador de seguidor solar.

Este módulo implementa una interfaz gráfica utilizando `tkinter` para 
permitir la selección de parámetros, ejecución de simulaciones y generación de reportes.
"""

import tkinter as tk
from PIL import Image, ImageTk
from functools import partial
from datetime import datetime
from Interfaz.seleccionarParametros import crear_ventana_datetime
from Interfaz.generarReporte import generar_reporte

# Variables globales para almacenar referencias a los elementos de la interfaz
label_fecha = None
label_inicio = None
label_fin = None
boton_iniciar = None
boton_icono = None


def centrar_ventana(ventana):
    """
    Centra la ventana en la pantalla.

    Args:
        ventana (tk.Tk or tk.Toplevel): Ventana de Tkinter a centrar.
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
    """
    Crea un botón con un icono.

    Args:
        parent (tk.Widget): Widget padre donde se ubicará el botón.
        ruta_icono (str): Ruta del archivo de imagen del icono.
        comando (function): Función a ejecutar cuando se presione el botón.

    Returns:
        tk.Button or None: Retorna el botón creado o None si no se encontró el icono.
    """
    try:
        icono = Image.open(ruta_icono).resize((40, 40), Image.Resampling.LANCZOS)  # Ajustar tamaño
        icono = ImageTk.PhotoImage(icono)
    except FileNotFoundError:
        print(f"Error: No se encontró el icono en {ruta_icono}")
        return None

    boton = tk.Button(parent, image=icono, command=comando, borderwidth=0, cursor="hand2", bg="#e4e4e4")
    boton.image = icono  # Guardar referencia para evitar que se borre

    return boton


def actualizar_parametros(fecha, hora_inicio, hora_fin):
    """
    Actualiza los valores seleccionados en la interfaz.

    Args:
        fecha (str): Fecha seleccionada en formato YYYY-MM-DD.
        hora_inicio (str): Hora de inicio seleccionada en formato HH:MM.
        hora_fin (str): Hora de fin seleccionada en formato HH:MM.
    """
    if label_fecha:
        label_fecha.config(text=f"Fecha: {fecha}")
    if label_inicio:
        label_inicio.config(text=f"Hora de inicio: {hora_inicio}")
    if label_fin:
        label_fin.config(text=f"Hora de fin: {hora_fin}")
    
    boton_iniciar.pack(pady=10)
    boton_icono.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)


def reporte():
    """
    Genera y guarda un reporte con los parámetros seleccionados.
    """
    if label_fecha and label_inicio and label_fin:
        fecha_str = label_fecha.cget("text").replace("Fecha: ", "")
        inicio_str = label_inicio.cget("text").replace("Hora de inicio: ", "")
        fin_str = label_fin.cget("text").replace("Hora de fin: ", "")

        # Convertir fecha a tipo `datetime.date`
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"⚠️ Error: Formato de fecha inválido ({fecha_str}).")
            return

        # Convertir horas a enteros
        try:
            inicio = int(inicio_str.split(":")[0])  # Tomar solo la hora
            fin = int(fin_str.split(":")[0])
        except ValueError:
            print(f"⚠️ Error: Formato de hora inválido ({inicio_str}, {fin_str}).")
            return

        # Generar el reporte
        reporte_texto = generar_reporte(fecha, inicio, fin)

        # Guardar el reporte en un archivo de texto
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
mensaje_descripcion = tk.Label(
    bienvenida, 
    text="Visualiza y analiza el movimiento de un seguidor solar de 2 grados de libertad.", 
    font=("Helvetica", 12, "italic"), 
    background="#f7faf9", 
    wraplength=350, 
    justify="center"
)
mensaje_descripcion.pack(pady=20)


# Botón para continuar
def abrir_principal():
    """
    Cierra la ventana de bienvenida y abre la interfaz principal.
    """
    bienvenida.destroy()
    abrir_interfaz_principal()


boton_continuar = tk.Button(
    bienvenida, text="Iniciar Simulación", command=abrir_principal, 
    font=("Arial", 12, "bold"), bg="#ffc133", fg="black", padx=10, pady=5, cursor="hand2"
)
boton_continuar.pack(pady=10)


def abrir_interfaz_principal():
    """
    Crea y muestra la interfaz principal del simulador de seguidor solar.
    """
    global label_fecha, label_inicio, label_fin, boton_iniciar, boton_icono

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
    titulo_panel = tk.Frame(left_panel, bg="#4A4A4A")
    titulo_panel.pack(side="top", fill="x")  
    titulo = tk.Label(
        titulo_panel, text="SIMULADOR DE UN\nSEGUIDOR SOLAR", 
        font=("Helvetica", 20, "bold"), foreground="#FFFFFF", background="#4A4A4A"
    )
    titulo.pack(pady=20, anchor="n")

    # Botón de selección de parámetros
    boton_abrir_datetime = tk.Button(
        left_panel, text="Selector de Parámetros", 
        command=partial(crear_ventana_datetime, actualizar_parametros), 
        font=("Arial", 12, "bold"), bg="#ffc133", fg="black", padx=10, pady=5, cursor="hand2"
    )
    boton_abrir_datetime.pack(pady=10)

    # Labels para mostrar los valores seleccionados
    label_fecha = tk.Label(left_panel, text="Fecha: --", font=("Arial", 10), bg="#FFFFFF")
    label_fecha.pack(pady=5)

    label_inicio = tk.Label(left_panel, text="Hora de inicio: --", font=("Arial", 10), bg="#FFFFFF")
    label_inicio.pack(pady=5)

    label_fin = tk.Label(left_panel, text="Hora de fin: --", font=("Arial", 10), bg="#FFFFFF")
    label_fin.pack(pady=5)

    raiz.mainloop()


bienvenida.mainloop()
