import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Interfaz import calculoAngulos as sun_position


def visualizar_trayectoria_panel(tiempos, azimuts, elevaciones, beta, phi):
    """
    Visualiza la trayectoria del panel solar en 3D.

    Args:
        tiempos (list): Lista de tiempos.
        azimuts (list): Lista de azimuts.
        elevaciones (list): Lista de elevaciones.
        beta (list): Lista de ángulos de pitch.
        phi (list): Lista de ángulos de roll.
    """

    # Configurar la ventana de Tkinter
    ventana_principal = tk.Tk()
    ventana_principal.title("Simulación del Movimiento del Panel Solar")

    # Crear un marco para la gráfica 3D
    marco_3d = tk.Frame(ventana_principal)
    marco_3d.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Crear la figura y el eje 3D dentro de la ventana Tkinter
    figura = plt.Figure(figsize=(10, 7), dpi=100)
    ejes = figura.add_subplot(111, projection='3d')

    # Definir los parámetros del panel
    centro = [0, 0, 0]
    ancho = 4
    alto = 2

    # Función para crear los vértices del panel solar
    def construir_panel(centro, ancho, alto):
        """
        Crea los vértices del panel solar.

        Args:
            centro (list): Coordenadas del centro del panel.
            ancho (float): Ancho del panel.
            alto (float): Alto del panel.

        Returns:
            np.array: Array con las coordenadas de los vértices.
        """
        w = ancho / 2
        h = alto / 2
        vertices = np.array([
            [centro[0] - w, centro[1] - h, centro[2]],  # Inferior izquierdo
            [centro[0] + w, centro[1] - h, centro[2]],  # Inferior derecho
            [centro[0] + w, centro[1] + h, centro[2]],  # Superior derecho
            [centro[0] - w, centro[1] + h, centro[2]]  # Superior izquierdo
        ])
        return vertices

    # Crear los vértices del panel
    vertices = construir_panel(centro, ancho, alto)

    # Inicializar el panel con nuevos colores
    panel = Poly3DCollection([vertices], facecolors=['red', 'yellow'], linewidths=3,
                             edgecolors='black')  # rojo y amarillo
    ejes.add_collection3d(panel)

    # Agregar marcadores en los vértices con nuevo color
    puntos_dispersion = [ejes.scatter(vertice[0], vertice[1], vertice[2], color='green', s=50) for vertice in
                         vertices]  # verde

    # Configurar los límites de la gráfica
    ejes.set_xlim(-5, 5)
    ejes.set_ylim(-5, 5)
    ejes.set_zlim(-5, 5)

    # Marcar la dirección del Norte (eje Y positivo)
    ejes.quiver(0, 0, 0, 5, 0, 0, color='blue', linewidth=2)  # Flecha apuntando al este
    ejes.text(5.2, 0, 0, "Este", color='blue', fontsize=12)  # Etiqueta de "Este"

    # Añadir texto para mostrar el tiempo
    etiqueta_tiempo = ejes.text2D(0.05, 0.95, "", transform=ejes.transAxes, color='black', fontsize=12)

    # Función para aplicar ambas rotaciones (pitch y roll) usando matrices combinadas
    def aplicar_rotaciones(vertices, angulo_pitch, angulo_roll):
        """
        Aplica las rotaciones de pitch y roll a los vértices.
        """
        # Usar la función Rxyz para calcular la matriz de rotación combinada
        rotacion_combinada = sun_position.Rxyz(angulo_roll, angulo_pitch, 0)  # gamma = 0

        # Aplicar la rotación combinada a los vértices
        return vertices @ rotacion_combinada.T

    # Función para inicializar la animación
    def iniciar_animacion():
        """
        Inicializa la animación.
        """
        panel.set_verts([vertices])
        etiqueta_tiempo.set_text('')  # Iniciar con texto vacío
        for punto in puntos_dispersion:
            punto._offsets3d = (vertices[:, 0], vertices[:, 1], vertices[:, 2])
            return [panel] + puntos_dispersion + [etiqueta_tiempo]

    # Función para actualizar la animación con los valores de beta y phi
    def actualizar_animacion(fotograma):
        """
        Actualiza la animación en cada fotograma.

        Args:
            fotograma (int): Número de fotograma actual.
        """
        if fotograma < len(tiempos):
            # Aplicar rotaciones combinadas
            vertices_rotados = aplicar_rotaciones(vertices, beta[fotograma], phi[fotograma])

            # Actualizar las posiciones del panel
            panel.set_verts([vertices_rotados])

            # Actualizar las posiciones de los puntos en los vértices
            for i, punto in enumerate(puntos_dispersion):
                punto._offsets3d = (np.array([vertices_rotados[i, 0]]),
                                    np.array([vertices_rotados[i, 1]]),
                                    np.array([vertices_rotados[i, 2]]))

            # Actualizar la etiqueta de tiempo con el tiempo calculado
            tiempo_actual = tiempos[fotograma].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d")
            etiqueta_tiempo.set_text(tiempo_actual)

        return [panel] + puntos_dispersion + [etiqueta_tiempo]

    # Crear el lienzo para la figura 3D
    canvas3 = FigureCanvasTkAgg(figura, master=marco_3d)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Crear la animación dentro de la ventana Tkinter, sin blit
    intervalo_tiempo_ms = 1000  # Un frame por segundo para sincronizar con el tiempo real
    animacion = animation.FuncAnimation(figura, actualizar_animacion, frames=np.arange(0, len(tiempos)),
                                        init_func=iniciar_animacion, interval=intervalo_tiempo_ms, blit=False)

    # Iniciar la interfaz gráfica de Tkinter
    ventana_principal.mainloop()