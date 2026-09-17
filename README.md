# OMDA14 · Analítica conversacional con IA

Vas a construir, paso a paso, una aplicación para explorar los datos de FitLife y hacer preguntas a un modelo de lenguaje: añadirás código, probarás lo que cambia y explicarás qué has observado. Esta rama, `main`, contiene solo la preparación. Los ejercicios de cada sesión se publican en su propia rama y se descargan al empezar la sesión.

## Antes de la sesión 1

1. Sigue [la guía de instalación](SETUP.md) de tu sistema operativo.
2. Comprueba que la app de prueba abre y responde a sus controles.
3. Lee [el caso FitLife](ENUNCIADO.md).

**Cuando termines la comprobación, ya estás preparado.** No necesitas una clave de acceso a un modelo para esta preparación; la clave del curso se usa a partir del paso 5 de la sesión.

## Cuando empiece la sesión 1

Los ejercicios y su guía están en la rama `clase/sesion-1`. Abre la carpeta del proyecto en VS Code, abre **Terminal > New Terminal** y ejecuta:

```text
git fetch origin
git switch -c alumno/sesion-1 origin/clase/sesion-1
```

`fetch` descarga lo publicado para la clase. `switch -c` crea tu rama, `alumno/sesion-1`, a partir de la rama de la clase; en ella quedan tus cambios, en tu ordenador. Al cambiar de rama aparecen en la carpeta `exercises/`, `explicaciones/`, `PREGUNTAS_TEST.md` y la guía `SESION1.md`, y el README cambia por el de la sesión. Ábrela y sigue desde «Preparar tu rama»: explica qué es una rama, propone un experimento para verlo y acompaña los ejercicios uno a uno.

Puedes leer la guía antes en GitHub: [guía de la sesión 1](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-1/SESION1.md).

Si `git status` muestra archivos modificados antes de cambiar de rama, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservarlos.

## Qué hay en esta rama

| Archivo | Para qué |
| :--- | :--- |
| [SETUP.md](SETUP.md) | Instalación paso a paso en Windows y macOS. |
| [SESION1_CHECKLIST.md](SESION1_CHECKLIST.md) | Lista para saber que estás preparado. |
| [ENUNCIADO.md](ENUNCIADO.md) | El caso FitLife: contexto, datos y la pregunta del taller. |
| [ACTUALIZAR.md](ACTUALIZAR.md) | Cómo actualizar el proyecto y conservar tu trabajo entre sesiones. |
| `test_app.py`, `check_setup.py` | La app y la comprobación que verifican tu instalación. |
| `data/` | Los dos CSV de FitLife. |
| `docente/`, `tests/` | Copia de referencia y pruebas automáticas del curso. No hace falta abrirlos. |
