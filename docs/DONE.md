# DONE

## Fase 1: Núcleo de Análisis (CLI)

- [X] Configuración del proyecto con `poetry` y dependencias iniciales.
- [X] Integración y comunicación con el motor de ajedrez Stockfish usando `python-chess`.
- [X] Creación de una herramienta de línea de comandos (`src/analysis_core.py`) que acepta un fichero PGN y la profundidad del análisis.
- [X] Implementado el cálculo de **Pérdida Promedio de Centipeones (ACPL)** por jugador (Blancas y Negras) usando un método incremental eficiente.
- [X] Implementado el cálculo del **Porcentaje de Precisión** por jugador, basado en la fórmula y las estadísticas de Lichess.
- [X] Generación de un informe final en la consola con las métricas ACPL y Precisión.

## Fase 4: Interfaz Web (MVP)

- [X] Estructura básica de una aplicación web con **Flask**.
- [X] Endpoint `/analyze` que acepta un PGN y devuelve un `JSON` con los resultados.
- [X] Diseño de un frontend básico (HTML, CSS, JS) con un área de texto para pegar el PGN y un botón de "Analizar".
- [X] Integración del núcleo de análisis para procesar las solicitudes desde la web.

## Fase 5: Reporte y Visualización de Resultados

- [X] Diseño de un formato de reporte estructurado en dos columnas.
- [X] **Tablero de Ajedrez Interactivo:** Visualización del tablero con controles para navegar por las jugadas (`chessboard-js`).
- [X] **Gráfica de Evaluación:** Gráfico de líneas que muestra la evolución de la evaluación de Stockfish jugada a jugada (`Chart.js`).
- [X] **Tabla de Análisis Detallada:** Tabla que muestra el ACPL y la Precisión de cada jugada individual.
- [X] **Interactividad Cruzada:** Clicar en una fila de la tabla de análisis salta a esa posición en el tablero de ajedrez.
