import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Interfaz.calculoAngulos import getSolarPosition, Rxyz

def visualizar_trayectoria_panel_y_sol(frame_padre, tiempos, azimuts, elevaciones, beta, phi):
    """
    Renderiza la simulación de la trayectoria del panel solar y la trayectoria del sol 
    dentro de un frame de Tkinter en la interfaz principal.

    Args:
        frame_padre (tk.Frame): El frame de Tkinter donde se incrustará el gráfico 3D.
        tiempos (list): Lista de tiempos de la simulación.
        azimuts (list): Lista de ángulos de azimut a lo largo del tiempo.
        elevaciones (list): Lista de ángulos de elevación a lo largo del tiempo.
        beta (list): Lista de ángulos de pitch (inclinación) a lo largo del tiempo.
        phi (list): Lista de ángulos de roll (balanceo) a lo largo del tiempo.
    """
    
    # Limpiar cualquier contenido previo en el frame
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Crear marco para el gráfico 3D dentro del frame
    marco_3d = tk.Frame(frame_padre)
    marco_3d.pack(fill=tk.BOTH, expand=True)

    # Crear figura y ejes 3D
    figura = plt.Figure(figsize=(10, 7), dpi=100)
    ejes = figura.add_subplot(111, projection='3d')

    # Definir el centro del panel solar y sus dimensiones
    centro_panel = [0, 0, 0]
    ancho, alto = 4, 2
    sun_trajectory = {'x': [], 'y': [], 'z': []}

    def construir_panel(centro, ancho, alto):
        """
        Construye un panel rectangular con las dimensiones proporcionadas.

        Args:
            centro (list): Coordenadas [x, y, z] del centro del panel.
            ancho (float): Ancho del panel.
            alto (float): Alto del panel.

        Returns:
            np.array: Vértices del panel en 3D.
        """
        w, h = ancho / 2, alto / 2
        return np.array([
            [centro[0] - w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] + h, centro[2]],
            [centro[0] - w, centro[1] + h, centro[2]]
        ])

    def create_sun(ax, center, radius=1.0, color='orange'):
        """
        Crea una esfera representando el sol en la gráfica 3D.

        Args:
            ax (Axes3D): El objeto de los ejes 3D donde se graficará el sol.
            center (list): Coordenadas [x, y, z] del centro del sol.
            radius (float): Radio de la esfera (por defecto 1.0).
            color (str): Color de la esfera (por defecto 'orange').
        """
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        ax.plot_surface(x, y, z, color=color, shade=True, rstride=3, cstride=3, linewidth=0)

    # Construir el panel y añadirlo a los ejes
    vertices = construir_panel(centro_panel, ancho, alto)
    panel = Poly3DCollection([vertices], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black')
    ejes.add_collection3d(panel)

    # Ajuste de límites y dirección Este
    ejes.set_xlim(-10, 10)
    ejes.set_ylim(-10, 10)
    ejes.set_zlim(-10, 10)
    ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
    ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

    def aplicar_rotaciones(vertices, angulo_pitch, angulo_roll, angulo_yaw=0):
        """
        Aplica las rotaciones al panel solar basado en los ángulos de control.

        Args:
            vertices (np.array): Vértices del panel.
            angulo_pitch (float): Ángulo de pitch (inclinación).
            angulo_roll (float): Ángulo de roll (balanceo).
            angulo_yaw (float): Ángulo de yaw (giro horizontal).

        Returns:
            np.array: Vértices rotados del panel.
        """
        rotacion_combinada = Rxyz(angulo_roll, angulo_pitch, angulo_yaw)
        return vertices @ rotacion_combinada.T

    def actualizar_animacion(fotograma):
        """
        Actualiza la animación del panel solar y la trayectoria del sol.

        Args:
            fotograma (int): Índice del fotograma actual.

        Returns:
            list: Lista de objetos del panel (en este caso, solo el panel).
        """
        if fotograma < len(tiempos):
            ejes.clear()
            vertices_rotados = aplicar_rotaciones(vertices, beta[fotograma], phi[fotograma])
            panel = Poly3DCollection([vertices_rotados], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black')
            ejes.add_collection3d(panel)

            azimuth, elevation = azimuts[fotograma], elevaciones[fotograma]
            sun_size = 1.0 + (elevation / 90) * 0.5  
            r = 10  
            sun_position = [
                r * np.cos(np.radians(elevation)) * np.sin(np.radians(azimuth)),
                r * np.cos(np.radians(elevation)) * np.cos(np.radians(azimuth)),
                r * np.sin(np.radians(elevation))
            ]

            sun_trajectory['x'].append(sun_position[0])
            sun_trajectory['y'].append(sun_position[1])
            sun_trajectory['z'].append(sun_position[2])

            ejes.plot(sun_trajectory['x'], sun_trajectory['y'], sun_trajectory['z'], color='yellow', linewidth=2, linestyle='-')
            create_sun(ejes, sun_position, radius=sun_size)

            # Ajustes de límites y dirección Este
            ejes.set_xlim(-10, 10)
            ejes.set_ylim(-10, 10)
            ejes.set_zlim(-10, 10)
            ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
            ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

            # Agregar la etiqueta de tiempo dentro del gráfico
            ejes.text2D(0.05,0.05, tiempos[fotograma].strftime("Hora: %H:%M\nFecha: %Y-%m-%d"), 
                        transform=figura.transFigure, fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))

        return [panel]

    # Crear canvas y animación
    canvas = FigureCanvasTkAgg(figura, master=marco_3d)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    animacion = animation.FuncAnimation(figura, actualizar_animacion, frames=len(tiempos), interval=200, blit=False)
    
    # Actualizar el frame de Tkinter
    frame_padre.update_idletasks()
