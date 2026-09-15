# OMDA14 · Preparación docente

## Estado

La prioridad de esta entrega es instalar y comprobar el entorno desde `main`. Los contenidos de FitLife se conservan desde el commit `af557b1cdb1dbd3ea33748a93f46d422a3a30baf` de [MDA13](https://github.com/Kieleth/mda13-fitlife-workshop). Los archivos heredados sin adaptar se comparan mediante SHA-256 en `material_base.json`. La sección `adaptations` registra `paso_0.py`, su hash original y el motivo del cambio.

Se ha importado el material comprometido en Git. Las modificaciones locales de `paso_6.py`, `paso_12.py` y `paso_13.py` no forman parte de esa base. Tampoco se han copiado claves, archivos privados, guiones del profesor ni código de referencia ignorado por Git.

La rama `codex/sesion-1` contiene el paso 0 aprobado: mismo error de import que MDA13, entrada de texto, transformación con Python, contadores y explicación HTML de Streamlit. La guía es [SESION1_PASO0.md](SESION1_PASO0.md). Las siguientes secciones mantienen la propuesta para el resto del curso; los otros ejercicios no se han adaptado todavía.

## Cuatro sesiones de 2 h 30 min

| Sesión | Contenido que se conserva | Qué queremos que el alumno pueda observar |
| :--- | :--- | :--- |
| 1 | Streamlit, datos, chat, primera llamada al LLM, límites de responder con una muestra | Qué texto sale del programa, qué datos se incluyen, dónde se ejecuta cada parte y qué respuesta vuelve |
| 2 | Generación de código, ejecución con Python, errores y autocorrección | La diferencia entre texto generado y un cálculo ejecutado; el código, sus entradas, su resultado y un caso de comprobación |
| 3 | Historial, interpretación y ejemplos en el prompt | Qué historial se reenvía, cómo crece la petición y por qué una pregunta puede provocar dos llamadas al modelo |
| 4 | Caso completo y paso de experimento a aplicación compartida | Reproducir un resultado, explicar sus límites y reconocer qué cambia al compartir la app |

Un resultado ejecutado por Python puede ser incorrecto si el código filtra mal o usa una definición equivocada. Comprobaremos resultados concretos; que una llamada no produzca un error no demuestra que el análisis sea correcto.

## Ramas: propuesta pendiente de aprobación

`main` sería la entrada estable de instalación. Cada rama docente tendría un punto de partida de sesión comprobado y las instrucciones de esa sesión. Cada alumno crearía su propia rama a partir de ella para guardar su trabajo con commits.

Hay una decisión docente pendiente: ramas acumulativas, donde cada sesión parte de la anterior, o puntos de partida independientes, donde nadie necesita haber terminado la sesión anterior. Las independientes facilitan recuperar a quien se haya quedado atrás; las acumulativas hacen visible la evolución de una misma app.

En ambos casos hay que separar la rama del profesor de la rama de trabajo del alumno. Antes de cambiar de sesión se guardan los cambios con un commit. No se debe enseñar a borrar trabajo para que una actualización funcione.

## Primera explicación HTML: recorrido de una petición

La explicación partiría de una pregunta concreta, por ejemplo «¿cuántos registros tiene FitLife?», y permitiría avanzar paso a paso:

1. **Escribes texto.** El navegador recibe una entrada; todavía no se ha llamado al modelo.
2. **La app prepara una petición.** Mostrar exactamente los mensajes y los datos incluidos, con los campos de autenticación ocultos. Un archivo de tu ordenador no aparece automáticamente en el contexto del modelo.
3. **La petición viaja a un servidor.** Comparar la API remota con un servicio que ejecuta un modelo local. Identificar dónde están navegador, proceso Python y modelo.
4. **El modelo procesa tokens.** Distinguir texto, tokens, representaciones numéricas y parámetros aprendidos. Separar entrenamiento de inferencia. Las explicaciones de los cálculos internos serán ilustraciones, no datos medidos dentro de una API cerrada.
5. **Se genera la respuesta.** Explicar la generación autorregresiva de tokens y cómo se devuelve texto a la app.
6. **La pantalla se actualiza.** Comparar respuesta completa y streaming, que entrega fragmentos sucesivos. Un fragmento recibido por la API no equivale necesariamente a un token.
7. **Streamlit vuelve a ejecutar el script.** Mostrar el efecto de un control, qué conserva `session_state` y qué código provoca una llamada al modelo. Streamlit y streaming son conceptos distintos.

Para cada experimento: predecir qué ocurrirá, ejecutar, observar la petición y la respuesta, y explicar la diferencia. Mostrar por separado lo observado y lo ilustrado. No etiquetar una animación como una llamada real.

## Dependencias antes de preparar esas prácticas

Falta decidir el proveedor y modelo para las llamadas, cómo se facilitará el acceso al alumnado y qué equipos tendrán disponibles para una demostración local. No se ha configurado ni probado una API en esta entrega. La instalación inicial no descarga pesos de modelos.

Antes de publicar las sesiones hay que adaptar las instrucciones heredadas de Git y Anaconda, verificar los ejemplos de API con el SDK fijado y revisar las afirmaciones del material antiguo sobre cálculo, tokens, límites de contexto y despliegue. El objetivo es mantener el contenido del curso y mejorar la precisión de las explicaciones.

## Comprobaciones de esta entrega

Desde un entorno del proyecto:

```text
python -m pip install -r requirements.txt
python -m pip check
python check_setup.py
python -m unittest discover -s tests -v
```

GitHub Actions ejecutó correctamente la misma instalación y los trece tests en Windows, macOS y Linux. El commit comprobado, la ejecución y los límites de estas pruebas están registrados en [VERIFICACION.md](VERIFICACION.md).

Las pruebas de Streamlit usan [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest), que simula interacciones con la app. Complementan la comprobación manual en un navegador.

`requirements.in` declara las dependencias directas y `requirements.txt` fija la resolución completa con hashes. Las herramientas para regenerarlo se declaran en `requirements-maintenance.txt`; el alumnado solo necesita `requirements.txt`.
