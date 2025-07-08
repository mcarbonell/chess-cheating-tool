# DONE

## Fase 1: Núcleo de Análisis (CLI)

- [X] Configuración del proyecto con `poetry` y dependencias iniciales.
- [X] Integración y comunicación con el motor de ajedrez Stockfish usando `python-chess`.
- [X] Creación de una herramienta de línea de comandos (`src/analysis_core.py`) que acepta un fichero PGN y la profundidad del análisis.
- [X] Implementado el cálculo de **Pérdida Promedio de Centipeones (ACPL)** por jugador (Blancas y Negras) usando un método incremental eficiente.
- [X] Implementado el cálculo del **Porcentaje de Precisión** por jugador, basado en la fórmula y las estadísticas WDL de Lichess.
- [X] Generación de un informe final en la consola con las métricas ACPL y Precisión.
