"""
Módulo para la visualización de la trayectoria del panel solar en 3D.

Este módulo utiliza `matplotlib` y `tkinter` para representar el movimiento
del panel solar en función de los ángulos de azimut, elevación, pitch y roll.
La animación permite observar la orientación dinámica del panel a lo largo del tiempo.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Interfaz import calculoAngulos as sun_position


def visualizar_trayectoria_panel(tiempos, azimuts, elevaciones, beta, phi):
    """
    Visualiza la trayectoria del panel solar en 3D mediante una animación.

    Args:
        tiempos (list): Lista de tiempos de la simulación.
        azimuts (list): Lista de ángulos azimutales del sol.
        elevaciones (list): Lista de ángulos de elevación del sol.
        beta (list): Lista de ángulos de pitch del panel solar.
        phi (list): Lista de ángulos de roll del panel solar.
    """
    # Crear ventana de Tkinter
    ventana_principal = tk.Tk()
    ventana_principal.title("Simulación del Movimiento del Panel Solar")

    # Marco para la gráfica 3D
    marco_3d = tk.Frame(ventana_principal)
    marco_3d.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Crear la figura y el eje 3D dentro de Tkinter
    figura = plt.Figure(figsize=(10, 7), dpi=100)
    ejes = figura.add_subplot(111, projection='3d')

    # Definir los parámetros del panel solar
    centro = [0, 0, 0]
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
        vertices = np.array([
            [centro[0] - w, centro[1] - h, centro[2]],  # Inferior izquierdo
            [centro[0] + w, centro[1] - h, centro[2]],  # Inferior derecho
            [centro[0] + w, centro[1] + h, centro[2]],  # Superior derecho
            [centro[0] - w, centro[1] + h, centro[2]]   # Superior izquierdo
        ])
        return vertices

    # Crear los vértices del panel solar
    vertices = construir_panel(centro, ancho, alto)

    # Crear la representación visual del panel con colores
    panel = Poly3DCollection([vertices], facecolors=['red', 'yellow'], linewidths=3, edgecolors='black')
    ejes.add_collection3d(panel)

    # Agregar marcadores en los vértices del panel
    puntos_dispersion = [ejes.scatter(vertice[0], vertice[1], vertice[2], color='green', s=50) for vertice in vertices]

    # Configurar límites del gráfico 3D
    ejes.set_xlim(-5, 5)
    ejes.set_ylim(-5, 5)
    ejes.set_zlim(-5, 5)

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
        # Obtener la matriz de rotación combinada
        rotacion_combinada = sun_position.Rxyz(angulo_roll, angulo_pitch, 0)  # Se asume gamma = 0

        # Aplicar la rotación a los vértices
        return vertices @ rotacion_combinada.T

    def iniciar_animacion():
        """
        Inicializa la animación de la trayectoria del panel solar.
        """
        panel.set_verts([vertices])
        etiqueta_tiempo.set_text('')  # Iniciar sin texto visible

        for punto in puntos_dispersion:
            punto._offsets3d = (vertices[:, 0], vertices[:, 1], vertices[:, 2])

        return [panel] + puntos_dispersion + [etiqueta_tiempo]

    def actualizar_animacion(fotograma):
        """
        Actualiza la animación en cada fotograma para reflejar el movimiento del panel.

        Args:
            fotograma (int): Índice del fotograma actual en la simulación.
        """
        if fotograma < len(tiempos):
            # Aplicar rotaciones de pitch y roll
            vertices_rotados = aplicar_rotaciones(vertices, beta[fotograma], phi[fotograma])

            # Actualizar la posición del panel en la animación
            panel.set_verts([vertices_rotados])

            # Actualizar la posición de los puntos en los vértices
            for i, punto in enumerate(puntos_dispersion):
                punto._offsets3d = (np.array([vertices_rotados[i, 0]]),
                                    np.array([vertices_rotados[i, 1]]),
                                    np.array([vertices_rotados[i, 2]]))

            # Actualizar la etiqueta de tiempo en la animación
            tiempo_actual = tiempos[fotograma].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d")
            etiqueta_tiempo.set_text(tiempo_actual)

        return [panel] + puntos_dispersion + [etiqueta_tiempo]

    # Crear el lienzo para integrar la gráfica 3D en la ventana de Tkinter
    canvas3 = FigureCanvasTkAgg(figura, master=marco_3d)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Configurar la animación de la trayectoria del panel
    intervalo_tiempo_ms = 1000  # 1 frame por segundo para sincronizar con el tiempo real
    animacion = animation.FuncAnimation(figura, actualizar_animacion, frames=np.arange(0, len(tiempos)),
                                        init_func=iniciar_animacion, interval=intervalo_tiempo_ms, blit=False)

    # Iniciar la ventana de Tkinter
    ventana_principal.mainloop()
