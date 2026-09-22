# Sesión 3: que el chat recuerde y que alguien explique el número

Esta guía acompaña los ejercicios `exercises/paso_12.py` a `paso_15.py`. Puedes seguirla en clase o por tu cuenta. Los pasos 0 a 11 están en esta rama en su versión terminada: son las sesiones 1 y 2 resueltas, para repasar y para comparar con las tuyas. Cada ejercicio lleva sus instrucciones en la cabecera del archivo; aquí está el hilo de la sesión, lo que debes ver antes de pasar al siguiente paso y las explicaciones que no caben en un comentario. No contiene las soluciones. Las páginas de `explicaciones/` son simulaciones que se abren con doble clic y no tocan tu app; hoy hay una nueva, `memoria.html`, y la guía indica cuándo abrirla.

## Qué vas a construir

El chat de la sesión 2, con tres cambios. Recuerda la conversación. Después de calcular, hace una segunda petición para que el modelo explique el número. Y el prompt lleva ejemplos resueltos. Por el camino verás que la pantalla puede recordar sin que el modelo recuerde nada, que la memoria es lo que tú metes en `messages` y que se paga en tokens a cada pregunta, que la explicación es texto escrito por el modelo sobre un número que no ha calculado, y que los ejemplos cambian qué se calcula más que si se calcula bien.

Necesitas la instalación de [SETUP.md](SETUP.md) y el archivo `.env` con la clave del curso, la misma de todo el taller. La clave se comparte en el chat del curso; si no la tienes, pídela ahí. La cabecera de `exercises/paso_5.py` explica cómo crear el archivo.

## Preparar tu rama

En la sesión 2 creaste `alumno/sesion-2` y trabajaste en ella. Hoy se publica `clase/sesion-3`, con los pasos 0 a 11 terminados y los 12 a 15 nuevos. Vas a crear `alumno/sesion-3` a partir de ella. Tu trabajo de la sesión 2 se queda en `alumno/sesion-2`, intacto.

Abre el proyecto en VS Code y **Terminal > New Terminal**. Si hay una app de Streamlit corriendo en otra terminal, párala con `Ctrl+C`. Mira dónde estás y qué tienes pendiente:

```text
git branch --show-current
git status
```

Si `status` lista archivos modificados o sin seguimiento, guárdalos primero en tu rama de la sesión 2. Git no cambia de rama si hay cambios sin guardar en archivos que la otra rama trae distintos, y hoy trae distintos casi todos. Si no tienes `mis_notas.md`, la segunda línea da un error y no pasa nada: el commit guarda lo demás.

```text
git add exercises
git add mis_notas.md
git commit -m "Mi sesión 2"
git status
```

`status` debe terminar en `nothing to commit, working tree clean`. Si no, mira qué archivo queda, añádelo con `git add` y su nombre, y repite el `git commit`: un archivo añadido sin commit viaja contigo a la rama nueva y acaba en otro commit. Git sugiere `git push` después de cada commit; no hace falta, tu trabajo se queda en tu ordenador. Ahora descarga la rama de la clase y crea la tuya:

```text
git fetch origin
git switch -c alumno/sesion-3 origin/clase/sesion-3
git branch --show-current
```

Si Git dice que `alumno/sesion-3` ya existe, es que ya la creaste: `git switch alumno/sesion-3`. Estos comandos funcionan desde cualquier rama: desde `alumno/sesion-1` si no hiciste la sesión 2, y desde `main` si empiezas hoy. Si `git status` muestra cambios en esa rama, guárdalos igual con un commit antes de cambiar, o mira [ACTUALIZAR.md](ACTUALIZAR.md).

Mira la carpeta `exercises/`: hay diecisiete archivos, los dieciséis pasos y el ejercicio extra. Abre `paso_9.py` y busca el `system_prompt`: los valores de las columnas ya están pegados debajo de `Columnas:`. Es la versión terminada, no la tuya. La tuya sigue en la otra rama. Compárala con el último archivo que tocaste, cambiando `paso_10` por el que sea:

```text
git diff alumno/sesion-2 -- exercises/paso_10.py
```

Las líneas con `-` son de tu versión y las de `+`, de la terminada. Verás al menos la línea del título, que ahora dice «(resuelto)». Si ocupa una pantalla con `(END)`, pulsa `q`. Si vienes de `alumno/sesion-1`, pon ese nombre en lugar de `alumno/sesion-2`, aquí y en el bloque siguiente.

Tus notas se quedaron en `alumno/sesion-2` con el resto de tu trabajo, y `mis_notas.md` ya no está en la carpeta. Compruébalo antes de seguir: si lo ves en la carpeta, sáltate este bloque, porque `restore` lo sustituiría por la versión de la otra rama, o lo borraría si allí no existe. Si no está, tráelo:

```text
git restore --source=alumno/sesion-2 -- mis_notas.md
git add mis_notas.md
git commit -m "Traigo mis notas"
```

`restore --source` copia un archivo tal como está en otra rama, sin tocar nada más. Si Git dice que no encuentra el archivo en esa rama, es que nunca lo guardaste con un commit. Si nunca creaste `mis_notas.md`, créalo ahora en la raíz del proyecto: hoy también hay cosas que apuntar.

## Cómo se trabaja cada paso

Igual que en las sesiones anteriores. Abres el archivo del paso en VS Code y lees la cabecera. Arrancas la app desde la terminal del proyecto con el comando de tu sistema, cambiando el nombre del archivo:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_12.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_12.py
```

Corriges o completas, guardas con `Ctrl+S` o `Cmd+S` y miras el navegador; si aparece **Rerun**, púlsalo. Cada paso tiene una **puerta**: lo que debes ver en pantalla para darlo por terminado. Para el siguiente paso, `Ctrl+C` en la terminal de la app y el comando con el archivo nuevo. Para los comandos de Git, abre otra terminal o para antes la app.

Los huecos `___` son código que falta. Borra el hueco y escribe lo que pide el comentario que tiene encima. Cuando el hueco va dentro de las comillas de un texto, las comillas se quedan y solo cambia lo de dentro; ahí `___` es texto y la app arranca igual sin rellenarlo.

Los pasos de hoy tienen un interruptor **Mostrar código** arriba a la derecha. Actívalo al empezar cada paso: sin él no ves qué ha calculado el modelo, y en la sesión 2 viste por qué eso importa.

## Repaso: dónde lo dejamos

Un repaso corto con la versión terminada, aunque acabaras la sesión 2. Arranca `exercises/paso_11.py` y pregunta «Dibuja un gráfico de barras del churn por centro». Lo normal es que el primer intento falle y veas un mensaje azul. Abre «Lo que enviamos en el último intento»: la lista `messages` tiene cuatro entradas, el `system`, tu pregunta, el código que falló como `assistant` y el error como `user`. Si esta vez acertó a la primera, verás dos; pregúntalo otra vez. Mira también el resultado: que el segundo intento no dé error no quiere decir que el número esté bien.

Esa lista es la idea de hoy. El modelo no recordó su primer intento: recibió la conversación entera porque tu app la escribió en `messages`. Hoy harás lo mismo con las preguntas del usuario.

## Paso 12: que el chat recuerde

**Qué haces.** Tres huecos: crear la lista del historial en `st.session_state`, guardar ahí cada pregunta y guardar cada respuesta. Antes de rellenar nada, arranca la app: el error rojo sale al abrirla, sin preguntar nada, porque el primer hueco está en una línea que Python lee nada más empezar. Rellena los tres y haz el diálogo de la cabecera, las tres preguntas en orden. Antes de enviar la segunda, «¿Cuál es el que tiene más socios?», apunta qué esperas que responda, y hazlo antes de seguir leyendo: el párrafo siguiente cuenta lo que suele pasar.

**Qué hay detrás.** Cada vez que escribes, Streamlit ejecuta el archivo entero desde la primera línea; lo viste en la sesión 1. `prompt`, `messages` o `resultado` nacen y mueren en cada ejecución. `st.session_state` es lo único que sobrevive, y el bucle `for msg in st.session_state.messages` vuelve a pintar la conversación en cada vuelta. Lo que se guarda es texto: por eso, a la pregunta siguiente, una tabla vuelve a aparecer como texto en el historial.

Ahora abre «Lo que enviamos en la última petición», debajo de la respuesta. Dos entradas: el `system` y tu última pregunta. La pantalla recuerda; el modelo, no. Recibió «¿Cuál es el que tiene más socios?» sin nada más. Mira el código de la segunda y de la tercera. Lo normal es que al menos una responda con un centro o con un motivo de baja: el modelo nunca vio la palabra «planes». Si las dos hablan de planes, ha acertado adivinando, y la petición lo demuestra.

**El reto de verdad.** Dentro del código, debajo de `messages = [...]`, hay un bloque «El reto de verdad» con tres líneas comentadas. Quita el `# ` del principio de las tres, sin tocar los espacios de delante, y guarda. Rehacen `messages` con todo el historial: es el mismo bucle que pinta la conversación en pantalla, puesto dentro de la petición. Recarga la página del navegador (F5 en Windows, `Cmd+R` en macOS) para empezar con la conversación vacía y repite las tres preguntas. Abre el desplegable en cada una: dos entradas, cuatro, seis. Mira el pie: los tokens de prompt suben a cada pregunta, porque cada petición lleva todas las anteriores. Suben poco, unos veinte por turno, porque el historial guarda el resultado como texto y no el código; con respuestas largas subirían mucho más. Si Python dice `IndentationError` en una línea que no has tocado, revisa las tres que has activado: deben quedar alineadas con `messages = [` de encima.

**Simulación 6: `explicaciones/memoria.html`.** Estaciones 1 a 3: la pantalla frente a la petición, lo que sobrevive a cada ejecución, y `messages` creciendo con la conversación. Son capturas reales del mismo diálogo; la página no está conectada a tu app.

**Puerta.** Con el reto de verdad hecho, la tercera pregunta responde sobre planes, y su desplegable muestra seis entradas en `messages`.

**Antes de seguir.** Mira el código de «¿Cuál es el que tiene más socios?». ¿Cuenta filas o socios distintos? No es lo mismo: la tabla tiene una fila por socio y por mes, 16.334 filas de 940 socios, y la columna `member_id` identifica a cada socio. Pregunta «¿Qué plan tiene más socios distintos, contando member_id?» y compara las dos respuestas. Apunta cuál responde a lo que tú querías saber.

## Paso 13: una segunda petición que explica el número

**Qué haces.** Dos huecos, los dos en la segunda pasada: el texto que le pedimos al modelo y la llamada que lo envía. El primero es largo. Sustituye `___` por el texto del comentario de encima, desde `f"""` hasta las tres comillas del final, quitando el `#` de cada línea. Las líneas de dentro pueden quedar pegadas al margen: dentro de las comillas triples la sangría no rompe nada. La `f` de delante sí importa: es la que mete tu pregunta y el resultado en el texto. Sin ella, el modelo recibe `{resultado}` tal cual, sin ningún error, y escribe una explicación de un número que no ha visto. Si lo ves en el desplegable de la pasada 2, ya sabes qué falta. Antes de rellenar, arranca y pregunta: la pasada 1 funciona y verás su desplegable; el error rojo llega después, en el primer hueco. Rellena los dos y pregunta «¿Cuál es la tasa de churn del plan básico?».

**Qué hay detrás.** Son dos peticiones y cada una tiene su desplegable. La primera es la de la sesión 2: código, `exec`, un número de pandas. Fíjate en que ese número ya no aparece suelto en la pantalla. Abre «Lo que enviamos: pasada 2, la explicación» y lo encontrarás dentro del `system`, como texto, al lado de tu pregunta. El modelo no lo ha calculado: lo lee y escribe alrededor. Compara los tokens de las dos pasadas en los pies: la segunda pesa mucho menos, porque no lleva las columnas ni las reglas.

La explicación suena a informe, y el número de dentro es real. El resto de la frase sale del mismo sitio que las respuestas de la sesión 1: el modelo escribe lo probable. Si añade una cifra que no está en el resultado, esa cifra no la ha calculado nadie. Haz el reto A de la cabecera con las tres preguntas y busca cada número de la explicación dentro del `system` de la pasada 2. Los que no estén ahí no salen de tus datos. Y que un número esté no basta: mira si la frase le da el sentido que tiene. Una diferencia de puntos contada como porcentaje, una media de bajas llamada tasa o una correlación leída al revés usan números del resultado y dicen algo falso.

Con una tabla larga, como en el reto B, abre el desplegable de la pasada 2 y mira el final del resultado dentro del `system`: pandas recorta las tablas largas al convertirlas en texto y deja `...` y una línea como `[108 rows x 3 columns]`. El modelo solo ve las filas que caben, y explica la tabla entera.

**Simulación 6, estaciones 4 y 5.** Las dos pasadas con el número viajando como texto, y varias explicaciones reales con sus números marcados: los que están en el resultado y los que no.

**Puerta.** La explicación de la tasa de churn del básico en pantalla, y en `mis_notas.md`, para una de las preguntas del reto A, qué números de la explicación están en el resultado y cuáles no.

## Paso 14: ejemplos en el prompt

**Qué haces.** Dos huecos, los dos dentro de comillas: `EXAMPLES` y `RULES`. Como son texto, la app arranca sin rellenarlos, y eso te da el antes. Con **Mostrar código** activado, pregunta «¿Las bajas del plan básico aumentaron cuando el competidor bajó precios?» y apunta qué compara el código (¿cuenta bajas o calcula tasas? ¿qué ha decidido que significa «cuando el competidor bajó precios»?) y los tokens del pie. Hazla dos veces: el modelo puede decidir cada vez una cosa distinta, y llegar a respuestas opuestas. Después copia en los huecos los ejemplos y las reglas de las PISTAS, sin el `#` del principio de cada línea, guarda y repite la pregunta. Ojo al comparar: sin rellenar, este prompt lleva menos reglas que el del paso 13, porque la del `merge` y la de la tasa de churn pasan a `RULES`.

**Qué hay detrás.** Los ejemplos son texto dentro del `system`: ábrelo en «Lo que enviamos» y los verás. El modelo no los ejecuta; los imita. Por eso cambian la forma del código que escribe, y viajan en cada petición: mira cuánto ha subido el pie.

En el código de esta pregunta verás dos cosas nuevas. `merge` une las dos tablas por la columna `month`: a cada fila de un socio le pega el precio del competidor de ese mes. `.diff()` resta a cada fila la anterior: con meses ordenados, dice cuánto cambió algo de un mes al siguiente, y `< 0` se queda con los meses en que bajó.

Después prueba las preguntas 7 a 12 de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md), con y sin los ejemplos. Quizá ninguna daba error antes. Lo que cambia es qué se calcula: una pregunta que antes devolvía un sí o un no puede devolver dos márgenes, y el lifetime value puede pasar de sumar lo pagado a sumar el margen. Ninguna de las dos versiones es un error de Python. Decidir cuál es la buena es trabajo tuyo, no del modelo.

La pregunta 12 merece el reto C: «¿Debería FitLife bajar el precio del plan básico?». Abre el código y busca de dónde sale la recomendación. Si sale de un umbral, ¿quién ha elegido ese umbral?

**Simulación 6, estación 6.** El mismo prompt con y sin ejemplos, y dos preguntas reales cuyo código cambia de definición.

**Puerta.** La pregunta del competidor antes y después de los ejemplos, con lo que compara el código en cada caso apuntado en `mis_notas.md`, y una de las preguntas 7 a 12 cuyo código haya cambiado.

## Paso 15 (opcional): el analista completo

**Qué haces.** Sin huecos. Es todo junto: el prompt con ejemplos, los reintentos, la explicación y el historial en pantalla. Como en los pasos 13 y 14, cada petición lleva solo la última pregunta. Si quieres la conversación entera, son las tres líneas del reto de verdad del paso 12, debajo de `messages = [...]`, cambiando `st.session_state.messages` por `st.session_state.messages_v3`, que es como se llama aquí el historial. Haz las doce preguntas de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md) y ponle a cada una una nota: correcta, parcial, inventada o no puede. Después, las preguntas de la misión de la cabecera.

**Qué hay detrás.** Lee la función `interpret_result()` antes de preguntar. Su prompt le cuenta al modelo los precios de los tres planes y que el competidor cobra 19 €. Por eso las explicaciones citan cifras que no salen del resultado: salen de ese texto, que escribió una persona. Es contexto útil, y también es texto que el modelo repite sin comprobar.

La de bajar el básico de 29 € a 24 € es la más útil de leer despacio. Abre el código: ¿multiplica por los socios de hoy, los activos del último mes, o por todas las filas de los tres años? La explicación repetirá la cifra que le des con toda seguridad, sea cual sea. Ninguna segunda pasada arregla un cálculo que responde a otra pregunta.

El reto A cambia el modelo. `gpt-4.1-nano` funciona con la clave del curso; `gpt-4.1` no, y el error 403 que verás lo dice: el proyecto no tiene acceso a ese modelo.

**Puerta.** Las doce preguntas con su nota en `mis_notas.md`, y tu respuesta a la doce escrita por ti: qué números usarías y qué decidirías.

## Vía avanzada

Esto es opcional y va aparte del resto: no hace falta para el cierre, y puedes coger solo un trozo. Los cuatro pasos de hoy llevan al final de su cabecera un bloque «Vía avanzada», y los cuatro cuentan lo mismo: lo que envías lo decides tú, y lo que vuelve se comprueba. En el paso 12 mides cuánto crece la petición con la conversación y la recortas a las últimas entradas. En el paso 13 comparas los números de la explicación con los del resultado antes de enseñarla. En el paso 14 mides los ejemplos con `exercises/bonus_evaluacion.py`, ya resuelto, en vez de mirarlos pregunta a pregunta. En el paso 15 guardas cada respuesta en un archivo para poder releerlas y defenderlas.

**Puerta.** Uno de los cuatro funcionando, y apuntado en `mis_notas.md` qué pilló o qué rompió. Recortar el historial rompe alguna pregunta de seguimiento, y una comprobación de números da falsos avisos con los redondeos: lo que no vale es no saber cuáles.

## Cierre: lo que has visto

Responde por escrito, en `mis_notas.md`, con tus palabras:

- Después del reto de verdad del paso 12, ¿qué hay en `messages` en la tercera pregunta, y por qué pesa más que la primera?
- ¿Qué recuerda la pantalla y qué recibe el modelo? ¿Qué línea de tu código decide la diferencia?
- En el paso 13, ¿de dónde sale el número y de dónde sale la frase que lo rodea?
- ¿Qué cambió en el código de la pregunta del competidor con los ejemplos? ¿El de antes estaba mal, o calculaba otra cosa?
- En la pregunta 12, ¿qué parte puede darte el sistema y qué parte decides tú?

Guarda tu trabajo. Para antes la app con `Ctrl+C` o usa otra terminal del proyecto:

```text
git add exercises
git add mis_notas.md
git commit -m "Completo la sesión 3"
git status
```
