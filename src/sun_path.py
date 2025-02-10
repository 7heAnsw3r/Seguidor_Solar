"""
Módulo para la visualización de la trayectoria del sol en 3D.

Este módulo utiliza `matplotlib` y `tkinter` para representar la trayectoria
del sol a lo largo del tiempo. Incluye funciones para configurar los ejes,
crear una representación del sol y animar su movimiento en un gráfico 3D.
"""

import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def configure_axes(ax, title, xlabel=None, ylabel=None, zlabel=None):
    """
    Configura los ejes de un gráfico 3D.

    Args:
        ax (matplotlib.Axes3D): Eje 3D a configurar.
        title (str): Título del gráfico.
        xlabel (str, opcional): Etiqueta para el eje X.
        ylabel (str, opcional): Etiqueta para el eje Y.
        zlabel (str, opcional): Etiqueta para el eje Z.
    """
    ax.set_title(title, fontsize=16)
    if xlabel: ax.set_xlabel(xlabel, fontsize=12)
    if ylabel: ax.set_ylabel(ylabel, fontsize=12)
    if zlabel: ax.set_zlabel(zlabel, fontsize=12)


def create_sun(ax, center, radius=1.0, color='orange'):
    """
    Crea una representación esférica del sol en un gráfico 3D.

    Args:
        ax (matplotlib.Axes3D): Eje 3D donde se dibujará el sol.
        center (list): Coordenadas [x, y, z] del centro del sol.
        radius (float, opcional): Radio de la esfera solar (por defecto 1.0).
        color (str, opcional): Color de la esfera (por defecto 'orange').
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
    ax.plot_surface(x, y, z, color=color, shade=True, rstride=2, cstride=2, linewidth=0)


def graph_trayectoria_3d(times, azimuths, elevations):
    """
    Genera una animación en 3D de la trayectoria solar a lo largo del tiempo.

    Args:
        times (list): Lista de tiempos de simulación.
        azimuths (list): Lista de ángulos azimutales del sol.
        elevations (list): Lista de ángulos de elevación solar.
    """
    time_numbers = np.arange(len(times))

    # Crear la ventana de Tkinter
    root = tk.Tk()
    root.geometry("1200x800")  # Ajuste de tamaño para mejor visibilidad
    frame_3d = tk.Frame(root)
    frame_3d.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Configurar la figura 3D con matplotlib
    fig3 = plt.Figure(figsize=(25, 20), dpi=100)
    ax3 = fig3.add_subplot(111, projection='3d')
    configure_axes(ax3, "Solar Trajectory", "Time", "Azimuth", "Elevation")
    ax3.set_xlim(0, len(times) - 1)
    ax3.set_ylim(min(azimuths) - 5, max(azimuths) + 5)
    ax3.set_zlim(min(elevations) - 5, max(elevations) + 5)

    # Dibujar la trayectoria del sol en el gráfico
    ax3.plot(time_numbers, azimuths, elevations, 'y-', alpha=0.3)  # Línea de trayectoria con transparencia

    def update_3d(frame):
        """
        Actualiza la animación en cada fotograma para reflejar el movimiento del sol.

        Args:
            frame (int): Índice del fotograma actual en la simulación.
        """
        ax3.clear()  # Limpiar solo el sol, no la trayectoria
        configure_axes(ax3, "Solar Trajectory", "Time", "Azimuth", "Elevation")
        ax3.set_xlim(0, len(times) - 1)
        ax3.set_ylim(min(azimuths) - 5, max(azimuths) + 5)
        ax3.set_zlim(min(elevations) - 5, max(elevations) + 5)

        # Re-dibujar la trayectoria con menor opacidad
        ax3.plot(time_numbers, azimuths, elevations, 'y-', alpha=0.3)

        # Dibujar el sol en la posición actual del fotograma
        sun_radius = 1.0
        create_sun(ax3, [time_numbers[frame], azimuths[frame], elevations[frame]], radius=sun_radius)

        # Agregar la etiqueta de tiempo en la animación
        tiempo_actual = times[frame].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d")
        ax3.text2D(0.05, 0.95, tiempo_actual, transform=ax3.transAxes, color='black', fontsize=12)
        return []

    # Integrar la figura 3D en la interfaz Tkinter
    canvas3 = FigureCanvasTkAgg(fig3, master=frame_3d)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Configurar la animación de la trayectoria solar
    ani3 = animation.FuncAnimation(fig3, update_3d, frames=len(times), interval=500, blit=False)

    # Iniciar la ventana de Tkinter
    root.mainloop()
