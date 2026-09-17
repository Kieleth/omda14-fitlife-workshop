# OMDA14 · Instalación antes de clase

Al terminar tendrás el proyecto en tu portátil, las librerías instaladas en un entorno propio y una app de Streamlit que responde cuando cambias sus controles.

## 1. Herramientas

Instala [VS Code](https://code.visualstudio.com/download), [Git](https://git-scm.com/downloads) y [Python 3.13.15](https://www.python.org/downloads/release/python-31315/#files). En la tabla **Files**, elige **Windows installer (64-bit)** para un PC habitual o **macOS installer** para Mac. Si tu PC utiliza Windows ARM, pregunta en el chat del curso antes de instalar. El taller fija la versión de Python en `.python-version`.

En Windows, el instalador de Python debe incluir el lanzador `py`. En macOS, el instalador oficial permite ejecutar `python3.13`. Si ya tienes otra versión o Anaconda, puedes conservarla: el entorno del taller estará en la carpeta `.venv`.

Git guarda versiones de tus archivos en tu ordenador. GitHub es la web donde está publicado el proyecto. Crea también una [cuenta de GitHub](https://github.com/signup) para usarla durante el curso. En VS Code instala la extensión **Python**, de Microsoft. El proyecto la recomienda al abrirse.

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

El repositorio es público: [Kieleth/omda14-fitlife-workshop](https://github.com/Kieleth/omda14-fitlife-workshop).

Un repositorio es la carpeta del proyecto con su historial. Clonar descarga una copia a tu ordenador. Abre VS Code y usa **File > Open Folder** para elegir **Documentos** como carpeta donde guardarla. Después abre **Terminal > New Terminal**: la terminal empieza en la carpeta seleccionada. Ejecuta ahí estos comandos:

```text
git clone https://github.com/Kieleth/omda14-fitlife-workshop.git
cd omda14-fitlife-workshop
git branch --show-current
```

El último comando debe mostrar `main`. Clonar un repositorio público por HTTPS no requiere contraseña ni token.

Abre esa carpeta en VS Code con **File > Open Folder**. Abre **Terminal > New Terminal**. Comprueba que ves `requirements.txt`, `check_setup.py`, `test_app.py` y `data/` en el explorador de archivos. Desde esa terminal puedes seguir los comandos de instalación de tu sistema.

## 3. Crear el entorno e instalar las librerías

Antes de ejecutar los comandos, identifica qué hace cada pieza:

| Pieza | Para qué sirve |
| :--- | :--- |
| Python 3.13 | Ejecuta el código; `.python-version` indica la serie usada en el taller. |
| `venv` y `pip` | Vienen con Python: el primero crea el entorno y el segundo instala las librerías. |
| `requirements.txt` | Fija todas las dependencias; es el único archivo que instala el alumnado. |
| `pip check` | Detecta dependencias instaladas incompatibles o ausentes. |
| `check_setup.py` | Comprueba Python, el entorno, Git, las librerías y los dos CSV. |
| `test_app.py` | Comprueba en el navegador que Python y Streamlit responden a tus acciones. |

La primera instalación necesita acceso a internet para descargar los paquetes. La comprobación local posterior no llama a una API.

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

Ejecuta únicamente el bloque de tu sistema operativo.

Usamos la ruta del Python de `.venv` en todos los comandos. Así instalamos y ejecutamos siempre en el mismo entorno y no hace falta activar scripts de PowerShell.

`pip install -r requirements.txt` instala todas las dependencias del proyecto. No instales paquetes sueltos para arreglar un error: repite ese comando con el Python de `.venv`.

Para editar código, abre la paleta de comandos de VS Code, busca **Python: Select Interpreter** y selecciona el Python de `.venv`. El proyecto incluye esa carpeta como recomendación.

## 4. Comprobar la app

La terminal mostrará una dirección local, normalmente `http://localhost:8501`. Ábrela en tu navegador si no se abre sola. Mantén la terminal abierta.

En la página de OMDA14:

1. Comprueba que las comprobaciones aparecen en verde.
2. Cambia el número a **7**. El cuadrado debe pasar a **49** y debe aumentar el contador de ejecuciones.
3. Cambia el plan de FitLife. La tabla y el número de registros deben actualizarse.

Has probado que el navegador, Streamlit, Python y los archivos locales trabajan juntos. **Esto todavía no comprueba una conexión con un LLM (modelo de lenguaje).** No necesitas `.env` ni clave para pasar esta prueba.

Para parar la app, vuelve a la terminal y pulsa `Ctrl+C`.

**Ya estás preparado. La aplicación se construye en clase, siguiendo el README.**

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
| Faltan datos o columnas | Recupera los CSV del repositorio. No inventes filas ni cambies la comprobación para que pase. |
| `Address already in use` | Puede haber otra app abierta. Busca su terminal y párala con `Ctrl+C`, o usa la URL que ya está abierta. |
| La ruta a `data/` es correcta y sigue fallando, o la terminal muestra `Network URL` y `External URL` | Has arrancado la app desde otra carpeta. Vuelve a la raíz del proyecto (`cd ..` si estás en `exercises/`) y repite el comando. |
| La página deja de responder | Comprueba que la terminal que ejecuta Streamlit sigue abierta y no muestra un error. |

Si necesitas ayuda, indica tu sistema operativo, el comando que ejecutaste y el texto completo del error. No compartas claves ni el contenido de `.env`.

## Antes de la primera sesión

- [ ] `check_setup.py` termina sin errores.
- [ ] La app abre y responde a los dos controles.
- [ ] Has leído [el caso FitLife](ENUNCIADO.md).
- [ ] Puedes abrir el proyecto y su terminal en VS Code.

La conexión al modelo, la clave de la API y cualquier instalación para ejecutar modelos locales se prepararán por separado. No son requisitos de esta primera comprobación.

Referencias: [instalación de Streamlit](https://docs.streamlit.io/get-started/installation/command-line), [entornos virtuales de Python](https://docs.python.org/3.13/library/venv.html).

Para actualizar el proyecto y conservar tus cambios, sigue [ACTUALIZAR.md](ACTUALIZAR.md). La lista de preparación está en [SESION1_CHECKLIST.md](SESION1_CHECKLIST.md).
