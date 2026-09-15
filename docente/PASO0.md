# Paso 0: guía para Luis

## Objetivo y cierre

El mismo que en MDA13: arrancar la app, leer el error del import, corregirlo y ver el título y el mensaje. Ese es el punto de finalización. La guía del alumno está en [SESION1_PASO0.md](../SESION1_PASO0.md).

## Preguntas para acompañar el ejercicio

Antes de corregir, pedir que localicen el nombre de la librería en el error y en el código. Después, relacionar st.title y st.write con la página. El import carga la librería, no crea un elemento visible.

Si se cambia un texto, pedir una predicción antes de guardar. Después de guardar, ejecutar Rerun si aparece o activar Always rerun. Con Auto Save en VS Code, el archivo puede guardarse automáticamente: no prometer que el navegador seguirá igual hasta pulsar una tecla concreta.

El HTML de explicaciones/streamlit.html acompaña ese mismo cambio: editor, archivo guardado, servidor que ejecuta Python y navegador. Es una ilustración, no una lectura de la app. Luis decide cuándo mostrarla.

## Ampliaciones originales, opcionales

Cambiar el título o el mensaje; añadir st.balloons() y sustituirlo por st.snow(); añadir el slider de edad. Basta observar sus efectos. El slider ya provoca una nueva ejecución cuando cambia su valor, pero aquí no hace falta guardar ese valor ni añadir cálculos.

Una explicación verbal o señalar las líneas en pantalla basta para seguir la ejecución. No se exige añadir trazas, variables ni transformaciones. El chat eco se construye en paso_4, en su lugar dentro del curso.

## Continuación

Guardar los cambios en la rama del alumno con las instrucciones de la guía y pasar a paso_1, título y texto. Los pasos 1 a 7 están en exercises/ con el código del material base. Solo se han actualizado referencias de instalación y el nombre de la carpeta en los comentarios.

Los pasos 1, 3, 4, 5 y el bonus 7 describen huecos que ya están resueltos en esa versión. Antes de impartirlos, revisar con Luis qué líneas se entregan para completar. Esta corrección conserva su código y no inventa otro reto.

Las pruebas comprueban la equivalencia del código inicial con el original, el error esperado, su corrección, los cambios de texto y las ampliaciones opcionales. No comprueban llamadas reales a un LLM.

Fuente: [ciclo de edición y ejecución de Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts).
