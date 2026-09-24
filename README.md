# OMDA14 · Analítica conversacional con IA

Construirás paso a paso una aplicación para explorar los datos de FitLife y hacer preguntas a un modelo de lenguaje: añadirás código, probarás lo que cambia y explicarás qué has observado. Las instrucciones sirven para seguirlas en clase o por tu cuenta.

## Antes de clase

1. Si no hiciste la sesión 1, sigue [la guía de instalación](SETUP.md) de tu sistema operativo y lee [el caso FitLife](ENUNCIADO.md).
2. Comprueba que tienes el archivo `.env` con la clave del curso en la raíz del proyecto. Es la misma clave de las sesiones anteriores y se comparte en el chat del curso; la cabecera de `exercises/paso_5.py` explica cómo crear el archivo.

## Durante la clase

Abre la [guía de la sesión 4](SESION4.md). Empieza por «Preparar tu rama»: guarda tu trabajo de la sesión 3 y crea `alumno/sesion-4` a partir de esta rama. Después comprobarás el historial y trabajarás con herramientas, comparación de modelos, revisión con evidencia, documentos y gráficos solicitados en lenguaje natural.

## Ejercicios

Los pasos 0 a 15 están resueltos para repasar y comparar con tu solución. Los pasos 12 a 15 envían también el historial a la API. Los pasos 16 a 21 son los de hoy: cada archivo tiene un punto de partida que funciona y un cambio que construir. A partir del paso 5 hace falta la clave del curso.

| Paso | Qué trabajamos |
| :--- | :--- |
| [0](exercises/paso_0.py) | Sesión 1, resuelto: arrancar la app y leer el primer error. |
| [1](exercises/paso_1.py) | Sesión 1, resuelto: mostrar título y texto. |
| [2](exercises/paso_2.py) | Sesión 1, resuelto: cargar un CSV. |
| [3](exercises/paso_3.py) | Sesión 1, resuelto: explorar los dos datasets y calcular tu verdad. |
| [4](exercises/paso_4.py) | Sesión 1, resuelto: construir un chat eco. |
| [5](exercises/paso_5.py) | Sesión 1, resuelto: conectar con un modelo y ver lo que viaja. |
| [6](exercises/paso_6.py) | Sesión 1, resuelto: preguntar sobre los datos y ver lo que ve el modelo. |
| [7](exercises/paso_7.py) | Sesión 1, resuelto y opcional: añadir contexto y comparar. |
| [8](exercises/paso_8.py) | Sesión 2, resuelto: pedir al modelo el código en vez de la respuesta. |
| [9](exercises/paso_9.py) | Sesión 2, resuelto: extraer el código y ejecutarlo sobre los datos reales. |
| [10](exercises/paso_10.py) | Sesión 2, resuelto: capturar los errores y enseñar el código que se ejecutó. |
| [11](exercises/paso_11.py) | Sesión 2, resuelto y opcional: devolver el error al modelo para que corrija su código. |
| [Extra](exercises/bonus_evaluacion.py) | Sesión 2, resuelto y opcional: medir el sistema con las doce preguntas de test. |
| [12](exercises/paso_12.py) | Guardar la conversación y decidir qué parte recibe el modelo. |
| [13](exercises/paso_13.py) | Una segunda petición que explica el resultado. |
| [14](exercises/paso_14.py) | Ejemplos y reglas en el prompt. |
| [15, opcional](exercises/paso_15.py) | El analista completo, para investigar el caso con las doce preguntas. |
| [16](exercises/paso_16.py) | Conservar, inspeccionar y recuperar una conversación. |
| [17](exercises/paso_17.py) | Ofrecer funciones de Python al modelo y comprobar sus resultados. |
| [18](exercises/paso_18.py) | Comparar modelos con una pregunta y un criterio de acierto. |
| [19](exercises/paso_19.py) | Revisar un análisis contra la evidencia calculada. |
| [20](exercises/paso_20.py) | Cargar documentos, buscar fragmentos y responder con fuentes. |
| [21](exercises/paso_21.py) | Pedir gráficos, comprobar su tabla y añadir una métrica. |

Termina con [la demo compartida y el salto a producción](DE_EXPERIMENTO_A_PRODUCCION.md). El [recorrido visual de las herramientas](explicaciones/herramientas.html) permite seguir una petición simulada sin usar la API.

Las 12 preguntas con las que evaluaremos el sistema en todas las sesiones están en [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md).
