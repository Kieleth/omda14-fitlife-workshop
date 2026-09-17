# Sesión 1: de una página web a un modelo de lenguaje

Esta guía acompaña los ejercicios `exercises/paso_0.py` a `paso_7.py`. Puedes seguirla en clase o por tu cuenta. Cada ejercicio lleva sus instrucciones en la cabecera del archivo; aquí está el hilo de la sesión, lo que debes ver antes de pasar al siguiente paso y las explicaciones que no caben en un comentario. No contiene las soluciones.

## Qué vas a construir

Una app web en tu portátil que carga los datos de FitLife, tiene un chat y envía tus preguntas a un modelo de lenguaje. Por el camino verás qué sale exactamente de tu ordenador cuando pulsas Enter, qué recibe el modelo, qué devuelve y dónde están sus límites. Al terminar sabrás qué puede hacer un modelo con una tabla de datos, qué no, y por qué.

Necesitas la instalación de [SETUP.md](SETUP.md) y, a partir del paso 5, la clave del curso. Las dos páginas de `explicaciones/` son simulaciones que se abren con doble clic y no tocan tu app; la guía indica cuándo abrirlas.

## Cómo se trabaja cada paso

1. Abre el archivo del paso en VS Code y lee la cabecera: explica el concepto, el reto y unas pruebas opcionales.
2. Arranca la app desde la terminal del proyecto con el comando de tu sistema, cambiando el nombre del archivo:

   Windows:

   ```powershell
   .venv\Scripts\python.exe -m streamlit run exercises/paso_1.py
   ```

   macOS:

   ```bash
   .venv/bin/python -m streamlit run exercises/paso_1.py
   ```

3. Lee lo que aparece. Un error es información: la terminal dice qué falta y en qué línea.
4. Corrige o completa, guarda con `Ctrl+S` o `Cmd+S` y mira el navegador. Si aparece **Rerun**, púlsalo; **Always rerun** lo hace solo a partir de entonces.
5. Cada paso tiene una **puerta**: lo que debes ver en pantalla para darlo por terminado. Las pruebas opcionales de la cabecera son para quien quiera más.
6. Para el siguiente paso, pulsa `Ctrl+C` en la terminal de la app y repite el comando con el archivo nuevo.

Los huecos `___` son código que falta. Borra el hueco y escribe lo que pide el comentario que tiene encima. Cuando el hueco va entre llaves, `{___}`, las llaves se quedan y solo cambia lo de dentro.

## Preparar tu rama

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

## Paso 0: arranca tu primera app

El reto es leer un error, corregirlo y ver tu primera página web. Al aparecer el título y el mensaje, has completado el paso.

### Arrancar, leer el error y corregirlo

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

### Si has terminado antes

Son pruebas opcionales del mismo programa; las mismas están en la cabecera del archivo.

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

### Ver qué ocurre entre guardar y ver el cambio

**Simulación 1: `explicaciones/streamlit.html`.** Localízalo en Finder o el Explorador de archivos y haz doble clic. Recorre el cambio de título desde el editor hasta el navegador: editas el archivo, lo guardas, Streamlit ejecuta Python y actualiza la página. Es una simulación, no está conectada a tu app.

### Guardar el paso en Git

Para registrar tu versión en Git, abre **otra terminal** del proyecto con **Terminal > New Terminal**. La primera puede seguir ejecutando la app.

```text
git diff -- exercises/paso_0.py
git add exercises/paso_0.py
git commit -m "Completo el paso 0"
git status
```

`diff` muestra tus cambios. Si ocupa una pantalla con `(END)`, pulsa `q` para volver a la terminal. `add` selecciona este archivo para guardarlo. `commit` registra esa versión en tu rama. `status` debe terminar con `nothing to commit, working tree clean`. Si Git pide nombre y correo, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo configurarlos. El commit queda en tu ordenador; no hay que publicarlo para completar la práctica.

**Siguiente: [paso_1.py](exercises/paso_1.py).** Pulsa `Ctrl+C` en la terminal de la app y repite el comando de arranque cambiando `paso_0.py` por `paso_1.py`. Los pasos 1 a 7 se guardan en Git al final de la sesión.

## Paso 1: título y texto

**Qué haces.** Dos huecos: un subtítulo y un texto. El comentario encima de cada hueco dice qué escribir.

**Qué hay detrás.** Cada llamada `st.algo(...)` añade un elemento a la página, en el orden en que aparece en el código. `st.write` acepta Markdown: `**negrita**`, `*cursiva*`, `` `código` ``.

**Puerta.** Título, subtítulo y texto, en ese orden. Si falta uno, mira si la línea sigue siendo `___` o si se ha quedado mal escrita.

**Si has terminado antes.** La cabecera propone `st.markdown`, `st.metric` y `st.divider`. Pruébalos y quítalos después, o déjalos: son tu app.

## Paso 2: cargar un CSV

**Qué haces.** La app arranca y falla al leer el archivo. Lee el error: dice qué archivo busca y no encuentra. Compara con la carpeta `data/`.

**Qué hay detrás.** Una ruta es relativa a la carpeta desde la que arrancaste la app, que es la raíz del proyecto, no la carpeta `exercises/` donde está el archivo. `pd.read_csv` convierte el CSV en un DataFrame: una tabla con filas y columnas.

**Puerta.** La tabla en pantalla y el texto «16.334 filas y 15 columnas».

**Si has terminado antes.** `df.head(10)`, `df.describe()` y `df["plan"].value_counts()` están en la cabecera. Fíjate en lo que devuelve `value_counts`: lo vas a necesitar.

## Paso 3: los dos datasets

**Qué haces.** El primer dataset ya está cargado. Dos huecos para cargar el segundo y describirlo, siguiendo el patrón de las líneas de arriba.

**Qué hay detrás.** Cada fila de `fitlife_members.csv` es un socio en un mes concreto: 16.334 filas de 940 socios. `fitlife_context.csv` tiene una fila por mes, 36 en total. La columna `month` permite unirlos.

**Puerta.** Las dos tablas con su número de filas y columnas.

**Tu verdad para el resto de la sesión.** Antes de preguntar a un modelo, calcula tú. Añade al final del archivo y ejecuta:

```python
st.write(df_members["status"].value_counts())
st.write(df_members["center"].value_counts())
st.write(df_members[df_members["plan"] == "basic"]["status"].value_counts())
```

La primera línea cuenta activos y bajas. La segunda, filas por centro. La tercera cruza plan y estado: las bajas del plan básico entre el total de filas del básico es su tasa de churn. Apunta los tres resultados. Son la referencia contra la que juzgarás al modelo en los pasos 6 y 7.

## Paso 4: un chat que repite

**Qué haces.** Un hueco dentro del bloque del asistente para que la app repita lo que escribes.

**Qué hay detrás.** `st.chat_input` devuelve el texto escrito o `None` si no hay nada. `st.chat_message` crea un bocadillo, y todo lo indentado bajo su `with` se pinta dentro. Con tres piezas tienes la interfaz completa de un chat. Lo único que va a cambiar de aquí en adelante es lo que ocurre dentro del bocadillo del asistente.

**Puerta.** Escribes algo y el asistente lo repite.

## Paso 5: conectar un modelo

**Qué haces.** Crea el archivo `.env` en la raíz con la clave del curso, siguiendo los pasos de la cabecera (`.env.template` muestra el formato). Completa el hueco que crea el cliente. Pregunta cualquier cosa.

Si al arrancar aparece «Missing credentials», el archivo `.env` no existe o no se llama exactamente así.

**Qué hay detrás.** Una API es una puerta: tu programa envía un texto a una dirección de internet, con una cabecera que lleva tu clave, y recibe otro texto. Lo que viaja es JSON, un formato de texto para escribir datos con llaves, comillas y comas. En la petición van dos campos: el nombre del modelo y `messages`, una lista donde cada entrada dice quién habla (`role`) y qué dice (`content`). La respuesta también es JSON, y la frase que ves en el bocadillo es un solo campo dentro de ella, `choices[0].message.content`. Al lado viene `usage`, que cuenta tokens: los trozos de texto con los que trabaja el modelo, una palabra corta o media palabra cada uno.

**Mira lo que viaja.** La cabecera tiene la sección «Mira lo que viaja» con cinco líneas para pegar al final del archivo. Copia las líneas, quita el `# ` del principio de cada una y deja cuatro espacios delante de `with`. Guarda, pregunta algo y abre los dos desplegables. En el primero está exactamente lo que ha salido de tu ordenador. En el segundo, todo lo que ha vuelto. Busca en él el campo que muestra la app y el recuento de tokens.

**Simulación 2: `explicaciones/api.html`, con la casilla «Con contexto» desmarcada.** Recorre las seis estaciones con tu pregunta: la app, el JSON que construye Python, lo que viaja por internet, el modelo leyendo tokens, el JSON que vuelve y el campo que extrae la app. Compara la estación 3 con tu desplegable «Lo que enviamos».

**Prueba.** Pregunta «¿Qué sabes sobre FitLife, una red de gimnasios?». Lee la respuesta con calma: ¿sabe algo de nuestro caso? ¿De dónde podría saberlo, si en el JSON solo va tu pregunta?

**Puerta.** Una respuesta del modelo y los dos desplegables abiertos.

## Paso 6: pregunta por los datos

**Qué haces.** Nada está roto. Antes de ejecutar, lee la variable `context` en el código: es lo que la app añade a cada petición, con rol `system`. Fíjate en cuántas filas de la tabla incluye. Después haz las cinco preguntas de la cabecera y anota, para cada una, si la respuesta es correcta, parcial o inventada, y cómo lo sabes. Tus números del paso 3 son la referencia.

**Mira exactamente lo que ve el modelo.** Pega las seis líneas de la sección de la cabecera, como en el paso 5. Abre «Lo que enviamos» y lee el `content` del `system` hasta el final. ¿Cuántos socios distintos aparecen en las filas? ¿Cuántos planes? ¿Cuántos centros? Vuelve a la pregunta del centro con más socios con eso delante.

**Qué hay detrás.** El modelo no tiene el CSV, ni tu pregunta anterior, ni las de tus compañeros. Tiene este JSON y nada más. Cuando le preguntas por algo que exige contar filas que no están, no puede contarlas; escribe el texto que mejor encaja con lo que tiene delante. A veces eso es un número. Ese número no sale de un cálculo, sale del mismo mecanismo que las palabras de alrededor.

**Simulación 3: `explicaciones/api.html`, con la casilla «Con contexto» marcada.** Estación 2: las cinco filas dentro del texto del `system`. Estación 4: la barra de tokens, con lo que pesa esta petición, la tabla entera y el límite del modelo.

**Prueba A de la cabecera.** Si a la pregunta de la tasa de churn responde explicando un procedimiento en vez de dar un número, pide «Dame solo el porcentaje, sin explicar el procedimiento». Hazlo tres veces. Compara con tu número del paso 3. Si cambia entre intentos, no lo está calculando. Si coincide tres veces, tampoco: un número que no sale de contar las filas es un número inventado.

**Puerta.** Tu tabla de cinco preguntas rellena y la respuesta a «¿cuántos socios distintos ve el modelo?».

## Paso 7: contexto de verdad

**Qué haces.** Cuatro huecos entre llaves en el prompt: cada uno es una variable ya calculada más arriba en el código. Después repite las cinco preguntas y compara con el paso 6, pregunta por pregunta.

**Qué hay detrás.** Ahora el `system` lleva las distribuciones por plan, centro, estado y canal, y el contexto mensual completo. Responde a esto con tus resultados delante: ¿qué preguntas contesta ahora que antes no? ¿Estaba la respuesta escrita en el prompt? ¿Qué pregunta sigue sin poder contestar, y qué cruce de columnas le faltaría? Lee las últimas líneas del prompt y compáralas con lo que de verdad le hemos dado.

**Reto E: el límite.** Con el bloque del paso 6 pegado aquí, anota `prompt_tokens` con `head()`. Cambia `head()` por `head(50)`, repite la pregunta y anota de nuevo. Resta, divide entre 45 y tienes los tokens por fila; multiplica por 16.334. Compara con el límite del modelo que da la cabecera. Si pruebas `df_members.to_string()`, la petición falla con «Request too large» y el error te dice cuántos tokens contó: con la clave del curso no cuesta nada probarlo.

**Retos A a D.** Temperatura, persona, inyección de instrucciones y memoria. Son opcionales; el D abre una pregunta que se trabaja en la sesión 3.

**Puerta.** Tu comparación paso 6 frente a paso 7 rellena.

## Cierre: lo que has visto

Responde por escrito, con tus palabras, sin abrir nada:

- ¿Qué sale de tu portátil cuando pulsas Enter en el chat? ¿En qué formato y con qué campos?
- ¿Qué tiene delante el modelo cuando responde? ¿Qué no tiene?
- ¿Por qué inventa una tasa de churn y no inventa un NPS?
- ¿Qué es un token y dónde está el límite de lo que puedes enviar?

Si puedes contestar las cuatro, puedes dibujar en una pizarra lo que ha pasado en esta sesión.

Guarda tu trabajo en Git desde la terminal del proyecto:

```text
git add exercises
git commit -m "Completo la sesión 1"
git status
```

`add exercises` selecciona los archivos de esa carpeta que has cambiado. Ni `.env` ni `.venv` entran: Git los ignora.

Las doce preguntas de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md) se repiten en cada sesión para medir cómo mejora el sistema. En la sesión 2, en vez de pedirle al modelo la respuesta, le pediremos el código que la calcula.
