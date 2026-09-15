# OMDA14 · Instalación antes de clase

Al terminar tendrás el proyecto en tu portátil, las librerías instaladas en un entorno propio y una app de Streamlit que responde cuando cambias sus controles.

## 1. Herramientas

Instala [VS Code](https://code.visualstudio.com/download), [Git](https://git-scm.com/downloads) y [Python 3.13](https://www.python.org/downloads/). Selecciona una versión de la serie **3.13** con instalador para tu sistema. El taller fija la versión de Python en `.python-version`.

En Windows, el instalador de Python debe incluir el lanzador `py`. En macOS, el instalador oficial permite ejecutar `python3.13`. Si ya tienes otra versión o Anaconda, puedes conservarla: el entorno del taller estará en la carpeta `.venv`.

Crea también una [cuenta de GitHub](https://github.com/signup) para los ejercicios de Git. En VS Code instala la extensión **Python**, de Microsoft. El proyecto la recomienda al abrirse.

Abre una terminal nueva después de instalar las herramientas. En Windows usa PowerShell; en macOS usa Terminal.

Windows:

```powershell
py -3.13 --version
git --version
```

macOS:

```bash
python3.13 --version
git --version
```

Python debe mostrar `3.13.x`. Si un comando falla, resuélvelo antes de continuar. En macOS, `git --version` puede ofrecer instalar las herramientas de línea de comandos de Apple: acepta y vuelve a comprobarlo cuando termine.

## 2. Obtener el proyecto

**La dirección de GitHub se añadirá cuando el profesor confirme y publique el repositorio.** No clones el repositorio antiguo de MDA13 para preparar OMDA14.

Cuando tengas la dirección, abre en VS Code la carpeta clonada, llamada `omda14-fitlife-workshop`. Abre `Terminal > New Terminal`. Comprueba que ves `requirements.txt`, `check_setup.py`, `test_app.py` y `data/` en el explorador de archivos.

## 3. Crear el entorno e instalar las librerías

Un entorno es una carpeta que contiene su propio Python y sus librerías. Todos los comandos siguientes se ejecutan desde la carpeta del proyecto. Ejecútalos uno a uno; si alguno falla, corrige ese error antes de continuar.

### Windows · PowerShell

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe check_setup.py
.venv\Scripts\python.exe -m streamlit run test_app.py
```

### macOS · Terminal

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python check_setup.py
.venv/bin/python -m streamlit run test_app.py
```

Usamos la ruta del Python de `.venv` en todos los comandos. Así instalamos y ejecutamos siempre en el mismo entorno y no hace falta activar scripts de PowerShell.

`pip install -r requirements.txt` instala todas las dependencias del proyecto. No instales paquetes sueltos para arreglar un error: repite ese comando con el Python de `.venv`.

Para editar código, abre la paleta de comandos de VS Code, busca **Python: Select Interpreter** y selecciona el Python de `.venv`. El proyecto incluye esa carpeta como recomendación.

## 4. Comprobar la app

La terminal mostrará una dirección local, normalmente `http://localhost:8501`. Ábrela en tu navegador si no se abre sola. Mantén la terminal abierta.

En la página de OMDA14:

1. Comprueba que los chequeos aparecen en verde.
2. Cambia el número a **7**. El cuadrado debe pasar a **49** y debe aumentar el contador de ejecuciones.
3. Cambia el plan de FitLife. La tabla y el número de registros deben actualizarse.

Has probado que el navegador, Streamlit, Python y los archivos locales trabajan juntos. **Esto todavía no comprueba una conexión con un LLM.** No necesitas `.env` ni clave para pasar esta prueba.

Para parar la app, vuelve a la terminal y pulsa `Ctrl+C`.

## 5. Volver otro día

Abre la carpeta del proyecto en VS Code y su terminal. Ejecuta solo el último comando de tu sistema:

Windows:

```powershell
.venv\Scripts\python.exe -m streamlit run test_app.py
```

macOS:

```bash
.venv/bin/python -m streamlit run test_app.py
```

Conserva `.venv` en tu portátil. Git la ignora; no se sube al repositorio.

## Si algo falla

| Problema | Qué comprobar |
| :--- | :--- |
| `py` o `python3.13` no existe | Python 3.13 está instalado y has abierto una terminal nueva. En Windows, revisa que el instalador incluyó el lanzador `py`. |
| No se encuentra `requirements.txt` | Abre la carpeta del proyecto y ejecuta los comandos desde su terminal. |
| No se puede descargar un paquete | Revisa la conexión y el acceso a PyPI desde la red del centro. Repite la instalación completa; no desactives la verificación de certificados. |
| `No module named streamlit` | Usa el Python de `.venv` tanto para instalar como para abrir la app. |
| La versión de un paquete no coincide | Repite la instalación de `requirements.txt` en `.venv`. |
| Faltan datos o columnas | Recupera los CSV del repositorio. No inventes filas ni cambies el chequeo para que pase. |
| `Address already in use` | Puede haber otra app abierta. Busca su terminal y párala con `Ctrl+C`, o usa la URL que ya está abierta. |
| La página deja de responder | Comprueba que la terminal que ejecuta Streamlit sigue abierta y no muestra un error. |

Si necesitas ayuda, indica tu sistema operativo, el comando que ejecutaste y el texto completo del error. No compartas claves ni el contenido de `.env`.

## Antes de la primera sesión

- [ ] `check_setup.py` termina sin errores.
- [ ] La app abre y responde a los dos controles.
- [ ] Has leído [el caso FitLife](ENUNCIADO.md).
- [ ] Puedes abrir el proyecto y su terminal en VS Code.

La conexión al modelo, la clave de la API y cualquier instalación para ejecutar modelos locales se prepararán por separado. No son requisitos de esta primera comprobación.

Referencias: [instalación de Streamlit](https://docs.streamlit.io/get-started/installation/command-line), [entornos virtuales de Python](https://docs.python.org/3.13/library/venv.html).
