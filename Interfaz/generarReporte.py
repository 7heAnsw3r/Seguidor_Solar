"""
Módulo para la generación de reportes en formato PDF.

Este módulo genera reportes con gráficos que representan el azimut, elevación,
pitch y roll del seguidor solar. Los gráficos se guardan temporalmente y se 
insertan en un archivo PDF. Luego, el PDF se guarda en el escritorio con un 
nombre incremental.
"""

import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import io
from PIL import Image
from Interfaz.calculoAngulos import getSolarPosition
import tkinter as tk
from tkinter import messagebox
import webbrowser


def generar_reporte(fecha, hora_inicio, hora_fin):
    """
    Genera un reporte en formato PDF con gráficos del seguidor solar.

    Args:
        fecha (datetime.date): Fecha seleccionada para la simulación.
        hora_inicio (int): Hora de inicio del cálculo.
        hora_fin (int): Hora de fin del cálculo.

    Returns:
        str: Mensaje indicando el nombre del archivo PDF generado.
    """
    # Obtener datos de posición solar
    times, azimuths, elevations, beta, alpha = getSolarPosition(
        start_date=fecha, start_hour=hora_inicio, end_hour=hora_fin
    )

    # --- Generar la primera gráfica (Azimut y Elevación) ---
    plt.figure(figsize=(10, 5))
    plt.plot(times, azimuths, label="Azimut", marker="o")
    plt.plot(times, elevations, label="Elevación", marker="s")
    plt.xlabel("Tiempo")
    plt.ylabel("Ángulo (°)")
    plt.title("Azimut y Elevación a lo largo del tiempo")
    plt.legend()
    plt.xticks(rotation=45)

    # Guardar la imagen temporalmente
    img_path1 = "grafico_azimut_elevacion.png"
    plt.savefig(img_path1, format='png')
    plt.close()

    # --- Generar la segunda gráfica (Pitch y Roll) ---
    plt.figure(figsize=(10, 5))
    plt.plot(times, beta, label="Beta (Pitch)", marker="o", color="r")
    plt.plot(times, alpha, label="Alpha (Roll)", marker="s", color="g")
    plt.xlabel("Tiempo")
    plt.ylabel("Ángulo (°)")
    plt.title("Pitch y Roll a lo largo del tiempo")
    plt.legend()
    plt.xticks(rotation=45)

    # Guardar la imagen temporalmente
    img_path2 = "grafico_alpha_beta.png"
    plt.savefig(img_path2, format='png')
    plt.close()

    # Obtener la ruta del escritorio del usuario
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Determinar un nombre único para el archivo PDF
    report_files = [f for f in os.listdir(desktop_path) if f.startswith("Informe_") and f.endswith(".pdf")]
    report_numbers = [int(f.split("_")[1].split(".")[0]) for f in report_files]

    if not report_numbers:
        report_number = 1
    else:
        report_number = max(report_numbers) + 1  # Asignar número incremental

    pdf_filename = f"Informe_{report_number}.pdf"
    pdf_path = os.path.join(desktop_path, pdf_filename)

    # --- Crear el PDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Reporte del Seguidor Solar", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Fecha: {fecha.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, f"Hora de Inicio: {hora_inicio}:00", ln=True)
    pdf.cell(200, 10, f"Hora de Fin: {hora_fin}:00", ln=True)

    pdf.ln(10)

    # Insertar la primera imagen
    pdf.image(img_path1, x=10, w=180)

    pdf.ln(10)

    # Insertar la segunda imagen
    pdf.image(img_path2, x=10, w=180)

    # Guardar el archivo PDF en el escritorio
    pdf.output(pdf_path)
    print(f"✅ Reporte generado exitosamente: {pdf_filename}")

    # Eliminar las imágenes temporales
    os.remove(img_path1)
    os.remove(img_path2)

    # --- Mostrar ventana emergente con opciones para el usuario ---
    def open_pdf():
        """Abre el archivo PDF generado en el navegador predeterminado."""
        webbrowser.open(pdf_path)

    def show_popup():
        """Muestra una ventana emergente informando sobre la generación del PDF."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal

        popup = tk.Toplevel(root)
        popup.title("Reporte Generado")

        # Centrar la ventana emergente en la pantalla
        window_width = 400
        window_height = 100
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Etiqueta con el mensaje
        label = tk.Label(popup, text=f"Reporte generado como {pdf_filename}")
        label.pack(pady=10)

        # Frame para centrar los botones
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        # Botón para abrir el PDF
        open_button = tk.Button(button_frame, text="Abrir PDF", command=open_pdf)
        open_button.pack(side="left", padx=10)

        # Botón para cerrar
        accept_button = tk.Button(button_frame, text="Cerrar", command=popup.destroy)
        accept_button.pack(side="left", padx=10)

        popup.mainloop()

    # Mostrar la ventana emergente con opciones
    show_popup()

    return f"Reporte PDF guardado como {pdf_filename} en el escritorio."
