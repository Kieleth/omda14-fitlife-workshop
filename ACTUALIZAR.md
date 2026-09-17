# OMDA14 · Actualizar y conservar tu trabajo

Abre la carpeta `omda14-fitlife-workshop` y la terminal de VS Code. Antes de descargar o cambiar de rama, mira dónde estás y qué has cambiado:

```text
git branch --show-current
git status
```

## Si tienes cambios sin guardar en Git

Haz un commit antes de actualizar o cambiar de rama. Un commit guarda una versión en tu ordenador; no publica nada en GitHub.

Si todavía estás en `main` o en una rama `clase/`, crea primero una rama propia. Por ejemplo, si `alumno/preparacion` no existe:

```text
git switch -c alumno/preparacion
```

Los cambios siguen en tu carpeta al crear esa rama. En VS Code, abre **Source Control**, revisa el diff de cada archivo, añade solo los archivos del ejercicio con **Stage Changes** y escribe un mensaje antes de pulsar **Commit**. No añadas claves, `.env` ni `.venv`.

Si Git pide tu identidad, configúrala una vez para este repositorio, sustituyendo los ejemplos por tus datos:

```text
git config user.name "Tu nombre"
git config user.email "tu-correo-de-GitHub"
```

Puedes usar la dirección privada que GitHub muestra en **Settings > Emails**. Después repite el commit y comprueba `git status`. Si no tienes claro qué guardar, conserva los archivos y pide ayuda en el chat del curso antes de seguir.

## Actualizar la preparación de main

Cuando `git status` indique que no hay cambios pendientes:

```text
git switch main
git pull --ff-only
```

`--ff-only` permite actualizar cuando no hace falta combinar historias distintas. Si falla, conserva el mensaje y pide ayuda; no borres cambios para forzar la actualización. `Already up to date` significa que no había novedades.

## Entrar en una sesión

Sigue los comandos de la guía de esa sesión: primero se descarga la rama de la clase y después se crea una rama de alumno a partir de ella. No hagas `git pull` a ciegas dentro de tu rama de ejercicios. Integrar material nuevo en una rama donde ya has trabajado se explica en la guía de esa sesión.

Para descargar la información de las ramas disponibles sin cambiar tus archivos:

```text
git fetch origin
git branch --remotes
```

## Volver a comprobar las dependencias

Tras actualizar o entrar en una sesión, ejecuta desde la carpeta del proyecto:

Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe check_setup.py
```

macOS:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python check_setup.py
```

La carpeta `.venv` sigue en tu ordenador al cambiar de rama. Las dependencias las declara cada versión de `requirements.txt`. Si falta el entorno, sigue [SETUP.md](SETUP.md) desde el paso de crear `.venv`.
