import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt


def configure_axes(ax, title, xlabel=None, ylabel=None, zlabel=None):
    """
    Configures the axes of a plot.
    """
    ax.set_title(title, fontsize=16)
    if xlabel: ax.set_xlabel(xlabel, fontsize=12)
    if ylabel: ax.set_ylabel(ylabel, fontsize=12)
    if zlabel: ax.set_zlabel(zlabel, fontsize=12)


def create_sun(ax, center, radius=1.0, color='orange'):  # Reduced initial radius
    """
    Creates a sphere representing the sun in a 3D plot with a smaller initial size.
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
    ax.plot_surface(x, y, z, color=color, shade=True, rstride=2, cstride=2, linewidth=0)


def graph_trayectoria_3d(times, azimuths, elevations):
    time_numbers = np.arange(len(times))

    root = tk.Tk()

    root.geometry("1200x800")  # Large window size for better visibility
    frame_3d = tk.Frame(root)
    frame_3d.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    fig3 = plt.Figure(figsize=(25, 20), dpi=100)
    ax3 = fig3.add_subplot(111, projection='3d')
    configure_axes(ax3, "Solar Trajectory", "Time", "Azimuth", "Elevation")
    ax3.set_xlim(0, len(times) - 1)
    ax3.set_ylim(min(azimuths) - 5, max(azimuths) + 5)
    ax3.set_zlim(min(elevations) - 5, max(elevations) + 5)

    # Plot all trajectory lines initially
    ax3.plot(time_numbers, azimuths, elevations, 'y-', alpha=0.3)  # Use alpha for a faint line

    def update_3d(frame):
        ax3.clear()  # Clear only the sun, not the trajectory line
        configure_axes(ax3, "Solar Trajectory", "Time", "Azimuth", "Elevation")
        ax3.set_xlim(0, len(times) - 1)
        ax3.set_ylim(min(azimuths) - 5, max(azimuths) + 5)
        ax3.set_zlim(min(elevations) - 5, max(elevations) + 5)

        # Replot the trajectory line with lower opacity
        ax3.plot(time_numbers, azimuths, elevations, 'y-', alpha=0.3)

        # Plot the sun at the current position with increasing size
        sun_radius = 1.0  # + frame * 0.01  # Gradually increase size of the sun
        create_sun(ax3, [time_numbers[frame], azimuths[frame], elevations[frame]], radius=sun_radius)
        tiempo_actual = times[frame].strftime("Hora: %Hh%M\nFecha: %Y-%m-%d")
        ax3.text2D(0.05, 0.95, tiempo_actual, transform=ax3.transAxes, color='black', fontsize=12)
        return []

    canvas3 = FigureCanvasTkAgg(fig3, master=frame_3d)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    ani3 = animation.FuncAnimation(fig3, update_3d, frames=len(times), interval=500, blit=False)
    root.mainloop()

