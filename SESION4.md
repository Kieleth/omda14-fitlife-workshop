# Sesión 4: del analista que responde al sistema que puedes comprobar

Continúas con FitLife y sus doce preguntas. Los pasos 0 a 15 están resueltos en esta rama. Los pasos 12 a 15 conservan además la conversación en las peticiones de cálculo e interpretación. Hoy comprobarás esa continuidad, guardarás una investigación, darás al modelo herramientas concretas, compararás modelos, revisarás una respuesta contra su evidencia, incorporarás documentos y pedirás gráficos sobre los datos. Al final prepararás una demo accesible desde otro navegador.

## Preparar tu rama sin perder la sesión 3

Para la app que esté ejecutándose con `Ctrl+C`. En otra terminal del proyecto:

```text
git branch --show-current
git status
```

Si tienes cambios, guárdalos primero en tu rama actual. En Source Control de VS Code, revisa cada archivo, selecciona los ejercicios y notas que quieras conservar y haz un commit. No añadas `.env`, claves ni conversaciones descargadas. Un archivo sin seguimiento puede ser una práctica tuya: consérvalo y revisa su contenido antes de decidir si va al commit. [ACTUALIZAR.md](ACTUALIZAR.md) explica el proceso.

Cuando `git status` muestre `nothing to commit, working tree clean`:

```text
git fetch origin
git switch -c alumno/sesion-4 origin/clase/sesion-4
git branch --show-current
```

El último comando debe mostrar `alumno/sesion-4`. Si ya existe, vuelve con `git switch alumno/sesion-4`. Tu sesión 3 sigue en su rama. Quien empieza desde main sigue los mismos comandos después de completar [SETUP.md](SETUP.md). Se usan el mismo `.venv`, las mismas dependencias y la misma clave de API.

### Traer tus notas

El archivo `mis_notas.md` que guardaste en la sesión 3 sigue en aquella rama. Mira primero si ya existe en la carpeta actual: si está, conserva esa versión y no ejecutes el bloque siguiente, porque la sustituiría. Si no está y lo habías guardado con un commit en `alumno/sesion-3`, cópialo:

```text
git restore --source=alumno/sesion-3 -- mis_notas.md
git add mis_notas.md
git commit -m "Traigo mis notas a la sesion 4"
```

Esto copia solo ese archivo, sin cambiar tus ejercicios ni borrar la versión de la otra rama. Si tus notas están en otra rama, sustituye `alumno/sesion-3` por su nombre. Si Git no encuentra el archivo, no estaba guardado allí: vuelve a la rama anterior para localizarlo. Si nunca creaste notas, puedes crear ahora `mis_notas.md` en la raíz del proyecto.

Abre `exercises/paso_15.py`. Para ver qué cambió frente a la sesión anterior:

```text
git diff origin/clase/sesion-3 -- exercises/paso_15.py
```

Pulsa `q` si Git muestra una pantalla con `(END)`. Un commit guarda archivos de código. No guarda por sí solo el chat que estaba en memoria.

## Arrancar cada ejercicio

Desde la raíz del proyecto, usa solo el comando de tu sistema. Para cambiar de ejercicio, para el anterior con `Ctrl+C` y cambia el número del archivo.

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run exercises/paso_16.py
```

macOS:

```bash
.venv/bin/python -m streamlit run exercises/paso_16.py
```

La instalación no cambia. Cada archivo tiene un reto en su cabecera. No hace falta resolver todos los retos avanzados para continuar.

## Paso 16: tres significados de «recordar»

**Predice primero.** Envías otra pregunta, cambias un interruptor, recargas el navegador y paras Python. ¿En cuáles deberían sobrevivir los mensajes? ¿Qué parte depende del navegador y qué parte de tu código?

Haz tres preguntas: «¿Cuántos planes tiene FitLife?», «¿Cuál tiene más socios distintos?» y «¿Y el básico?». Deben quedar visibles tus tres preguntas. Cambia **Mostrar código**: siguen los mensajes y el detalle de cada turno. Abre el de la última respuesta y localiza las preguntas anteriores dentro de `peticion_inicial`.

La pantalla se reconstruye desde `st.session_state`. La API recibe la lista que construye tu código. Son dos mecanismos distintos. En esta rama el historial se envía tanto para calcular como para interpretar. Los campos de pantalla, como `code` y `details`, no se copian como campos adicionales del mensaje de API.

**Construye el cambio.** En `chat_history.py`, lee `api_messages`. En el paso 16, sustituye el bloque que construye `messages` por una llamada a esa función e impórtala junto a las otras funciones del módulo. Hay una segunda petición dentro de `interpret_result`: construye también su `messages` con `api_messages(interp_prompt, history)`. Comprueba que las dos siguen enviando el mismo contenido que antes. Después cambia `api_messages` para enviar solo dos turnos completos anteriores y la nueva pregunta: en una conversación alternada son las últimas cinco entradas, más el `system` que se añade aparte. Haz una pregunta que dependa del principio. La pantalla debe seguir completa aunque ambas peticiones reciban menos contexto. Si solo cambias la primera, la interpretación seguirá recibiendo toda la conversación y la prueba no demostrará ese límite.

**Termina el experimento:** `api_messages` también se usa en las herramientas, los gráficos y la demo final. Si dejas `history[-5:]`, esas apps heredarán el límite aunque muestren todo el chat. Anota la diferencia observada y quita ese recorte antes de seguir: vuelve a recorrer `history` completo en el helper. Conserva las dos llamadas al helper que acabas de construir en el paso 16. Envía otra pregunta y comprueba que su petición incluye de nuevo el principio de la conversación.

**Recupera una investigación.** Descarga el JSON con **Guardar conversación**, recarga el navegador y comprueba que la sesión nueva está vacía. Selecciona el archivo y pulsa **Recuperar conversación**. Deben volver preguntas, respuestas, código y detalles sin una nueva llamada al modelo. Prueba una copia del JSON a la que hayas quitado `content` de un mensaje: debe mostrar un error y conservar el chat actual.

Recuperar sustituye el chat abierto. Guarda primero el actual si quieres conservar ambos. Este mecanismo es una copia que tú descargas, no una base de datos que sincroniza dispositivos. El archivo contiene lo hablado y sus resultados; no lo subas al repositorio.

**Comprobación para continuar:** tres preguntas visibles tras un rerun, esas preguntas localizadas en una petición completa, y una conversación recuperada después de recargar. Apunta las tres pruebas y qué conserva cada una.

## Paso 17: de generar código a elegir una herramienta

Abre `explicaciones/herramientas.html` con doble clic desde tu explorador de archivos. Avanza por las seis etapas y responde antes de desplegar la explicación. Es una simulación sin API; después busca los mismos elementos en la petición real de la app.

En el paso 15 el modelo podía escribir código que ejecutábamos. Aquí recibe nombres de funciones y una descripción de sus argumentos. Puede pedir una llamada; Python comprueba el nombre, los argumentos y los datos, ejecuta una función concreta y devuelve el resultado. El modelo redacta a partir de ese resultado. No instalamos un framework de agentes.

Pregunta «¿Cuántos socios activos tiene el básico y cuál es su churn en el último mes de los datos?». En **Detalle de este turno**, sigue `request`, `tool_calls`, `tool_results` y la respuesta final. Relaciona el `id` de la llamada con `tool_call_id` del resultado. Señala dónde se hizo la división del churn: está en Python.

**Construye el cambio.** Pregunta qué ingreso tendría el básico con un precio de 24 euros. La app empieza ofreciendo solo `resumen_plan`. En `HERRAMIENTAS`, añade la segunda definición de `TOOLS`. Lee `escenario_precio` antes de repetir: mantiene la población activa fija y la compara con el importe realmente pagado, que puede incluir descuentos. No presupone que todos pagaban 29 euros.

Verifica el cálculo en el código: mes seleccionado, socios activos, suma de `price_paid`, número de activos multiplicado por 24 y diferencia. ¿Ese resultado demuestra que se reducirán las bajas? ¿Qué dato haría falta para responderlo?

**Ampliación opcional: construye una herramienta propia.** Elige otra pregunta de [PREGUNTAS_TEST.md](PREGUNTAS_TEST.md). Antes de programar, escribe qué filas cuentan, de qué periodo y en qué unidades devolverás el resultado. Añade una función en `fitlife_tools.py`, su definición en `TOOLS` y el nombre permitido en `execute_tool`. Prueba la función con una tabla pequeña cuyo resultado conozcas. Después ofrécela al modelo.

**Comprobación para continuar:** una llamada que ejecuta `escenario_precio`, su resultado comprobado y una pregunta que esas herramientas no pueden resolver. La herramienta propia es opcional. Que la API acepte un argumento no demuestra que hayas definido bien el cálculo.

## Paso 18: comparar sin elegir por la calidad de la prosa

Primero escribe la condición de acierto. Usa una pregunta con periodo y población explícitos. La app incluye una comprobación con pandas del básico en el último mes; si cambias la pregunta, construye también su comprobación correspondiente.

Selecciona dos candidatos y pulsa **Comparar**. Todos reciben la misma pregunta y las mismas herramientas, en conversaciones nuevas. Compara exactitud, límites reconocidos, llamadas, segundos y tokens. Descarga el JSON. Un error de permisos o cuota no cuenta como una respuesta incorrecta: anótalo como una ejecución no realizada.

`o4-mini` permite tratar el tema de modelos de razonamiento. Puede requerir acceso adicional en tu proyecto. Los detalles muestran el uso que devuelve la API, no su razonamiento interno. Más tiempo o más tokens no garantizan una mejor respuesta. No es necesario cambiar de modelo para completar los otros pasos.

**Construye el cambio.** Añade a cada resultado tu veredicto (`correcta`, `parcial`, `inventada`, `no puede`) y una justificación. Guarda también esos campos en el JSON. Repite la comparación y decide qué evidencia te haría cambiar de elección.

**Comprobación para continuar:** misma tarea, criterio escrito antes de ver respuestas y comparación guardada. Una ejecución es una observación, no un ranking definitivo.

## Paso 19: un analista y un revisor

Orquestar es decidir qué llamada ocurre, con qué información y después de cuál. Aquí hay dos papeles explícitos, que pueden usar el mismo modelo: uno consulta herramientas y redacta; otro recibe pregunta, borrador y resultados calculados para revisarlos.

Genera el análisis. Antes de revisarlo, añade al borrador «Bajar a 24 euros reducirá las bajas un 20 %». Pide la revisión. Abre la petición del revisor y busca el dato que justificaría ese 20 %. Ahora prueba con una respuesta correcta. ¿El revisor distingue ambas o critica por sistema?

**Construye el cambio.** `REVIEW_PROMPT` ya pide citar el campo de evidencia de cada objeción. Conserva esa instrucción y añade una salida separada en **error**, **supuesto** y **dato que falta**, con un ejemplo de objeción válida. Después quítale la evidencia de una prueba y compara qué pierde. Restaura el envío de evidencia antes de continuar. No consideres aprobada una respuesta solo porque dos modelos coinciden.

La pantalla conserva exactamente qué borrador se revisó. Si cambias el texto después, pide otra revisión: la anterior no evalúa el texto nuevo.

La pregunta del análisis guardado también queda visible. Si editas la pregunta superior, pulsa **Generar análisis** para obtener nuevos datos y borrador. Hasta que esa petición termine correctamente, la revisión sigue usando la pregunta y la evidencia anteriores.

**Comprobación para continuar:** una afirmación sin respaldo detectada o un fallo del revisor documentado, y una comprobación independiente con Python. El último juicio sigue siendo tuyo.

## Paso 20: el CSV no contiene la respuesta

Arranca `exercises/paso_20.py` con el mismo comando de Streamlit. Pregunta «¿Con cuántos días de antelación hay que solicitar la baja?». Es una condición comercial, no una cuenta sobre filas. Los tres documentos de `data/conocimiento/` son ficticios y están marcados como tales.

Abre también `explicaciones/documentos.html` con doble clic desde el explorador de archivos: permite cambiar la selección y ver el contexto que prepararíamos, sin llamar a la API.

### Cargar no significa entrenar

El archivo contiene texto. Python lo lee y lo divide en fragmentos, conservando el nombre, la sección y un identificador que cambia si cambia el contenido. Después tu programa decide qué fragmentos enviar junto a la pregunta. El modelo recibe ese texto en esa petición. No se han cambiado los parámetros aprendidos del modelo ni se han insertado los documentos en sus conocimientos permanentes.

**Predice antes de enviar:** ¿qué podrá contestar con cada modo?

1. **Sin documentos.** Inspecciona la lista vacía y envía la pregunta. Una respuesta que reconoce que falta la política es válida. Si inventa una regla, anótala como fallo.
2. **Todos los fragmentos.** Lee lo cargado, envía la misma pregunta y abre la fuente citada. Busca la frase concreta y sus condiciones. Comprueba en la petición que viaja el texto, no solo el nombre del archivo.
3. **Buscar fragmentos.** Tu código cuenta palabras compartidas y selecciona los primeros resultados. Mira `matched_words` y `score`: son coincidencias de palabras, no probabilidades. Cambia el máximo de fragmentos y observa qué información entra o queda fuera.

Encontrar información y añadirla a la petición antes de generar la respuesta se llama **RAG**, del inglés *retrieval-augmented generation*. Esta búsqueda sencilla permite ver cada paso. Un sistema mayor podría buscar por similitud semántica mediante embeddings, representaciones numéricas del texto, pero también tendría que comprobar que recuperó la evidencia necesaria. [Explicación oficial de recuperación y contexto](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy).

La app valida el formato de la respuesta y que los identificadores citados existan entre los fragmentos enviados. Eso no demuestra que la fuente respalde la conclusión: lee el párrafo. Un resultado con `status=supported` es una declaración del modelo, no una certificación de Python.

### Construye una mejora de búsqueda

En `fitlife_documents.py`, localiza `words` y `retrieve`. Prueba el término «anulación» y después «baja» en la consulta. La primera palabra no aparece en los documentos; compara los fragmentos recuperados sin llamar a la API.

Añade un pequeño diccionario de sinónimos que convierta `anulacion` en `baja` antes de comparar palabras. Conserva ambos términos si necesitas buscar los dos. Repite las dos consultas y explica por qué ha cambiado el resultado. Después comprueba una pregunta ajena, como «¿hay clases de natación?»: añadir sinónimos no crea la información que falta.

### Incorpora tu propio documento

Crea un archivo `.md` o `.txt` en UTF-8 con una condición inventada y un título. Por ejemplo: «Las taquillas violetas usan el código tulipán». Súbelo con el selector de archivos, revisa sus fragmentos y confirma que está seleccionado entre los documentos disponibles. El límite por archivo es 200 KB. Se usan textos legibles para observar el mecanismo; esta versión no extrae texto de PDF ni de escaneos.

Pregunta por esa condición con **Todos los fragmentos**. Excluye después ese documento y repite. Cada envío es una consulta independiente: la respuesta anterior no se añade como historial oculto. La respuesta guardada identifica la pregunta y el modo con que se obtuvo, y avisa si después cambias la selección.

**Prueba de límite.** Pregunta si la promoción de enero cambia el plazo de baja. Comprueba si hacen falta la política de bajas y la promoción. Si la búsqueda solo recupera una, ajusta la consulta o el número de fragmentos. Una respuesta fluida no corrige una búsqueda incompleta.

**Ampliación.** Sube otra versión, con otro nombre, que establezca un plazo diferente. ¿Señala el conflicto? ¿Qué fecha o condición necesitaría para decidir cuál aplica? No presupongas que el primer resultado es la política vigente.

**Comprobación para continuar:** un documento propio visible dentro de la petición, una respuesta con su fuente comprobada, una consulta sin respaldo reconocida como tal y una mejora de búsqueda que puedas explicar. Guarda el JSON de una consulta fuera del repositorio.

## Paso 21: gráficos que responden a preguntas

Arranca `exercises/paso_21.py`. Predice primero si el churn del básico es constante durante el periodo. Pide «Dibuja el churn mensual por plan durante 2024». Sigue cuatro objetos: la pregunta, los argumentos de `crear_grafico`, la tabla que calcula Python y el gráfico que dibuja Streamlit.

El modelo elige una métrica, un intervalo, una agrupación y un tipo de gráfico. Python comprueba esos argumentos y calcula los valores con pandas. No acepta una lista de cifras inventada por el modelo. La tabla descargable contiene exactamente los puntos representados, junto con el número de registros de cada grupo.

Prueba después:

- «Ahora en barras». Comprueba que los dos gráficos siguen visibles tras otra ejecución.
- «Compara los socios activos por centro en diciembre de 2024». Busca qué filas cuentan y qué significa `active_members`.
- «Dibuja los ingresos del básico mes a mes durante 2024». Comprueba que suma `price_paid` de registros activos, incluidos los descuentos.
- «Dibuja los ingresos de 2030». Un periodo sin datos debe dar un error explicado, no una serie de ceros.

El intervalo omitido se interpreta como el último mes y se muestra. Una evolución sin periodo usa los meses disponibles. Revisa siempre esos filtros. Las líneas representan meses; las barras comparan categorías. El CSV termina en 2024: «último mes» no significa hoy.

### Una pregunta de negocio antes del dibujo

«¿Qué plan tiene más socios?» admite varias cuentas. Pide tres gráficos de barras por plan: registros socio-mes en todo el periodo (`member_records`), socios distintos en todo el periodo (`distinct_members`) y activos del último mes (`active_members`). Escribe cuál quieres antes de pedir el gráfico. La posición de un plan puede cambiar al cambiar la población.

El churn agrupado sobre varios meses divide bajas entre registros socio-mes, no entre personas distintas. Una media global puede ocultar cambios mensuales. En una serie con meses ausentes, esta app rechaza el gráfico para que no interpretes una línea continua como evidencia de los puntos que faltan.

### Construye una métrica

Añade `churned_records`, el número de registros con `status == 'churned'`, a `METRICS` y a la selección de cálculos de `build_chart` en `fitlife_charts.py`. Añadir solo el nombre debe producir un error: falta implementar la operación.

Compruébala con cuatro registros: tres activos y una baja. El número de bajas debe ser 1 y la tasa, 25 %. Repite con tres activos y dos bajas: 2 y 40 %. Después pide ambos gráficos sobre FitLife y explica por qué número y porcentaje responden preguntas distintas.

**Comprobación para continuar:** gráfico solicitado en lenguaje natural, una cifra contrastada en su tabla, una métrica añadida por ti y una limitación explícita. Descarga la conversación, recupérala y verifica que vuelven los gráficos sin consultar de nuevo al modelo. La copia conserva el resultado calculado entonces; no recalcula un CSV que haya cambiado después.

## Cerrar el caso y abrir la app desde otro navegador

Vuelve a la pregunta 12: «¿Debería FitLife bajar el precio del plan básico?». Prepara una respuesta que separe tres cosas: qué dicen los datos, qué cambia bajo un supuesto explícito y qué no sabemos todavía. Guarda el cálculo y los argumentos que permitirían defenderla.

Después sigue [De experimento a una demo compartida](DE_EXPERIMENTO_A_PRODUCCION.md). La entrada de despliegue es `app.py`, con un selector de Cálculos, Documentos y Gráficos, una clave en el servidor y un código de acceso al taller. Comprueba desde otra ventana que cada sesión tiene su propia conversación. Las consultas de documentos siguen siendo independientes, como en el paso 20.

Para guardar tus cambios, usa otra terminal: `git status`, revisa `git diff`, añade solo los archivos que hayas modificado y haz un commit. Conserva aparte los JSON descargados. El resultado de la sesión es código, una investigación recuperable y evidencia para decidir qué funciona y qué falta.
