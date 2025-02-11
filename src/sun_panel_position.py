"""
Módulo para la visualización simultánea de la trayectoria del panel solar y del sol en 3D.

Este módulo utiliza `matplotlib` y `tkinter` para representar simultáneamente
el movimiento del panel solar y la trayectoria del sol en una única ventana.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from src import sun_position


def visualizar_trayectoria_panel_y_sol(tiempos, azimuts, elevaciones, beta, phi):
    """
    Visualiza simultáneamente la trayectoria del panel solar y del sol en 3D mediante una animación.

    Args:
        tiempos (list): Lista de tiempos de la simulación.
        azimuts (list): Lista de ángulos azimutales del sol.
        elevaciones (list): Lista de ángulos de elevación del sol.
        beta (list): Lista de ángulos de pitch del panel solar.
        phi (list): Lista de ángulos de roll del panel solar.
    """
    # Crear ventana de Tkinter
    ventana_principal = tk.Tk()
    ventana_principal.title("Simulación del Movimiento del Panel Solar y del Sol")

    # Marco para la gráfica 3D
    marco_3d = tk.Frame(ventana_principal)
    marco_3d.pack(fill=tk.BOTH, expand=True)

    # Crear la figura y el eje 3D dentro de Tkinter
    figura = plt.Figure(figsize=(10, 7), dpi=100)
    ejes = figura.add_subplot(111, projection='3d')

    # Definir los parámetros del panel solar
    centro_panel = [0, 0, 0]
    ancho = 4
    alto = 2

    def construir_panel(centro, ancho, alto):
        """
        Crea los vértices del panel solar para su representación en 3D.

        Args:
            centro (list): Coordenadas del centro del panel.
            ancho (float): Ancho del panel solar.
            alto (float): Alto del panel solar.

        Returns:
            np.array: Array con las coordenadas de los vértices del panel.
        """
        w = ancho / 2
        h = alto / 2
        return np.array([
            [centro[0] - w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] - h, centro[2]],
            [centro[0] + w, centro[1] + h, centro[2]],
            [centro[0] - w, centro[1] + h, centro[2]]
        ])

    def create_sun(ax, center, radius=0.5, color='orange'):
        """
        Crea una representación esférica del sol en un gráfico 3D.

        Args:
            ax (matplotlib.Axes3D): Eje 3D donde se dibujará el sol.
            center (list): Coordenadas [x, y, z] del centro del sol.
            radius (float, opcional): Radio de la esfera solar (por defecto 0.5).
            color (str, opcional): Color de la esfera (por defecto 'orange').
        """
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        ax.plot_surface(x, y, z, color=color, shade=True, rstride=2, cstride=2, linewidth=0)

    # Crear los vértices del panel solar
    vertices = construir_panel(centro_panel, ancho, alto)

    # Crear la representación visual del panel con colores
    panel = Poly3DCollection([vertices], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black')
    ejes.add_collection3d(panel)

    # Agregar marcadores en los vértices del panel
    puntos_panel = [ejes.scatter(vertice[0], vertice[1], vertice[2], color='green', s=50) for vertice in vertices]

    # Configurar límites del gráfico 3D para incluir el sol y el panel
    ejes.set_xlim(-10, 10)
    ejes.set_ylim(-10, 10)
    ejes.set_zlim(-10, 10)

    # Marcar la dirección del Este en la visualización
    ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
    ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

    # Agregar una etiqueta de tiempo en la animación
    etiqueta_tiempo = ejes.text2D(0.05, 0.95, "", transform=ejes.transAxes, color='black', fontsize=12)

    def aplicar_rotaciones(vertices, angulo_pitch, angulo_roll):
        """
        Aplica las rotaciones de pitch y roll a los vértices del panel.

        Args:
            vertices (np.array): Coordenadas de los vértices originales.
            angulo_pitch (float): Ángulo de inclinación (beta).
            angulo_roll (float): Ángulo de giro (phi).

        Returns:
            np.array: Coordenadas transformadas después de la rotación.
        """
        rotacion_combinada = sun_position.Rxyz(angulo_roll, angulo_pitch, 0)
        return vertices @ rotacion_combinada.T

    def iniciar_animacion():
        panel.set_verts([vertices])
        etiqueta_tiempo.set_text('')
        for punto in puntos_panel:
            punto._offsets3d = (vertices[:, 0], vertices[:, 1], vertices[:, 2])
        return [panel] + puntos_panel + [etiqueta_tiempo]

    def actualizar_animacion(fotograma):
        if fotograma < len(tiempos):
            # Aplicar rotaciones al panel
            vertices_rotados = aplicar_rotaciones(vertices, beta[fotograma], phi[fotograma])
            panel.set_verts([vertices_rotados])
            for i, punto in enumerate(puntos_panel):
                punto._offsets3d = (np.array([vertices_rotados[i, 0]]),
                                    np.array([vertices_rotados[i, 1]]),
                                    np.array([vertices_rotados[i, 2]]))

            # Actualizar la posición del sol
            ejes.clear()
            ejes.add_collection3d(Poly3DCollection([vertices_rotados], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black'))
            create_sun(ejes, [azimuts[fotograma] / 10, elevaciones[fotograma] / 10, 0])  # Ajuste de escala para visualización

            # Configurar de nuevo los ejes y límites
            ejes.set_xlim(-10, 10)
            ejes.set_ylim(-10, 10)
            ejes.set_zlim(-10, 10)
            ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)
            ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)

            # Actualizar la etiqueta de tiempo
            tiempo_actual = tiempos[fotograma].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d")
            etiqueta_tiempo = ejes.text2D(0.05, 0.95, tiempo_actual, transform=ejes.transAxes, color='black', fontsize=12)

        return [panel] + puntos_panel + [etiqueta_tiempo]

    # Crear el lienzo para integrar la gráfica 3D en la ventana de Tkinter
    canvas3 = FigureCanvasTkAgg(figura, master=marco_3d)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Configurar la animación de la trayectoria del panel y el sol
    intervalo_tiempo_ms = 1000  # 1 frame por segundo para sincronizar con el tiempo real
    animacion = animation.FuncAnimation(figura, actualizar_animacion, frames=np.arange(0, len(tiempos)),
                                        init_func=iniciar_animacion, interval=intervalo_tiempo_ms, blit=False)

    # Iniciar la ventana de Tkinter
    ventana_principal.mainloop()