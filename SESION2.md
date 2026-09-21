# Sesión 2: que el modelo escriba el código y que Python calcule

Esta guía acompaña los ejercicios `exercises/paso_8.py` a `paso_11.py`. Puedes seguirla en clase o por tu cuenta. Los pasos 0 a 7 están en esta rama en su versión terminada: son la sesión 1 resuelta, para repasar y para comparar con la tuya. Cada ejercicio lleva sus instrucciones en la cabecera del archivo; aquí está el hilo de la sesión, lo que debes ver antes de pasar al siguiente paso y las explicaciones que no caben en un comentario. No contiene las soluciones.

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

Si `status` lista archivos modificados, guárdalos primero en tu rama de la sesión 1. Git no cambia de rama si hay cambios sin guardar en archivos que la otra rama trae distintos, y hoy los trae todos:

```text
git add exercises
git commit -m "Mi sesión 1"
```

Si además tienes `mis_notas.md`, añádelo antes del commit con `git add mis_notas.md`. Si un `add` falla porque el archivo no existe, no se ha guardado nada: repítelo sin ese archivo. Ahora descarga la rama de la clase y crea la tuya:

```text
git fetch origin
git switch -c alumno/sesion-2 origin/clase/sesion-2
git branch --show-current
```

Si Git dice que `alumno/sesion-2` ya existe, es que ya la creaste: `git switch alumno/sesion-2`. Estos comandos funcionan desde cualquier rama, también desde `main` si empiezas hoy; si `git status` muestra cambios ahí, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservarlos.

Mira la carpeta `exercises/`: hay doce archivos. Abre `paso_5.py`: el hueco de `client` está relleno y los desplegables están pegados al final. Es la versión terminada, no la tuya. La tuya sigue en la otra rama. Compárala con el último archivo que tocaste, cambiando `paso_6` por el que sea:

```text
git diff alumno/sesion-1 -- exercises/paso_6.py
```

Las líneas con `-` son de tu versión y las de `+`, de la terminada. Verás al menos la línea del título, que ahora dice «(resuelto)». Si ocupa una pantalla con `(END)`, pulsa `q`.

Tus notas se quedaron en `alumno/sesion-1` con el resto de tu trabajo. Tráelas a esta rama:

```text
git restore --source=alumno/sesion-1 -- mis_notas.md
git add mis_notas.md
git commit -m "Traigo mis notas"
```

`restore --source` copia un archivo tal como está en otra rama, sin tocar nada más. Si Git dice que no encuentra el archivo en esa rama pero lo ves en la carpeta, es que nunca hiciste commit de él y ha viajado contigo: no hace falta traerlo. Si nunca creaste `mis_notas.md`, créalo ahora en la raíz del proyecto: hoy también hay cosas que apuntar.

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

**Qué haces.** Un hueco: la primera línea del `system_prompt`, dentro de las comillas. Antes de rellenarlo, haz el experimento de la cabecera con la misma pregunta tres veces, «¿Cuántos registros tiene el dataset?»:

1. Con el hueco tal cual, `___` como primera línea.
2. Con «Responde con texto, en una frase, sin escribir código.» en el hueco.
3. Con la instrucción que pide el comentario.

Apunta qué devuelve cada vez. Después haz las tres preguntas de la cabecera.

**Qué hay detrás.** El modelo no lee una línea: lee el prompt entero, y las reglas de abajo ya hablan de código. Por eso el experimento no tiene un interruptor mágico en la primera línea. Cuando dos partes del prompt se contradicen, gana la que más pesa en el conjunto, y no siempre la que tú creías; apunta cuál ganó en tu caso. La instrucción explícita y las reglas juntas son la versión que funciona de forma fiable. El prompt es una unidad: cámbialo pensando en el conjunto.

Abre «Lo que enviamos»: el `content` del `system` ya no lleva filas de la tabla. Solo los nombres de las columnas, cuántas filas hay y las reglas. Abre «Lo que recibimos»: el código está dentro de `content`, entre ` ```python ` y ` ``` `; esos tres acentos graves se llaman backticks y son la marca de Markdown para un bloque de código. Es texto. El modelo no ha ejecutado nada, y tu app tampoco. Compara los `prompt_tokens` con los del paso 6.

**Puerta.** Las tres preguntas de la cabecera respondidas con un bloque de código, y sabes señalar en «Lo que recibimos» dónde está.

**Antes de seguir.** Pregunta «¿Cuál es la tasa de churn del plan básico?» y lee el código con calma. ¿Con qué valor filtra la columna `plan`? Apúntalo tal cual.

## Paso 9: ejecuta el código

**Qué haces.** Dos huecos: extraer el código de la respuesta y ejecutarlo. Los dos están escritos en el comentario de encima. Luego «¿Cuántos registros tiene el dataset de socios?» y después la pregunta de la tasa de churn del básico.

Antes de rellenar nada, arranca y pregunta: el error que ves es Python diciendo que `___` no es un nombre que conozca. Es el mismo tipo de error que verías si escribieras mal una variable.

**Qué hay detrás.** `re.search` con esa receta busca lo que hay entre ` ```python ` y ` ``` ` y lo devuelve como texto. `exec` ejecuta ese texto como si estuviera escrito en tu archivo, dentro de un diccionario que hace de mesa de trabajo: le ponemos encima `df_members`, `df_context` y `pd`, el código deja ahí `resultado`, y la app lo lee. El número ahora lo calcula pandas sobre las 16.334 filas. El modelo nunca las ha visto: solo escribió la receta.

Y la receta puede estar mal. Con la pregunta del churn del básico, mira el valor con el que filtra `plan` y el resultado. Si filtró por «básico», no hay ninguna fila que cumpla y el resultado es `nan` (not a number: pandas no puede promediar cero filas), cero, o un error de división por cero en rojo. En ningún caso tu referencia. En la tabla el plan se llama `basic`. El modelo conoce los nombres de las columnas, que van en el prompt; los valores, no. Adivina, y en castellano adivina «básico».

**El reto de verdad.** Pega en el `system_prompt` las tres líneas de valores que da la cabecera, sin el `#`, dentro de las comillas triples, debajo de la línea `Columnas: {list(df_members.columns)}`. Guarda, repite la pregunta y compara con tu referencia. Abre «Lo que enviamos» y localiza los valores dentro del `content`: eso es lo único que ha cambiado.

**Puerta.** La tasa de churn del básico coincide con tu referencia del repaso, y sabes decir qué líneas del prompt lo han arreglado.

**Si has terminado antes.** Pregunta «¿Cuántos socios se dieron de baja en 2024?» dos o tres veces y lee el código cada vez. Fíjate en cómo filtra el año en la columna `month`, que es texto con la forma `AAAA-MM`, y en si cuenta filas o socios distintos con `member_id`. ¿Da lo mismo cada vez?

## Paso 10: cuando el código falla, y cuando no falla pero debería

**Qué haces.** Tres huecos: el desplegable que enseña el código, el `st.error` y el desplegable con los detalles. Después dos preguntas: «Dibuja un gráfico de barras del churn por centro» y «¿Cuál es la satisfacción media de los socios?».

**Qué hay detrás.** `try` intenta ejecutar; si algo revienta, `except` recoge el error en `e` y la app sigue viva. Con el gráfico verás un error de verdad: el código suele intentar importar una librería de dibujo que no está instalada, y sin `try` la app se caería.

La segunda pregunta es la importante. No hay ninguna columna de satisfacción, así que no se puede responder. Mira lo que hace el modelo: escribe código que calcula algo con las columnas que sí existen, o deja `resultado = None` y la app no pinta nada debajo de «Resultado». Si devuelve un número, ese número es aritmética real sobre filas reales, y responde a una pregunta que nadie puede responder con estos datos. No hay error, no salta `except`, y sin el desplegable no lo sabrías nunca. Por eso el código generado se enseña siempre: es la única forma de saber qué se ha calculado.

**Puerta.** Un error en rojo con su desplegable de detalles, y la pregunta de la satisfacción con el código abierto y tu veredicto escrito en `mis_notas.md`: ¿qué ha calculado en realidad?

**Si has terminado antes.** El reto D de la cabecera: `exec` ejecuta en tu ordenador lo que el modelo escriba. Léelo, no lo ejecutes.

## Paso 11 (opcional): que corrija sus propios errores

**Qué haces.** Sin huecos. Lee el bucle. Pregunta «Dibuja un gráfico de barras del churn por centro» y mira los mensajes azules. Abre «Lo que enviamos en el último intento».

**Qué hay detrás.** El reintento son dos líneas: añadir a `messages` el código que falló como `assistant` y el error como `user`, y volver a llamar. El modelo no recuerda el primer intento; recibe la conversación entera porque la construimos nosotros en esa lista, y por eso cada petición pesa más que la anterior. Con el gráfico suele acertar al segundo intento: quita el dibujo y devuelve los recuentos. Prueba «Usa la columna nps de df_members para calcular el NPS medio por centro»: el error se corrige, pero la respuesta no puede existir; fíjate en cómo se rinde. Si el código deja `resultado = None`, la app lo cuenta como «sin resultado» y no vuelve a intentarlo: mira el pie con el número de peticiones. Hay errores que ningún reintento arregla porque el problema está en la pregunta, no en el código.

**Puerta.** Una pregunta resuelta al segundo intento, y en el desplegable una lista `messages` con cuatro entradas.

## Cierre: lo que has visto

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
