# Propuesta de Proyecto: Detector Avanzado de Trampas en Ajedrez Online

## 1. Introducción y Visión General

El ajedrez online enfrenta un creciente problema de trampas, que socava la integridad del juego competitivo. Las herramientas de detección existentes en plataformas como Lichess y Chess.com se basan principalmente en métricas de "precisión" o "pérdida de centipeones" (ACPL), que, si bien son útiles, tienen limitaciones significativas para diferenciar el juego humano excepcional del juego asistido por motor.

Este proyecto propone desarrollar una herramienta avanzada de detección de trampas que vaya más allá de las métricas superficiales. Nuestro objetivo es identificar patrones de juego "inhumanos" mediante el análisis profundo de partidas PGN, utilizando un motor de ajedrez potente como Stockfish y técnicas de Machine Learning para contextualizar el rendimiento del jugador.

La herramienta permitirá a los usuarios pegar un PGN de cualquier partida (independientemente de la plataforma) y obtener un informe detallado sobre la probabilidad de asistencia de motor para uno o ambos jugadores.

## 2. Objetivo del Proyecto

El objetivo principal es crear un sistema robusto capaz de:

*   **Identificar Jugadas Inhumanas:** Detectar patrones de jugadas que son extremadamente difíciles o imposibles de encontrar para un humano, incluso un Gran Maestro.
*   **Contextualizar el Rendimiento:** Evaluar el rendimiento del jugador en una partida en relación con su nivel de Elo reportado, calculando un "Elo de Rendimiento" para esa partida.
*   **Generar Informes Claros:** Proporcionar un análisis detallado y fácil de entender de la partida, con un "Índice de Trampa" ponderado y explicaciones de las métricas.
*   **Ser Accesible:** Ofrecer una interfaz de usuario sencilla (web) para el análisis de partidas individuales.
*   **Ser Sostenible:** Explorar un modelo freemium para cubrir los altos costos computacionales del análisis profundo.

## 3. Funcionalidades Clave y Métricas Avanzadas

Para lograr nuestro objetivo, la herramienta calculará las siguientes métricas para cada jugada de la partida, y luego las agregará para obtener un promedio o suma a nivel de partida:

*   **1. Métricas Estándar (Base):**
    *   **ACPL (Average Centipawn Loss):** Pérdida promedio de centipeones por jugada.
    *   **Accuracy%:** Porcentaje de precisión, según la fórmula de Lichess o similar.

*   **2. Rango Promedio MultiPV (Métrica de Consistencia):**
    *   **Descripción:** Mide la posición promedio de la jugada realizada por el jugador en la lista de las 'N' mejores jugadas que ofrece Stockfish (con `MultiPV=N`). Los motores eligen casi siempre la #1, los humanos varían más, especialmente si hay múltiples jugadas casi igual de buenas.
    *   **Implementación:** Analizar con Stockfish (ej. `MultiPV=5`) a profundidad media (ej. 18-20). Registrar el rango de la jugada del jugador.

*   **3. Dificultad de la Jugada / Puntuación de Horizonte (Métrica de Insight):**
    *   **Descripción:** Identifica jugadas que parecen malas o neutras a poca profundidad de análisis (ej. un sacrificio de pieza o dama) pero que se revelan como excelentes o ganadoras a mayor profundidad. La detección consistente de estas jugadas es altamente indicativa de asistencia de motor.
    *   **Implementación:** Comparar la evaluación de la jugada del jugador a una `Profundidad Baja` (ej. 10-12) con su evaluación a una `Profundidad Alta` (ej. 22-26). Cuantificar la "sorpresa" o "mejora" de la evaluación con la profundidad.

*   **4. Consistencia de Errores (Desviación Estándar del ACPL):**
    *   **Descripción:** Mide la variabilidad en la calidad de las jugadas del jugador. Los humanos tienden a cometer errores en ráfagas o en momentos de presión, llevando a una desviación estándar alta en el ACPL. Los motores (o tramposos) mantienen una calidad de jugada más uniforme, resultando en una desviación estándar muy baja.
    *   **Implementación:** Calcular la desviación estándar de la pérdida de centipeones por jugada a lo largo de la partida.

*   **5. Precisión en Fases Críticas:**
    *   **Descripción:** Evalúa la precisión del jugador específicamente en posiciones de alta complejidad táctica, bajo presión, o tras jugadas sorprendentes del oponente. Los humanos suelen rendir peor en estas situaciones, mientras que los motores mantienen su nivel.
    *   **Implementación:** Identificar posiciones "críticas" (ej. cambios bruscos en la evaluación, alta cantidad de tácticas forzadas) y calcular las métricas (ACPL, Rango MultiPV) solo para estas jugadas.

*   **6. Correlación Tiempo/Complejidad (Si Disponible en PGN):**
    *   **Descripción:** Analiza la relación entre el tiempo invertido por el jugador en una jugada y la complejidad o dificultad de dicha jugada. Los humanos tardan más en jugadas difíciles; los tramposos a menudo usan tiempos constantes o patrones anómalos.
    *   **Implementación:** Si el PGN incluye `[%clk]` o `[%emt]`, correlacionar el tiempo por jugada con la dificultad de la posición (basada en el `nps` de Stockfish, el número de nodos explorados para encontrar la mejor jugada, o la puntuación de Horizonte).

*   **7. "Performance ELO" (Métrica de Contextualización Clave):**
    *   **Descripción:** Un modelo de Machine Learning entrenado en millones de partidas humanas "limpias" de Lichess que, dadas las métricas anteriores (ACPL, Rango MultiPV, Horizonte, etc.), predice el Elo de rendimiento que se esperaría de un jugador que juega con esa calidad.
    *   **Implementación:** Entrenar un modelo de regresión (ej. XGBoost) donde las entradas son las métricas de la partida y la salida es el Elo real del jugador.

*   **8. Índice de Trampa (Resultado Final):**
    *   **Descripción:** Una puntuación consolidada (ej. de 0 a 100) que representa la probabilidad de asistencia externa. Se calculará ponderando las métricas anteriores, especialmente la discrepancia entre el Elo de rendimiento predicho y el Elo real del jugador (`Delta ELO`).

## 4. Fases de Desarrollo

El proyecto se abordará en las siguientes fases:

### Fase 1: Desarrollo del Núcleo de Análisis (CLI)

*   **Objetivo:** Crear una herramienta de línea de comandos capaz de analizar un solo PGN y extraer todas las métricas avanzadas por jugada y para la partida completa.
*   **Tareas Principales:**
    *   Parseo de PGNs utilizando `python-chess`.
    *   Configuración y comunicación con el motor Stockfish a través del protocolo UCI.
    *   Iteración por cada jugada de la partida, actualizando el estado del tablero.
    *   Ejecución de Stockfish para obtener evaluaciones a `Profundidad Baja`, `Profundidad Alta`, y `MultiPV`.
    *   Cálculo de todas las métricas (ACPL, Accuracy%, Rango MultiPV, Dificultad/Horizonte, Consistencia).
    *   Salida de los resultados en un formato estructurado (ej. JSON) para facilitar el procesamiento posterior.

### Fase 2: Adquisición y Procesamiento de Datos para "Performance ELO"

*   **Objetivo:** Construir un dataset masivo de partidas humanas para entrenar el modelo de Performance ELO.
*   **Tareas Principales:**
    *   Descarga de una muestra representativa de la base de datos de Lichess (varios niveles de Elo, partidas "limpias").
    *   Uso de la herramienta CLI de la Fase 1 para analizar por lotes miles (o millones) de estas partidas.
    *   Almacenamiento eficiente de los resultados del análisis (ej. en archivos CSV o Parquet) junto con el Elo real del jugador de cada partida.
    *   Limpieza y preprocesamiento de los datos para el Machine Learning.

### Fase 3: Modelado y Entrenamiento del "Performance ELO"

*   **Objetivo:** Desarrollar y entrenar el modelo de Machine Learning que predice el Elo de rendimiento.
*   **Tareas Principales:**
    *   Selección de características (`features`) del dataset generado en la Fase 2.
    *   Selección de algoritmo de Machine Learning (ej. XGBoost, LightGBM) para un problema de regresión.
    *   Entrenamiento del modelo con los datos.
    *   Evaluación del modelo y ajuste de hiperparámetros.
    *   Persistencia del modelo entrenado (ej. guardarlo en un archivo `.pkl` o `.joblib`).

### Fase 4: Interfaz Web (MVP)

*   **Objetivo:** Crear una interfaz web simple para que los usuarios finales interactúen con la herramienta.
*   **Tareas Principales:**
    *   Diseño de un frontend básico (HTML, CSS, JS) con un área de texto para pegar el PGN y un botón de "Analizar".
    *   Desarrollo de un backend API (Flask o FastAPI) que reciba el PGN del frontend.
    *   Integración del núcleo de análisis (Fase 1) y el modelo de Performance ELO (Fase 3) en el backend.
    *   Procesamiento del PGN, ejecución del análisis, y cálculo del Índice de Trampa.
    *   Retorno de un reporte legible al frontend.
    *   Implementación de una cola de tareas si el análisis puede ser prolongado.

### Fase 5: Reporte y Visualización de Resultados

*   **Objetivo:** Presentar los resultados de manera clara, interactiva y comprensible.
*   **Tareas Principales:**
    *   Diseño de un formato de reporte estructurado.
    *   Posibilidad de visualizar el tablero, las jugadas sospechosas.
    *   Gráficos simples de evaluación, ACPL por jugada, etc.
    *   Explicaciones textuales para cada métrica y el "Índice de Trampa" final.

## 5. Stack Tecnológico Sugerido

*   **Lenguaje de Programación:** Python (para todo el backend y lógica de análisis/ML).
*   **Motor de Ajedrez:** Stockfish (ejecutable).
*   **Librerías Python:**
    *   `python-chess`: Para manipulación de PGN y comunicación UCI.
    *   `pandas`, `numpy`: Para manipulación de datos.
    *   `scikit-learn`, `xgboost`/`lightgbm`: Para Machine Learning.
    *   `Flask` o `FastAPI`: Para el backend web.
*   **Frontend:** HTML, CSS, JavaScript (puro o con una librería ligera como Vue.js/React si se desea más interactividad).
*   **Almacenamiento de Datos:** Archivos CSV/Parquet para el dataset de entrenamiento.

## 6. Consideraciones Clave y Desafíos

*   **Costo Computacional:** El análisis profundo con Stockfish es intensivo en CPU y RAM. Esto impactará el tiempo de respuesta y los costos de hosting. La fase 2 de entrenamiento será la más costosa.
*   **Falsos Positivos:** La calibración del "Índice de Trampa" y la métrica de "Performance ELO" es crucial para evitar marcar a GMs o jugadores que tienen un día excepcional como tramposos. La *naturaleza* de los errores y aciertos es más importante que solo el número.
*   **Calibración del Modelo:** El modelo de "Performance ELO" necesitará ser ajustado y validado cuidadosamente con datos reales.
*   **Gestión de Cargas:** Para la interfaz web, será necesario manejar múltiples solicitudes de análisis, posiblemente con un sistema de cola (ej. Celery + Redis).

## 7. Modelo de Negocio / Estrategia (A considerar)

*   **Modelo "Open Core":** El código del núcleo de análisis (Fase 1) y la metodología de las métricas avanzadas (sección 3) podrían ser de código abierto para fomentar la transparencia y la confianza. Sin embargo, el modelo de Machine Learning entrenado (Fase 3) y la infraestructura de despliegue a escala podrían ser propietarios.
*   **Modelo Freemium:** Ofrecer un análisis gratuito al día (o por semana) con un nivel de profundidad estándar. Funcionalidades premium (análisis de mayor profundidad, análisis por lotes, análisis de historial de jugador, API para integración) podrían ser de pago.

---

## Alcance para la IA Codificadora

Como IA codificadora, se te solicita asistencia en la implementación de las siguientes fases y componentes:

1.  **Fase 1: Núcleo de Análisis (CLI)**
    *   Proporcionar un esqueleto de código Python para la interacción con Stockfish (inicialización, envío de comandos UCI como `position`, `go depth`, `go multipv`, y parsing de las salidas).
    *   Ayudar a estructurar la clase o función principal que toma un PGN, itera jugada por jugada y calcula las métricas básicas y avanzadas por cada posición.
    *   Ejemplos de cómo calcular el ACPL, Accuracy%, y la lógica para el Rango MultiPV y el inicio de la "Puntuación de Horizonte".

2.  **Fase 3: Modelado de "Performance ELO"**
    *   Ofrecer un ejemplo de código Python usando `scikit-learn` o `xgboost` para entrenar un modelo de regresión. Esto incluiría:
        *   Creación de un dataset de datos ficticios (`dummy data`) con métricas y un Elo asociado.
        *   Preprocesamiento básico de los datos.
        *   Entrenamiento de un modelo simple.
        *   Cómo guardar y cargar el modelo entrenado.
        *   Cómo usar el modelo cargado para hacer predicciones.

3.  **Fase 4: Interfaz Web (MVP)**
    *   Proporcionar la estructura básica de una aplicación web con Flask o FastAPI.
    *   Código para un endpoint que acepte un PGN (como texto en el cuerpo de la solicitud).
    *   Integración básica con el núcleo de análisis de la Fase 1 (llamando a las funciones de análisis).
    *   Un ejemplo simple de cómo el backend devolvería un resultado JSON al frontend.
    *   Un esqueleto HTML/JS mínimo para que el usuario pegue el PGN y vea una respuesta básica.

Se espera un enfoque incremental, solicitando código y ejemplos para cada subcomponente a medida que avanzamos en el desarrollo.

---