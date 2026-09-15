# Verificación de la instalación de OMDA14

Fecha: 14 de septiembre de 2026.

## Comprobado

Se creó un entorno vacío con Python 3.13.3 en macOS ARM64 y se ejecutó `pip install -r requirements.txt`. La instalación terminó correctamente; `pip check` no detectó incompatibilidades.

Los nueve chequeos del entorno pasaron. Los trece tests automáticos pasaron, incluidos los controles de Streamlit sin credenciales ni conexión de red, los errores de configuración y datos, y la conservación exacta de los 16 ejercicios, el extra y los dos CSV originales.

También se arrancó Streamlit y se comprobó la app en un navegador real:

- El control numérico pasó a 7 y el resultado a 49.
- El contador mostró nuevas ejecuciones del script.
- El plan cambió de `basic` a `premium` y los registros pasaron de 4.480 a 6.826; la tabla mostró filas del plan `premium`.

Los archivos se ejecutaron desde el nuevo repositorio, usando un entorno temporal de verificación fuera del repositorio. Ese entorno no se distribuye: cada alumno crea su propio `.venv` con las instrucciones de `SETUP.md`.

El primer chequeo en Windows detectó que Git convertía los saltos de línea de los 19 archivos originales. La instalación de paquetes, el chequeo del entorno y los controles de la app sí pasaron. `.gitattributes` fija los saltos de línea LF para todos los sistemas. Un test reproduce una extracción de Git con `core.autocrlf=true`: falló antes de la corrección y pasó después.

## Publicación

El repositorio público es [Kieleth/omda14-fitlife-workshop](https://github.com/Kieleth/omda14-fitlife-workshop). La guía [SETUP.md](SETUP.md) incluye los comandos para clonar `main` e instalar el taller.

## Instalación en Windows, macOS y Linux

[La ejecución de GitHub Actions](https://github.com/Kieleth/omda14-fitlife-workshop/actions/runs/34927723265) terminó correctamente en los tres sistemas para el commit `4e025bcad0e2e6c2405efcd187a85741da31ba9b`.

En cada sistema se clonó el repositorio, se creó `.venv` con Python 3.13, se instalaron las dependencias desde `requirements.txt`, se ejecutaron `pip check` y `check_setup.py`, y pasaron los trece tests. Esto comprueba la instalación y las interacciones locales de Streamlit en los entornos de GitHub Actions. No sustituye la prueba de apertura en el navegador de cada portátil.

El commit posterior que registra estos resultados solo cambia documentación; el código, los datos, las dependencias y la configuración comprobados siguen siendo los mismos.

## Pendiente

No se han probado llamadas a una API ni la ejecución de un modelo local. Los ejercicios originales se han conservado; eso no demuestra su compatibilidad completa con las versiones fijadas. Las ramas de las sesiones y las explicaciones HTML siguen pendientes de diseño y adaptación.
