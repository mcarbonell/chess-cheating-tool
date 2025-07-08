# Detector Avanzado de Trampas en Ajedrez

Este proyecto es una herramienta web para analizar partidas de ajedrez en formato PGN. Utiliza el potente motor **Stockfish** para realizar un análisis profundo jugada a jugada, calculando métricas avanzadas como la **Pérdida Promedio de Centipeones (ACPL)** y un **Porcentaje de Precisión** basado en el método de Lichess.

El resultado es una interfaz de análisis rica e interactiva, inspirada en las herramientas de Lichess, que permite a los usuarios entender en profundidad el desarrollo de una partida.

## Estado del Proyecto

El proyecto ha completado la implementación de un **núcleo de análisis robusto** y un **frontend interactivo (MVP)**.

Para un seguimiento detallado del progreso, puedes consultar:
- **[Tareas Completadas (DONE.md)](docs/DONE.md)**
- **[Tareas Pendientes (TODO.md)](docs/TODO.md)**

## Características Principales

*   **Interfaz Web Completa:** Una aplicación Flask que presenta los resultados en un dashboard de dos columnas.
*   **Análisis Profundo por Jugada:**
    *   Cálculo del **ACPL**.
    *   Cálculo de la **Precisión** basada en la conversión de centipeones a porcentaje de victoria.
*   **Visualizaciones Interactivas:**
    *   **Tablero de Ajedrez** con controles para navegar por toda la partida.
    *   **Gráfica de Evaluación** que muestra la ventaja material jugada a jugada.
    *   **Tabla de Análisis Detallada** con las métricas de cada movimiento, que al hacer clic, actualiza el tablero a esa posición.

### Captura de Pantalla
![Screenshot de la aplicación](https://i.imgur.com/your-screenshot-url.png)  <!-- Reemplaza esto con la URL de tu captura cuando la subas -->

## Cómo Usar la Aplicación

### 1. Prerrequisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/) para la gestión de dependencias.
- El motor Stockfish (el ejecutable se incluye en el repositorio en la carpeta `stockfish/`).

### 2. Instalación

Clona el repositorio e instala las dependencias usando Poetry:

```bash
git clone <URL-del-repositorio>
cd <nombre-del-repositorio>
poetry install
```

### 3. Crear la Carpeta de Imágenes (Primer Uso)
La aplicación necesita las imágenes de las piezas de ajedrez.
1.  **Crea la estructura de carpetas:** `src/static/img/chesspieces/wikipedia/`
2.  **Descarga las imágenes** desde el [repositorio de chessboard-js](https://github.com/oakmac/chessboardjs/raw/master/img/chesspieces/wikipedia.zip).
3.  **Descomprime y copia** los archivos `.png` en la carpeta `wikipedia` que has creado.

### 4. Ejecución del Servidor Web

Ejecuta la aplicación Flask con el siguiente comando:

```bash
poetry run flask --app src/main run
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

Abre tu navegador, pega el PGN de una partida, selecciona la profundidad y haz clic en "Analyze Game".

## Próximos Pasos

Los siguientes grandes objetivos se centran en refinar aún más el análisis backend (implementando métricas como MultiPV) y continuar añadiendo funcionalidades a la interfaz, como la capacidad de subir archivos PGN.
