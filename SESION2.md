# Sesión 2: que el modelo escriba el código y que Python calcule

Esta guía acompaña los ejercicios `exercises/paso_8.py` a `paso_11.py`. Puedes seguirla en clase o por tu cuenta. Los pasos 0 a 7 están en esta rama en su versión terminada: son la sesión 1 resuelta, para repasar y para comparar con la tuya. Cada ejercicio lleva sus instrucciones en la cabecera del archivo; aquí está el hilo de la sesión, lo que debes ver antes de pasar al siguiente paso y las explicaciones que no caben en un comentario. No contiene las soluciones. Las páginas de `explicaciones/` son simulaciones que se abren con doble clic y no tocan tu app; hoy hay una nueva, `codigo.html`, y la guía indica cuándo abrirla.

## Qué vas a construir

El mismo chat de la sesión 1, con un cambio en lo que le pedimos al modelo: en vez de la respuesta, el código que la calcula. Tu app extrae ese código de la respuesta, lo ejecuta sobre las 16.334 filas de verdad y enseña el resultado. Por el camino verás que el código llega como texto dentro del mismo JSON de siempre, que el número ya no sale del modelo sino de pandas, qué pasa cuando el código falla y qué pasa cuando no falla pero calcula lo que nadie pidió, y cómo el modelo corrige su propio código si le devuelves el error.

Necesitas la instalación de [SETUP.md](SETUP.md) y el archivo `.env` con la clave del curso, la misma de la sesión 1 y de todo el taller. La clave se comparte en el chat del curso; si no la tienes, pídela ahí. La cabecera de `exercises/paso_5.py` explica cómo crear el archivo.

## Preparar tu rama

En la sesión 1 creaste `alumno/sesion-1` y trabajaste en ella. Hoy se publica `clase/sesion-2`, con los pasos 0 a 7 terminados y los 8 a 11 nuevos. Vas a crear `alumno/sesion-2` a partir de ella. Tu trabajo de la sesión 1 se queda en `alumno/sesion-1`, intacto.

Abre el proyecto en VS Code y **Terminal > New Terminal**. Si hay una app de Streamlit corriendo en otra terminal, párala con `Ctrl+C`. Mira dónde estás y qué tienes pendiente:

```text
git branch --show-current
git status
```

Si `status` lista archivos modificados o sin seguimiento, guárdalos primero en tu rama de la sesión 1. Git no cambia de rama si hay cambios sin guardar en archivos que la otra rama trae distintos, y hoy los trae todos. Si no tienes `mis_notas.md`, la segunda línea da un error y no pasa nada: el commit guarda lo demás.

```text
git add exercises
git add mis_notas.md
git commit -m "Mi sesión 1"
git status
```

`status` debe terminar en `nothing to commit, working tree clean`. Si no, mira qué archivo queda y añádelo antes de seguir. Ahora descarga la rama de la clase y crea la tuya:

```text
git fetch origin
git switch -c alumno/sesion-2 origin/clase/sesion-2
git branch --show-current
```

Si Git dice que `alumno/sesion-2` ya existe, es que ya la creaste: `git switch alumno/sesion-2`. Estos comandos funcionan desde cualquier rama, también desde `main` si empiezas hoy; si `git status` muestra cambios ahí, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservarlos.

Mira la carpeta `exercises/`: hay trece archivos, los doce pasos y un ejercicio extra. Abre `paso_5.py`: el hueco de `client` está relleno y los desplegables están pegados al final. Es la versión terminada, no la tuya. La tuya sigue en la otra rama. Compárala con el último archivo que tocaste, cambiando `paso_6` por el que sea:

```text
git diff alumno/sesion-1 -- exercises/paso_6.py
```

Las líneas con `-` son de tu versión y las de `+`, de la terminada. Verás al menos la línea del título, que ahora dice «(resuelto)». Si ocupa una pantalla con `(END)`, pulsa `q`.

Tus notas se quedaron en `alumno/sesion-1` con el resto de tu trabajo, y `mis_notas.md` ya no está en la carpeta. Compruébalo antes de seguir: si lo ves en la carpeta, sáltate este bloque, porque `restore` lo sustituiría por la versión de la otra rama, o lo borraría si allí no existe. Si no está, tráelo:

```text
git restore --source=alumno/sesion-1 -- mis_notas.md
git add mis_notas.md
git commit -m "Traigo mis notas"
```

`restore --source` copia un archivo tal como está en otra rama, sin tocar nada más. Si Git dice que no encuentra el archivo en esa rama, es que nunca lo guardaste con un commit. Si nunca creaste `mis_notas.md`, créalo ahora en la raíz del proyecto: hoy también hay cosas que apuntar.

## Cómo se trabaja cada paso

Igual que en la sesión 1. Abres el archivo del paso en VS Code y lees la cabecera. Arrancas la app desde la terminal del proyecto con el comando de tu sistema, cambiando el nombre del archivo:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_8.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_8.py
```

Corriges o completas, guardas con `Ctrl+S` o `Cmd+S` y miras el navegador; si aparece **Rerun**, púlsalo. Cada paso tiene una **puerta**: lo que debes ver en pantalla para darlo por terminado. Para el siguiente paso, `Ctrl+C` en la terminal de la app y el comando con el archivo nuevo. Para los comandos de Git, abre otra terminal o para antes la app.

Los huecos `___` son código que falta. Borra el hueco y escribe lo que pide el comentario que tiene encima. Cuando el hueco va dentro de las comillas de un texto, las comillas se quedan y solo cambia lo de dentro; ahí `___` es texto y la app arranca igual sin rellenarlo.

## Repaso: dónde lo dejamos

Un repaso corto con la versión terminada, aunque acabaras la sesión 1. Arranca `exercises/paso_3.py` y abre el desplegable «Tu verdad»: son los cuatro recuentos de la sesión 1. En la última tabla están los activos y las bajas del plan básico. Divide las bajas entre el total, activos más bajas: ese porcentaje es tu referencia para toda la sesión. Apúntalo en `mis_notas.md`.

Arranca `exercises/paso_6.py` y pregunta «¿Cuál es la tasa de churn del plan básico?». Si explica un procedimiento en vez de dar un número, pide «Dame solo el porcentaje, sin explicar el procedimiento». Compara con tu referencia. Abre «Lo que enviamos» y lee el `content` del `system`: cinco filas de un solo socio. El modelo no tiene la tabla; tiene ese texto, y el número que escribe sale del mismo sitio que las palabras de alrededor.

Si quieres, `paso_7.py` con las distribuciones: sigue sin poder cruzar plan y estado. Lo que está escrito lo lee; lo que hay que contar no lo cuenta. La sesión 1 terminó con una pregunta: ¿y si en vez de la respuesta le pedimos el código? Empieza ahí.

## Paso 8: pide el código, no la respuesta

**Qué haces.** Un hueco: la primera línea del `system_prompt`, dentro de las comillas. Esa variable se llamaba `context` en la sesión 1; es la misma entrada `system` de `messages`. Antes de rellenarlo, haz el experimento de la cabecera con la misma pregunta tres veces, «¿Cuántos registros tiene el dataset?»:

1. Con el hueco tal cual, `___` como primera línea.
2. Con «Responde con texto, en una frase, sin escribir código.» en el hueco.
3. Con la instrucción que pide el comentario.

Apunta qué devuelve cada vez. Si las tres devuelven código, no has hecho nada mal: sigue leyendo. Después haz las tres preguntas de la cabecera.

**Qué hay detrás.** El modelo no lee una línea: lee el prompt entero, y las reglas de abajo ya hablan de código. Por eso el experimento no tiene un interruptor mágico en la primera línea. Cuando dos partes del prompt se contradicen, gana la que más pesa en el conjunto, y no siempre la que tú creías; apunta cuál ganó en tu caso. La instrucción explícita y las reglas juntas son la versión que funciona de forma fiable. El prompt es una unidad: cámbialo pensando en el conjunto.

Abre «Lo que enviamos»: el `content` del `system` ya no lleva filas de la tabla. Solo los nombres de las columnas, cuántas filas hay y las reglas. Abre «Lo que recibimos»: el código está dentro de `content`, entre ` ```python ` y ` ``` `; esos tres acentos graves se llaman backticks y son la marca de Markdown para un bloque de código. Es texto. El modelo no ha ejecutado nada, y tu app tampoco. Compara los `prompt_tokens` con los del paso 6.

**Simulación 5: `explicaciones/codigo.html`, con la casilla «Con los valores de las columnas» desmarcada.** Estaciones 1 a 3: el mismo JSON que acabas de abrir, el `content` con el código dentro como texto, y la receta que lo extrae. Son capturas reales de la pregunta del churn; la página no está conectada a tu app.

**Puerta.** Las tres preguntas de la cabecera respondidas con un bloque de código, y sabes señalar en «Lo que recibimos» dónde está.

**Antes de seguir.** Pregunta «¿Cuál es la tasa de churn del plan básico?» y lee el código con calma. ¿Con qué valor filtra la columna `plan`? Apúntalo tal cual.

## Paso 9: ejecuta el código

**Qué haces.** Dos huecos: extraer el código de la respuesta y ejecutarlo. Los dos están escritos en el comentario de encima. Luego «¿Cuántos registros tiene el dataset de socios?» y después la pregunta de la tasa de churn del básico.

Antes de rellenar nada, arranca y pregunta: el error que ves es Python diciendo que `___` no es un nombre que conozca. Es el mismo tipo de error que verías si escribieras mal una variable.

**Qué hay detrás.** `re.search` con esa receta busca lo que hay entre ` ```python ` y ` ``` ` y lo devuelve como texto. `exec` ejecuta ese texto como si estuviera escrito en tu archivo, dentro de un diccionario que hace de mesa de trabajo: le ponemos encima `df_members`, `df_context` y `pd`, el código deja ahí `resultado`, y la app lo lee. El número ahora lo calcula pandas sobre las 16.334 filas. El modelo nunca las ha visto: solo escribió la receta.

Vas a leer código pandas que no has escrito, con `groupby`, `lambda` o `shape`. No hace falta entenderlo entero: busca el nombre de la columna y el valor con el que filtra.

Y la receta puede estar mal. Con la pregunta del churn del básico, mira el valor con el que filtra `plan` y el resultado. Si filtró por «básico», no hay ninguna fila que cumpla y el resultado es `nan` (not a number: pandas no puede promediar cero filas), cero, `None`, o un error de división por cero en rojo. En ningún caso tu referencia. En la tabla el plan se llama `basic`. El modelo conoce los nombres de las columnas, que van en el prompt; los valores, no. Adivina, y en castellano adivina «básico».

**El reto de verdad.** Pega en el `system_prompt` las tres líneas de valores que da la cabecera, sin el `#`, dentro de las comillas triples, debajo de la línea `Columnas: {list(df_members.columns)}`. Guarda, repite la pregunta y compara con tu referencia. Abre «Lo que enviamos» y localiza los valores dentro del `content`: eso es lo único que ha cambiado.

**Simulación 5, estación 4.** La mesa de trabajo a cámara lenta: con la casilla desmarcada, `'básico'` no encuentra ninguna fila y sale `nan`; márcala y verás `'basic'`, las filas que filtra y el número que tú ya tienes.

**Puerta.** La tasa de churn del básico coincide con tu referencia del repaso, y sabes decir qué líneas del prompt lo han arreglado.

**Si has terminado antes.** Pregunta «¿Cuántos socios se dieron de baja en 2024?» dos o tres veces y lee el código cada vez. Fíjate en cómo filtra el año en la columna `month`, que es texto con la forma `AAAA-MM`, y en si cuenta filas o socios distintos con `member_id`. ¿Da lo mismo cada vez?

## Paso 10: cuando el código falla, y cuando no falla pero debería

**Qué haces.** Tres huecos: el desplegable que enseña el código, el `st.error` y el desplegable con los detalles. Este archivo vuelve al prompt del paso 8, sin los valores de las columnas: si preguntas por el churn del básico, comprueba si usa el valor real `basic` o necesita la aclaración. Después dos preguntas: «Dibuja un gráfico de barras del churn por centro» y «¿Cuál es la satisfacción media de los socios?».

**Qué hay detrás.** `try` intenta ejecutar; si algo revienta, `except` recoge el error en `e` y la app sigue viva. La petición del gráfico puede fallar, devolver una tabla o producir código válido. Anota lo que ocurrió. Para comprobar el manejo de errores aunque acierte, añade temporalmente dentro del `try`, antes de `exec`, `raise ValueError("Prueba controlada del error")`. Comprueba el mensaje y los detalles; retira esa línea después.

La segunda pregunta es la importante. No hay ninguna columna de satisfacción, así que no se puede responder. Mira lo que hace el modelo: escribe código que calcula algo con las columnas que sí existen, o deja `resultado = None` y la app pinta `None` debajo de «Resultado». Si devuelve un número, ese número es aritmética real sobre filas reales, y responde a una pregunta que nadie puede responder con estos datos. No hay error, no salta `except`, y sin el desplegable no lo sabrías nunca. Por eso el código generado se enseña siempre: es la única forma de saber qué se ha calculado.

**Puerta.** Un error en rojo con su desplegable de detalles, y la pregunta de la satisfacción con el código abierto y tu veredicto escrito en `mis_notas.md`: ¿qué ha calculado en realidad?

**Si has terminado antes.** El reto D de la cabecera: `exec` ejecuta en tu ordenador lo que el modelo escriba. Léelo, no lo ejecutes.

## Paso 11 (opcional): que corrija sus propios errores

**Qué haces.** Sin huecos. Lee el bucle. Pregunta «Dibuja un gráfico de barras del churn por centro» y mira los mensajes azules. Abre «Lo que enviamos en el último intento».

**Qué hay detrás.** El reintento son dos líneas: añadir a `messages` el código que falló como `assistant` y el error como `user`, y volver a llamar. El modelo no recuerda el primer intento; recibe la conversación entera porque la construimos nosotros en esa lista, y por eso cada petición pesa más que la anterior. Con el gráfico suele acertar al segundo intento: quita el dibujo y devuelve los recuentos. Prueba «Usa la columna nps de df_members para calcular el NPS medio por centro»: el error se corrige, pero la respuesta no puede existir; fíjate en cómo se rinde. Si el código deja `resultado = None`, la app lo cuenta como «sin resultado» y no vuelve a intentarlo: mira el pie, que dice cuántas peticiones hubo y cuánto pesó la última. Hay errores que ningún reintento arregla porque el problema está en la pregunta, no en el código.

**Simulación 5, estación 5.** El caso del gráfico paso a paso: el código del primer intento, el error, la lista `messages` creciendo de dos a cuatro entradas y los tokens de cada intento.

**Puerta.** Explica qué recibió cada petición que realmente ocurrió. Si hubo corrección, localiza el código fallido y el error en la petición siguiente. Si acertó a la primera o reconoció que faltaban datos, explica por qué no hubo reintento. Para observar el mecanismo sin depender de un fallo del modelo, recorre el ejemplo registrado de la simulación.

## Vía avanzada

Esto es opcional y va aparte del resto: no hace falta para el cierre ni para la sesión 3, y puedes coger solo un trozo. Los cuatro pasos de hoy llevan al final de su cabecera un bloque «Vía avanzada», y los cuatro cuentan lo mismo: el prompt se construye desde los datos y el resultado se comprueba. En el paso 8 mides lo que pesa el prompt y si el código se repite con `temperature=0`. En el paso 9 dejas de escribir a mano los valores de las columnas y los sacas del DataFrame. En el paso 10 miras el código antes del `exec` y te niegas a ejecutar lo que traiga `import` u `open(`, y en el paso 11 compruebas que el resultado es posible antes de darlo por bueno: si una tasa se sale de su rango, eso es un error más y se lo devuelves al modelo.

**Puerta.** Uno de los cuatro funcionando, y apuntado en `mis_notas.md` qué preguntas dejó de responder bien tu cambio. Todo filtro tiene ese coste; lo que no vale es no saber cuál es.

El ejercicio extra es [`exercises/bonus_evaluacion.py`](exercises/bonus_evaluacion.py). Lanza de una vez las doce preguntas de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md) contra el prompt del paso 10, esta vez con los valores de las columnas dentro, y de cada una te enseña el código generado, el resultado, el error si lo hubo, los tokens y los segundos. La nota la pones tú, pregunta a pregunta: correcta, parcial, inventada o no puede. Tiene tres huecos y no mide nada hasta que los rellenes; el archivo abre igual, los huecos solo revientan cuando pulsas el botón. Con la primera nota apuntada, cambia el prompt (las reglas de negocio de [ENUNCIADO.md](ENUNCIADO.md), un ejemplo resuelto, `temperature=0`), vuelve a lanzarlo y compara. En `mis_notas.md`: las dos notas, qué cambiaste entre una y otra, y qué has decidido que es una respuesta «correcta» a la pregunta doce.

**Puerta.** Las doce puntuadas dos veces, con dos prompts distintos, y las dos notas escritas.

## Cierre: lo que has visto

**Simulación 5, estación 6.** Quién hace qué, y la pregunta de la satisfacción con su código al lado. Mírala antes de responder a lo de abajo.

Responde por escrito, en `mis_notas.md`, con tus palabras:

- Entre el paso 6 y el paso 9, ¿qué ha cambiado en el JSON que enviamos y qué no?
- ¿De dónde sale ahora el número de la tasa de churn? ¿Qué papel tiene el modelo y cuál tiene pandas?
- ¿Por qué falló «básico» y qué lo arregló? ¿Qué te dice eso sobre lo que el modelo sabe de tus datos?
- En el paso 10, la pregunta de la satisfacción no dio error. ¿Por qué es más peligroso que un error?
- Tras un reintento del paso 11, ¿qué hay en `messages` y por qué el modelo «recuerda»?

Guarda tu trabajo. Para antes la app con `Ctrl+C` o usa otra terminal del proyecto:

```text
git add exercises
git add mis_notas.md
git commit -m "Completo la sesión 2"
git status
```

Con el paso 10 o el 11 abierto, prueba tres o cuatro de las doce preguntas de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md) y apunta cuáles responde bien, cuáles mal y cuáles no puede. En la sesión 3 el chat tendrá memoria: la lista `messages` que hoy has construido a mano con el error es la misma que guardará la conversación.
