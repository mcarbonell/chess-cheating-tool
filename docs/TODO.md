# TODO

## Fase 1: Núcleo de Análisis (CLI) - Refinamientos Avanzados

- [ ] Implementar la métrica **Rango Promedio MultiPV**.
- [ ] Implementar la métrica **Dificultad de la Jugada / Puntuación de Horizonte**.
- [ ] Implementar la métrica **Consistencia de Errores (Desviación Estándar del ACPL)**.
- [ ] Generar una salida de análisis más estructurada (ej. JSON) para facilitar su consumo por otros sistemas (si se decide crear una API pública).

## Fase 2: Adquisición y Procesamiento de Datos

- [ ] Script para descargar una muestra de la base de datos de partidas de Lichess.
- [ ] Script para analizar por lotes las partidas descargadas y almacenar los resultados (métricas + Elo del jugador).
- [ ] Limpieza y preprocesamiento de los datos para el entrenamiento del modelo.

## Fase 3: Modelado y Entrenamiento del "Performance ELO"

- [ ] Selección de características (`features`) para el modelo.
- [ ] Entrenamiento de un modelo de regresión (ej. XGBoost) para predecir el "ELO de Rendimiento".
- [ ] Evaluación y ajuste del modelo.
- [ ] Guardar y cargar el modelo entrenado.

## Mejoras Futuras para la Interfaz Web

- [ ] Permitir al usuario subir un archivo PGN además de pegar el texto.
- [ ] Implementar un sistema de cola de tareas (ej. Celery) si el análisis a mayor profundidad resulta ser muy lento para una respuesta HTTP directa.
- [ ] Mejorar la visualización destacando las jugadas "brillantes" o los "errores graves" en el tablero o la tabla.
- [ ] Añadir información del encabezado del PGN (nombres de los jugadores, resultado, etc.) al informe.
