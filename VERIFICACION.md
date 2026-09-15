# OMDA14 · Verificación de la instalación

Fecha: 14 de septiembre de 2026.

## Instalación desde cero

[GitHub Actions](https://github.com/Kieleth/omda14-fitlife-workshop/actions/runs/34928208238) comprobó el commit `033b2b0662f0c2b59c7821d52e9fda65775a34b5`: instalación y quince tests correctos en Windows, macOS y Linux.

En cada sistema se clonó el repositorio, se creó `.venv` con Python 3.13, se instalaron todas las dependencias desde `requirements.txt`, y se ejecutaron `pip check`, `check_setup.py` y los tests. Esto comprueba la instalación y las interacciones locales de Streamlit en los entornos de GitHub Actions. Cada alumno debe completar también la prueba de navegador en su portátil.

Los tests incluyen los errores de configuración y datos, controles de Streamlit sin credenciales ni conexión de red, conservación exacta de los 16 ejercicios, el extra y los dos CSV originales en `main`, y protección frente a instrucciones antiguas de instalación o de descarte del trabajo.

La prueba inicial de Windows detectó conversión de saltos de línea durante el checkout. `.gitattributes` conserva LF y un test reproduce un checkout con `core.autocrlf=true` en todos los sistemas. El fallo quedó corregido y los tres sistemas pasaron.

## Comprobación local en macOS

Se creó un entorno vacío con Python 3.13.3 en macOS ARM64. La instalación y `pip check` terminaron correctamente. También se arrancó `test_app.py` y se comprobó en un navegador real:

- Elegir 7 mostró 49 y aumentó el contador de ejecuciones.
- Cambiar el plan de `basic` a `premium` cambió el recuento de 4.480 a 6.826 y la tabla mostró filas del plan premium.

El entorno temporal de verificación no se distribuye. Cada alumno crea `.venv` siguiendo [SETUP.md](SETUP.md).

## Preparación y primera práctica

[SETUP.md](SETUP.md), [SESION1_CHECKLIST.md](SESION1_CHECKLIST.md) y [ACTUALIZAR.md](ACTUALIZAR.md) describen los requisitos, la instalación, las comprobaciones y cómo conservar el trabajo al actualizar. Las instrucciones actuales usan `.venv`.

La primera práctica se prepara en [`codex/sesion-1`](https://github.com/Kieleth/omda14-fitlife-workshop/tree/codex/sesion-1). Su [registro de verificación](https://github.com/Kieleth/omda14-fitlife-workshop/blob/codex/sesion-1/VERIFICACION.md) separa la app de la explicación HTML y documenta sus límites.

La actualización de documentación que enlaza esa rama no cambia el código, los datos, las dependencias ni los tests de instalación comprobados.

## Límites

No se han probado llamadas a una API de LLM ni la ejecución de un modelo local. Conservar los ejercicios originales no demuestra su compatibilidad completa con las versiones fijadas. La adaptación de los siguientes ejercicios y de las otras sesiones sigue pendiente.
