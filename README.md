# Detector Avanzado de Trampas en Ajedrez

Este proyecto es una herramienta diseñada para analizar partidas de ajedrez en formato PGN y detectar patrones de juego que puedan sugerir el uso de asistencia externa (motores de ajedrez). Va más allá de las métricas simples, implementando análisis profundos inspirados en las técnicas utilizadas por plataformas líderes como Lichess.

El núcleo del proyecto es una potente herramienta de línea de comandos que utiliza el motor de ajedrez **Stockfish** para realizar un análisis detallado de cada jugada.

## Estado Actual

El proyecto se encuentra en la **Fase 1**, con un núcleo de análisis funcional implementado.

Para un seguimiento detallado del progreso, puedes consultar:
- **[Tareas Completadas (DONE.md)](docs/DONE.md)**
- **[Tareas Pendientes (TODO.md)](docs/TODO.md)**

## Características Implementadas (CLI)

La herramienta de línea de comandos `src/analysis_core.py` actualmente puede:

1.  **Analizar una partida desde un archivo PGN.**
2.  **Calcular la Pérdida Promedio de Centipeones (ACPL)** para Blancas y Negras.
3.  **Calcular el Porcentaje de Precisión** (al estilo Lichess) para ambos jugadores.
4.  **Ajustar la profundidad del análisis** para un balance entre velocidad y precisión.

## Cómo Usar la Herramienta CLI

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

### 3. Ejecución

Para analizar una partida, utiliza el siguiente comando, especificando la ruta al archivo PGN y, opcionalmente, la profundidad del análisis.

```bash
poetry run python src/analysis_core.py --pgn_file ruta/a/tu/partida.pgn --depth 14
```

- `--pgn_file`: **(Requerido)** La ruta al archivo PGN que quieres analizar.
- `--depth`: **(Opcional)** La profundidad de búsqueda para Stockfish. Un valor más alto es más preciso pero más lento. El valor por defecto es `14`.

### Ejemplo de Salida

```
Starting incremental PGN analysis with depth 14...
Move 1 (g1f3) by White: ACPL=28
Move 1 (g8f6) by Black: ACPL=5
...
Analysis complete.

--- Analysis Report ---
White: ACPL = 22.49, Accuracy = 90.15%
Black: ACPL = 31.20, Accuracy = 87.33%
```

## Próximos Pasos

El siguiente gran objetivo es comenzar el desarrollo de la **Fase 4: Interfaz Web (MVP)** para hacer que la herramienta sea accesible a través de un navegador, o continuar refinando el análisis con métricas más avanzadas.
