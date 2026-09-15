# Construimos nuestra primera app

**Esta actividad se hace en clase. Espera a que Luis indique cada ronda.** Partimos de tres líneas de Python y construiremos una app que recibe un mensaje, lo transforma y lo muestra.

Trabajad por parejas: una persona escribe y la otra predice qué ocurrirá. Cambiad los papeles en la siguiente ronda. Cuando lleguéis a «Pausa», contrastad lo observado con Luis antes de seguir.

## 1. Nuestro espacio de trabajo

Una rama guarda una línea de trabajo en Git. La rama del profesor contiene los archivos de partida; tu rama guardará tus cambios. Al cambiar de rama pueden cambiar los archivos que ves en VS Code. Seguimos en la misma carpeta y usamos el mismo entorno `.venv`.

Abre `omda14-fitlife-workshop` en VS Code y **Terminal > New Terminal**. Si sigue abierta la app de instalación, pulsa `Ctrl+C` en su terminal para pararla. Comprueba el estado:

```text
git status
```

Si aparece `nothing to commit, working tree clean`, no hay cambios pendientes. Si aparece una lista de archivos modificados, enséñasela a Luis antes de cambiar de rama; [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservarlos.

Cuando Luis lo indique:

```text
git fetch origin
git switch -c alumno/sesion-1 origin/codex/sesion-1
git branch --show-current
```

`fetch` descarga los puntos de partida publicados. `switch -c` crea tu rama desde el de la clase. El último comando debe mostrar `alumno/sesion-1`. No necesitas permiso para escribir en el GitHub del profesor: trabajarás en tu copia local.

Si ya creaste tu rama antes, usa `git switch alumno/sesion-1` para volver a ella. Crear y volver a una rama son acciones distintas.

**Pausa:** localiza `exercises/paso_0.py` en el explorador de VS Code y ábrelo.

## 2. Leer el primer error

Streamlit es la librería de Python que permite mostrar elementos en el navegador. `import` carga una librería; `as st` le da un nombre corto para usarla en este archivo.

Desde la terminal del proyecto, ejecuta solo el comando de tu sistema:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_0.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_0.py
```

Abre la dirección local que aparezca en la terminal. Hay una errata intencionada: `ModuleNotFoundError` dice que Python no encuentra el módulo que intenta cargar. Compara su nombre con «Streamlit». Corrige solo ese nombre en la línea `import` y guarda con `Ctrl+S` o `Cmd+S`.

Si aparece **Rerun** en el navegador, púlsalo. **Always rerun** permite repetir automáticamente al guardar los siguientes cambios. Mantén abierta la terminal que ejecuta Streamlit.

**Pausa:** deberías ver un título y un mensaje. Señala qué línea produce cada uno.

## 3. Hacerla nuestra

**Predice:** si cambias un texto en el archivo, ¿qué parte de la página cambiará?

En `st.title("Hola, FitLife")`, cambia únicamente el texto entre comillas por el nombre de vuestro equipo. Conserva la función, los paréntesis y las comillas. En la última línea, escribe vuestro propio mensaje de bienvenida. Guarda y observa.

**Pausa:** enseña a tu pareja la relación entre una línea y lo que aparece en la página. Todavía no hemos añadido una entrada para el usuario.

## 4. Recibir un mensaje

Luis introducirá las variables: un nombre que permite utilizar un valor después. Añade estas dos líneas **al final del archivo**, debajo de la bienvenida:

<!-- build:entrada -->
```python
mensaje = st.text_input("Mensaje", "Hola, FitLife")
st.write(mensaje)
```

**Antes de probar:** señala qué texto crees que aparecerá en la entrada y dónde se mostrará lo que escribas.

Guarda. Escribe una frase distinta en **Mensaje** y pulsa Intro. Prueba también a borrar el texto.

**Pausa:** explica qué valor guarda `mensaje`. La línea que crea la entrada debe ir antes de la que usa su valor.

## 5. Cambiar lo que hace Python

**Predice:** queremos mostrar el mensaje en mayúsculas. ¿Dónde pondrías esa transformación: antes o después de mostrarlo?

Con Luis, sustituye **solo** la línea `st.write(mensaje)` que acabas de añadir por estas dos:

<!-- build:transformacion -->
```python
resultado = mensaje.upper()
st.write(resultado)
```

Guarda y prueba una frase con mayúsculas y minúsculas. Después, cada pareja cambia `upper()` por `lower()` y explica qué ha cambiado en la regla. Conserva la versión que hayas probado.

**Pausa:** señala la entrada, la transformación y la salida en tu código. ¿Qué habéis construido que no estaba al arrancar?

## 6. Ver la ejecución en la terminal

**Predice antes de añadirlo:** ¿dónde aparecerá un `print`? ¿Es el mismo sitio que un `st.write`?

Añade esta línea **al final del archivo**, después de mostrar el resultado:

<!-- build:traza -->
```python
print("Entrada:", mensaje, "| Salida:", resultado)
```

Guarda, cambia el mensaje y pulsa Intro. Mira el navegador y la terminal donde arrancaste Streamlit. Compara los valores con tu pareja.

Ahora añade esta línea **justo después del import**, antes del título:

<!-- build:arranque -->
```python
print("Se ejecuta paso_0")
```

**Predice:** al cambiar el mensaje, ¿veremos otra vez esa línea aunque esté antes de la entrada? Haz la prueba y cuéntale a Luis qué has observado.

**Pausa:** hemos construido entrada, transformación, salida y una traza. Una traza es un mensaje que nos ayuda a observar lo que ejecuta el programa.

## 7. Explicarlo y guardar nuestro trabajo

Luis utilizará `explicaciones/streamlit.html` para recorrer navegador → servidor de Streamlit → Python → navegador. Si os pide abrirlo, usa Finder o el Explorador de archivos y haz doble clic en el archivo. Es una simulación: compárala con lo que acabas de observar en tu programa.

Para guardar la versión que has construido, abre **otra terminal** del proyecto con **Terminal > New Terminal**. La primera puede seguir ejecutando la app. Ejecuta:

```text
git diff -- exercises/paso_0.py
git add exercises/paso_0.py
git commit -m "Construyo mi primera app"
git status
```

`diff` muestra tus cambios. Si ocupa una pantalla con `(END)`, pulsa `q` para volver a la terminal. `add` selecciona este archivo para guardarlo. `commit` registra esa versión en tu rama. `status` debe terminar con `nothing to commit, working tree clean`. Si Git pide nombre y correo, Luis os guiará con [ACTUALIZAR.md](ACTUALIZAR.md). El commit queda en tu ordenador; no hay que publicarlo para completar la práctica.

**Cierre con Luis:** explica quién recibe el texto, qué línea lo transforma y dónde se ejecuta Python. Este programa aplica la regla que hemos escrito; aún no hemos conectado un modelo de lenguaje.
