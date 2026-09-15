# Sesión 1 · Paso 0: ver Streamlit por dentro

Partimos del mismo reto de MDA13: la app no arranca por un error en el import. Después observaremos qué ocurre cuando el navegador recibe texto y Python actualiza la página.

## 1. Prepara tu rama

Completa primero [SETUP.md](SETUP.md) en `main`. La misma `.venv` sirve para este ejercicio. Desde la raíz del proyecto:

```text
git status
```

Si tienes cambios pendientes, guárdalos siguiendo [ACTUALIZAR.md](ACTUALIZAR.md). Con la carpeta sin cambios pendientes, descarga las ramas y crea tu rama de trabajo:

```text
git fetch origin
git switch -c alumno/sesion-1 origin/codex/sesion-1
git branch --show-current
```

El último comando debe mostrar `alumno/sesion-1`. Cada alumno tiene su propia copia del repositorio, así que puede usar ese mismo nombre. Si ya creaste esa rama antes, vuelve a ella con `git switch alumno/sesion-1`; no repitas el comando de creación. No necesitas permiso para escribir en el repositorio del profesor: estos cambios y commits son locales.

## 2. Lee el error y arranca la app

Ejecuta según tu sistema desde la carpeta del proyecto:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_0.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_0.py
```

Abre la dirección que muestre la terminal. Verás un `ModuleNotFoundError` intencionado. Compara el nombre del módulo en `exercises/paso_0.py` con la librería que acabas de comprobar en `test_app.py`. Corrige ese nombre y guarda.

Si Streamlit te ofrece **Rerun**, púlsalo. Puedes activar **Always rerun** para los siguientes cambios. No hace falta parar y arrancar el servidor cada vez que editas el archivo. Al ver «Hola, FitLife», ya has resuelto el reto original.

## 3. Predice, prueba y explica

Trabajad por parejas: una persona hace una predicción y la otra cambia el código o la entrada. Comparad la predicción con la pantalla y la línea `[paso_0]` de la terminal. Después intercambiad los papeles.

| Antes de actuar, predice | Qué haces | Qué debes observar |
| :--- | :--- | :--- |
| ¿Dónde aparecerá el texto? | Escribe `Hola, Madrid` en Mensaje y pulsa Intro. | Python recibe ese texto; el navegador muestra `HOLA, MADRID`; aparece una línea en la terminal. |
| ¿Se ejecuta solo la línea que cambia? | Pulsa «Volver a ejecutar sin cambiar el mensaje». | El contador de la sesión aumenta, pero el contador local vuelve a 1. La salida conserva el mismo texto. |
| ¿Es HTML o Python lo que editamos? | Cambia `titulo` por `El gimnasio de nuestro equipo`, guarda y ejecuta de nuevo. | Cambia el título de la página. |
| ¿Quién decide la transformación? | Sustituye `mensaje.upper()` por `mensaje.lower()`, guarda y prueba de nuevo. | El mismo texto ahora aparece en minúsculas. Puedes señalar la línea que lo produce. |
| ¿Qué queda al abrir otra sesión? | Recarga la pestaña del navegador. | Se reinicia el contador de sesión y vuelve el texto inicial. La función que editaste sigue cambiada porque está guardada en el archivo. |
| ¿Hay una respuesta escondida? | Borra el mensaje y pulsa Intro. | Entrada y salida son `''`, una cadena vacía. Python no inventa un mensaje. |

El número exacto de ejecuciones depende de las acciones que hagáis, incluidos los cambios de código. Comparad el contador antes y después de cada acción, sin asumir que siempre estará en un número concreto.

## 4. Recorre la explicación HTML

Abre `explicaciones/streamlit.html` con doble clic desde Finder o el Explorador de archivos. Funciona sin instalar nada más. Elige una entrada y avanza por el recorrido navegador → servidor de Streamlit → Python → navegador.

**Es una simulación didáctica.** Sus pasos y valores no están conectados con tu app. Úsala para explicar lo que has observado en la ejecución real. No tiene un modelo de lenguaje ni envía tu texto a un servicio.

En el programa real, `print(...)` escribe en la terminal. `st.code(...)` muestra valores en la página. El texto que ves es una transformación programada, no una respuesta generada por un LLM. Una API de un LLM será otra llamada que añadiremos más adelante.

## 5. Guarda tu primer cambio con Git

Después de corregir el import y probar tus cambios:

```text
git diff -- exercises/paso_0.py
git add exercises/paso_0.py
git commit -m "Paso 0: entiendo entrada, ejecucion y salida"
git status
```

Si Git pide tu nombre y correo, sigue [ACTUALIZAR.md](ACTUALIZAR.md). El commit guarda tu versión en tu rama local. No es necesario hacer push para completar este paso.

## Para terminar

Explica a tu pareja dónde se ejecuta Python, por qué el contador local vuelve a 1 y dónde añadirías una llamada a un LLM. Señala qué has visto de verdad y qué has recorrido en la simulación.

Referencias: [comportamiento de los controles de Streamlit](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior), [estado de sesión](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state), [cambio de rama con Git](https://git-scm.com/docs/git-switch).
