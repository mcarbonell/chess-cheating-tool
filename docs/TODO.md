# TODO

## Fase 1: Núcleo de Análisis (CLI) - Refinamientos

- [ ] Implementar la métrica **Rango Promedio MultiPV**.
- [ ] Implementar la métrica **Dificultad de la Jugada / Puntuación de Horizonte**.
- [ ] Implementar la métrica **Consistencia de Errores (Desviación Estándar del ACPL)**.
- [ ] Generar una salida de análisis más estructurada (ej. JSON) para facilitar su consumo por otros sistemas.

## Fase 2: Adquisición y Procesamiento de Datos

- [ ] Script para descargar una muestra de la base de datos de partidas de Lichess.
- [ ] Script para analizar por lotes las partidas descargadas y almacenar los resultados (métricas + Elo del jugador).
- [ ] Limpieza y preprocesamiento de los datos para el entrenamiento del modelo.

## Fase 3: Modelado y Entrenamiento del "Performance ELO"

- [ ] Selección de características (`features`) para el modelo.
- [ ] Entrenamiento de un modelo de regresión (ej. XGBoost) para predecir el "ELO de Rendimiento".
- [ ] Evaluación y ajuste del modelo.
- [ ] Guardar y cargar el modelo entrenado.

## Fase 4: Interfaz Web (MVP)

- [ ] Estructura básica de una aplicación web con **Flask** o **FastAPI**.
- [ ] Creación de un endpoint que acepte un PGN (texto o archivo).
- [ ] Integración del núcleo de análisis para procesar las solicitudes desde la web.
- [ ] Diseño de un frontend simple (HTML/CSS/JS) para pegar el PGN y mostrar los resultados.
- [ ] Implementar un sistema de cola de tareas (ej. Celery) si el análisis es muy lento.

## Fase 5: Reporte y Visualización de Resultados

- [ ] Diseño de un formato de reporte claro y atractivo en la interfaz web.
- [ ] Visualización del tablero de ajedrez, destacando jugadas clave.
- [ ] Gráficos para mostrar la evolución de la evaluación y el ACPL a lo largo de la partida.
