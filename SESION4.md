# Sesión 4: del analista que responde al sistema que puedes comprobar

Continúas con FitLife y sus doce preguntas. Los pasos 0 a 15 están resueltos en esta rama. Los pasos 12 a 15 conservan además la conversación en las peticiones de cálculo e interpretación. Hoy comprobarás esa continuidad, guardarás una investigación, darás al modelo herramientas concretas, compararás modelos y revisarás una respuesta contra su evidencia. Al final prepararás una demo accesible desde otro navegador.

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

**Construye el cambio.** Modifica `REVIEW_PROMPT` para que cada objeción cite el campo de evidencia que usa y separe error, supuesto y dato que falta. Después quítale la evidencia de una prueba y compara qué pierde. No consideres aprobada una respuesta solo porque dos modelos coinciden.

La pantalla conserva exactamente qué borrador se revisó. Si cambias el texto después, pide otra revisión: la anterior no evalúa el texto nuevo.

**Comprobación para continuar:** una afirmación sin respaldo detectada o un fallo del revisor documentado, y una comprobación independiente con Python. El último juicio sigue siendo tuyo.

## Cerrar el caso y abrir la app desde otro navegador

Vuelve a la pregunta 12: «¿Debería FitLife bajar el precio del plan básico?». Prepara una respuesta que separe tres cosas: qué dicen los datos, qué cambia bajo un supuesto explícito y qué no sabemos todavía. Guarda el cálculo y los argumentos que permitirían defenderla.

Después sigue [De experimento a una demo compartida](DE_EXPERIMENTO_A_PRODUCCION.md). La entrada de despliegue es `app.py`, con las dos herramientas, una clave en el servidor y un código de acceso al taller. Comprueba desde otra ventana que cada sesión tiene su propia conversación.

Para guardar tus cambios, usa otra terminal: `git status`, revisa `git diff`, añade solo los archivos que hayas modificado y haz un commit. Conserva aparte los JSON descargados. El resultado de la sesión es código, una investigación recuperable y evidencia para decidir qué funciona y qué falta.
