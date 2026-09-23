# De experimento a una demo compartida

Has construido un analista de FitLife, comprobado una cifra con Python y seguido las peticiones al modelo. Ahora otra persona debe poder abrir la app sin instalar Python. Desplegar significa ejecutar tu código en otro ordenador que atiende las visitas del navegador.

La entrada es `app.py`: usa las dos herramientas de `fitlife_tools.py`. Cada consulta puede hacer varias llamadas a la API. El código de acceso compartido limita la entrada a la demo; no identifica a cada usuario ni impone un presupuesto por persona.

## 1. Tu copia en GitHub

Un commit guarda tus archivos localmente. Un push los envía a GitHub. Un fork es una copia del repositorio dentro de tu cuenta, donde tienes permiso para publicar tus cambios.

1. En [el repositorio del taller](https://github.com/Kieleth/omda14-fitlife-workshop), pulsa **Fork**. Desmarca **Copy the main branch only** para copiar también las ramas de clase. Si ya tienes un fork, úsalo.
2. Copia la URL HTTPS de tu fork. Desde la raíz del proyecto, comprueba `git remote -v`: `origin` debe seguir apuntando al taller. Añade otro destino, sustituyendo `TU_USUARIO` por tu usuario real:

   ```text
   git remote add mi-fork https://github.com/TU_USUARIO/omda14-fitlife-workshop.git
   ```

   Si `mi-fork` ya existe, revisa su URL con `git remote -v`; no lo vuelvas a añadir. Si es incorrecta, corrígela con `git remote set-url mi-fork URL_CORRECTA`.
3. Comprueba `git branch --show-current`: debe mostrar `alumno/sesion-4`. Revisa y guarda tus cambios con un commit desde Source Control de VS Code. Incluye tus archivos de código; excluye claves y conversaciones descargadas.
4. Publica tu rama en tu copia:

   ```text
   git push mi-fork alumno/sesion-4
   ```

   Si pide autenticación, usa el inicio de sesión de GitHub que ofrece VS Code o tu gestor de credenciales. No pegues una clave de OpenAI como contraseña de GitHub.
5. Abre tu fork en GitHub, selecciona `alumno/sesion-4` y comprueba que ves `app.py`, `requirements.txt`, `fitlife_tools.py` y `data/`. El despliegue lee lo publicado, no los cambios que sigan solo en tu portátil.

## 2. Configurar y lanzar

Abre [Streamlit Community Cloud](https://share.streamlit.io/), conecta tu cuenta de GitHub y crea una app. Selecciona tu fork, la rama `alumno/sesion-4` y el archivo `app.py`. En **Advanced settings**, selecciona **Python 3.13**. Las dependencias están fijadas en `requirements.txt`; no hay paquetes que instalar a mano en el servidor. [Guía oficial de despliegue](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

En **Secrets**, usa el formato de [secrets.toml.example](.streamlit/secrets.toml.example) y sustituye los dos valores:

```toml
OPENAI_API_KEY = "clave-autorizada-para-esta-demo"
WORKSHOP_PASSWORD = "un-codigo-de-acceso-que-tu-elijas"
```

Usa una clave de un proyecto cuyo consumo puedas controlar y que tengas autorización para usar en la demo. No copies estos valores reales a GitHub. Las variables las necesita el proceso Python del servidor; la clave de API no se introduce en el chat. Si falta una de ellas, la app explica cuál y bloquea las consultas. [Gestión oficial de secretos](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

Guarda y despliega. Si falla el arranque, lee el primer error en los registros de Streamlit. Comprueba primero rama, `app.py`, Python 3.13 y las dos variables. Un error de acceso a un modelo se resuelve en el proyecto de API; reinstalar pandas no lo corrige.

Para probar esta misma entrada localmente, añade tu propio `WORKSHOP_PASSWORD` al `.env` que ya usas y ejecuta `app.py` con el comando de Streamlit de tu sistema, como en [SESION4.md](SESION4.md). No necesitas otro entorno ni nuevas dependencias.

## 3. Demostrar qué funciona

Abre la URL desplegada desde una ventana privada. Antes de introducir el código no debe aparecer el chat. Después:

1. Pregunta por socios activos del básico en el último mes. Comprueba periodo, población y resultado de la herramienta.
2. Haz una pregunta de seguimiento. Localiza ambas preguntas en la petición de API.
3. Abre otra ventana en otro navegador o dispositivo. Su conversación debe empezar vacía. El mismo código de acceso no implica un chat compartido.
4. Descarga tu conversación. Recarga y recupérala. La copia contiene mensajes y resultados: consérvala fuera de GitHub. El límite de este ejercicio es 1 MB y 1000 mensajes; si se supera, la app avisa y no ofrece una copia que no pueda recuperar.
5. Cambia un texto visible de `app.py`, haz commit y push a `mi-fork`. Comprueba que cambia en la URL. Has conectado un cambio de Git con una aplicación que se ejecuta en otro sitio.

Si un paso falla, anota entrada, resultado esperado, resultado observado y error. Una página que arranca demuestra el arranque, no que el análisis sea correcto.

## 4. De la demo a un servicio

| Tema | Qué tienes aquí | Qué tendrías que resolver con usuarios reales |
| :--- | :--- | :--- |
| Datos | CSV del caso, con meses y columnas conocidos. | Actualización, permisos y validación de esquema, fechas, duplicados y ausencias. |
| Ejecución | Dos funciones permitidas, argumentos comprobados y bucle de llamadas acotado. | Permisos por operación y pruebas de cada cálculo. Un prompt no convierte `exec` en un entorno aislado. |
| Historial | Memoria de sesión más exportación manual. | Almacenamiento, acceso por usuario, borrado y política de conservación. |
| Acceso y gasto | Código compartido; uso de tokens visible por llamada. | Identidad, límites de peticiones y controles de gasto. Un aviso de presupuesto no debe suponerse un corte automático. |
| Evaluación | Preguntas de FitLife y pruebas locales sin API. | Casos representativos, errores conocidos y comparaciones repetidas cuando cambien modelo, prompt o datos. |
| Entrega | GitHub instala dependencias y ejecuta tests en tres sistemas; Streamlit publica la rama elegida. | Revisión de cambios y recuperación de una versión anterior. Pasar tests no garantiza ausencia de fallos. |
| Operación | Detalle de peticiones y resultados en pantalla. | Registros con datos mínimos, tiempos, errores y una persona responsable de incidentes. |

Docker puede empaquetar el mismo entorno para otros alojamientos. No sustituye permisos, evaluación ni seguimiento del servicio. Las credenciales se inyectan al ejecutar, no se incorporan a una imagen. La capacidad y el coste se miden con la carga real; no se deducen del número de líneas del script.

**Para cerrar:** explica qué ordenador ejecutó Python, dónde estaba la clave, qué información recibió el modelo, quién calculó la cifra y qué prueba te permite confiar en ella.
