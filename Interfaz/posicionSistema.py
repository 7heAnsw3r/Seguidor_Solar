import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Interfaz.calculoAngulos import getSolarPosition, Rxyz

def visualizar_trayectoria_panel_y_sol(frame_padre, tiempos, azimuts, elevaciones, beta, phi):
    """Renderiza la simulación dentro de un frame de Tkinter en la interfaz principal."""
    
    # Limpiar cualquier contenido previo en el frame
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Marco para el gráfico 3D dentro del frame
    marco_3d = tk.Frame(frame_padre)
    marco_3d.pack(fill=tk.BOTH, expand=True)

    # Etiqueta para mostrar la hora dentro del área principal
    etiqueta_hora = tk.Label(frame_padre, text="", font=("Arial", 14))
    etiqueta_hora.pack(pady=5)

    figura = plt.Figure(figsize=(10, 7), dpi=100)
    ejes = figura.add_subplot(111, projection='3d')

    centro_panel = [0, 0, 0]
    ancho, alto = 4, 2
    sun_trajectory = {'x': [], 'y': [], 'z': []}

    def construir_panel(centro, ancho, alto):
        w, h = ancho / 2, alto / 2
        return np.array([
            [centro[0] - w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] + h, centro[2]],
            [centro[0] - w, centro[1] + h, centro[2]]
        ])

    def create_sun(ax, center, radius=1.0, color='orange'):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        ax.plot_surface(x, y, z, color=color, shade=True, rstride=3, cstride=3, linewidth=0)

    vertices = construir_panel(centro_panel, ancho, alto)
    panel = Poly3DCollection([vertices], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black')
    ejes.add_collection3d(panel)

    ejes.set_xlim(-10, 10)
    ejes.set_ylim(-10, 10)
    ejes.set_zlim(-10, 10)
    ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
    ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

    def aplicar_rotaciones(vertices, angulo_pitch, angulo_roll, angulo_yaw=0):
        rotacion_combinada = Rxyz(angulo_roll, angulo_pitch, angulo_yaw)
        return vertices @ rotacion_combinada.T

    def actualizar_animacion(fotograma):
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

            ejes.set_xlim(-10, 10)
            ejes.set_ylim(-10, 10)
            ejes.set_zlim(-10, 10)
            ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
            ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

            etiqueta_hora.config(text=tiempos[fotograma].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d"))

        return [panel]

    canvas = FigureCanvasTkAgg(figura, master=marco_3d)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    animacion = animation.FuncAnimation(figura, actualizar_animacion, frames=len(tiempos), interval=200, blit=False)
    
    frame_padre.update_idletasks()