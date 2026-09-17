# Paso 0: arranca tu primera app

El reto es leer un error, corregirlo y ver tu primera página web. Al aparecer el título y el mensaje, has completado el paso. Puedes seguirlo en clase o por tu cuenta.

## Preparar nuestra rama

Una rama guarda una línea de trabajo en Git. Vamos a usar tres. `main` trae la preparación que instalaste en casa. La rama de la clase se publica antes de cada sesión con los ejercicios de ese día. Tu rama, `alumno/sesion-1`, la creas ahora a partir de la de la clase, y en ella quedan tus cambios.

¿Por qué no editar directamente los archivos de `main`? Porque para la sesión 2 se publicará otra rama con archivos nuevos y querrás descargarla sin perder lo que escribas hoy. Con tu rama, lo de hoy queda guardado en tu ordenador y la sesión 2 empieza desde su propia rama. Al cambiar de rama pueden cambiar los archivos que ves en VS Code. Seguimos en la misma carpeta y usamos el mismo entorno `.venv`.

Abre `omda14-fitlife-workshop` en VS Code y **Terminal > New Terminal**. Si sigue abierta la app de instalación, pulsa `Ctrl+C` en su terminal para pararla. Comprueba el estado:

```text
git status
```

Si aparece `nothing to commit, working tree clean`, no hay cambios pendientes. Si aparece una lista de archivos modificados, haz un commit antes de cambiar de rama; [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo.

Crea tu rama:

```text
git fetch origin
git switch -c alumno/sesion-1 origin/clase/sesion-1
git branch --show-current
```

`fetch` descarga lo publicado para la clase; `origin/clase/sesion-1` es el nombre de la rama de la clase en GitHub. `switch -c` crea tu rama desde ese punto de partida. El último comando debe mostrar `alumno/sesion-1`. Trabajarás en tu copia local, sin necesidad de permiso para escribir en el GitHub del curso.

Si ya has creado tu rama, usa `git switch alumno/sesion-1` para volver a ella. Crear y volver a una rama son acciones distintas.

## Arrancar, leer el error y corregirlo

Abre `exercises/paso_0.py` en VS Code. Streamlit es una librería de Python que permite mostrar elementos en el navegador. `import` carga una librería; `as st` le da un nombre corto para utilizarla en este archivo.

Desde la terminal del proyecto, ejecuta solo el comando de tu sistema:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_0.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_0.py
```

Si no se abre el navegador, abre la dirección **Local URL** que aparece en la terminal. Mantén abierta esa terminal: está ejecutando la app.

Hay una errata intencionada. Lee el error en el navegador o la terminal: `ModuleNotFoundError` indica que Python no encuentra un módulo. ¿Qué nombre está buscando? Compáralo con el nombre de la librería.

Corrige la errata en el import y guarda con `Ctrl+S` en Windows o `Cmd+S` en macOS. Si aparece **Rerun** en el navegador, púlsalo. **Always rerun** permite repetir automáticamente al guardar los siguientes cambios.

**Cuando veas «Hola Mundo» y el mensaje, has completado el paso 0.** Señala qué línea genera el título y cuál genera el texto.

## Si has terminado antes

Son pruebas opcionales del mismo programa.

**A. Cambia un texto.** En `st.title("Hola Mundo")`, cambia solo el texto entre comillas por el nombre de tu equipo. Predice qué parte de la página cambiará. Guarda y compruébalo. Prueba también con el texto de `st.write`, manteniendo las comillas y los paréntesis.

**B. Añade un efecto.** Añade al final del archivo:

<!-- optional:globos -->
```python
st.balloons()
```

Guarda y observa. Después sustituye esa misma línea por:

<!-- optional:nieve -->
```python
st.snow()
```

**C. Prueba un control.** Añade al final:

<!-- optional:slider -->
```python
st.slider("Tu edad", 0, 100, 25)
```

Guarda y mueve el control en el navegador. ¿Qué ha añadido esa línea a tu página?

## Ver qué ocurre y continuar

Para ver qué ocurre entre guardar el archivo y ver el cambio, abre `explicaciones/streamlit.html`: localízalo en Finder o el Explorador de archivos y haz doble clic. Recorre el cambio de título desde el editor hasta el navegador: editas el archivo, lo guardas, Streamlit ejecuta Python y actualiza la página. Es una simulación, no está conectada a tu app.

Para registrar tu versión en Git, abre **otra terminal** del proyecto con **Terminal > New Terminal**. La primera puede seguir ejecutando la app.

```text
git diff -- exercises/paso_0.py
git add exercises/paso_0.py
git commit -m "Completo el paso 0"
git status
```

`diff` muestra tus cambios. Si ocupa una pantalla con `(END)`, pulsa `q` para volver a la terminal. `add` selecciona este archivo para guardarlo. `commit` registra esa versión en tu rama. `status` debe terminar con `nothing to commit, working tree clean`. Si Git pide nombre y correo, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo configurarlos. El commit queda en tu ordenador; no hay que publicarlo para completar la práctica.

**Siguiente: [paso_1.py](exercises/paso_1.py), mostrar título y texto.** Pulsa `Ctrl+C` en la terminal de la app y repite el comando de arranque cambiando `paso_0.py` por `paso_1.py`.
