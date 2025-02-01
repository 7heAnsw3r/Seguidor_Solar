## Seguidor Solar de 2 Grados de Libertad ☀️

Este proyecto implementa un simulador de un seguidor solar de 2 grados de libertad, que calcula los ángulos de control *pitch* y *roll* para mantener un panel solar perpendicular a la luz solar incidente durante un día determinado. 

**Características:**

*  Calcula la posición solar (azimut y elevación) para una fecha y ubicación geográfica dadas. 🌎
*  Determina los ángulos de control *pitch* y *roll* utilizando matrices de rotación. 🔄
*  Visualiza la trayectoria del sol y el panel solar en 3D. 📊
*  Permite al usuario ingresar la fecha y la duración de la simulación a través de una interfaz gráfica. 📅

**Cómo ejecutar el código:**

1.  **Instalar las dependencias:**
    ```bash
    pip install pysolar matplotlib numpy pytz tkcalendar datetime mpl_toolkits.mplot3d animation tkinter
    ```

2.  **Ejecutar el archivo principal:**
    ```bash
    python main.py
    ```

**Uso:**

1.  **Ingresar la fecha y hora de inicio y fin de la simulación en la interfaz gráfica.** ⏰
2.  **Visualizar la trayectoria del sol y el panel solar en las gráficas 3D.** 📈

**Estructura del proyecto:**

*   `main.py`: Archivo principal que contiene la lógica del programa. 💡
*   `funciones.py`: Contiene las funciones para calcular la posición solar y los ángulos de control. 🧮
*   `visualizacion.py`:  Contiene las funciones para visualizar la trayectoria del sol y el panel. 📉

**Nota:**

Este proyecto fue desarrollado como parte de un proyecto de métodos numéricos. 👩‍💻
