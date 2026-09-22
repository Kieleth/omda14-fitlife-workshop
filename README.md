# OMDA14 · Analítica conversacional con IA

Vas a construir, paso a paso, una aplicación para explorar los datos de FitLife y hacer preguntas a un modelo de lenguaje: añadirás código, probarás lo que cambia y explicarás qué has observado. Esta rama, `main`, contiene solo la preparación. Los ejercicios de cada sesión se publican en su propia rama y se descargan al empezar la sesión.

## Antes de empezar

1. Sigue [la guía de instalación](SETUP.md) de tu sistema operativo.
2. Comprueba que la app de prueba abre y responde a sus controles.
3. Lee [el caso FitLife](ENUNCIADO.md).

**Cuando termines la comprobación, ya estás preparado.** No necesitas una clave de acceso a un modelo para esta preparación; la clave del curso se usa a partir del paso 5 de la sesión 1.

## Cuando empiece la sesión 3

Los ejercicios de la sesión 3 y su guía están en la rama `clase/sesion-3`. Esa rama trae además los pasos 0 a 11 de las sesiones 1 y 2 en su versión terminada, para repasar y comparar.

Si hiciste la sesión 2 en tu rama `alumno/sesion-2`, sigue la sección «Preparar tu rama» de la [guía de la sesión 3](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-3/SESION3.md): primero guardas tu trabajo con un commit y después creas `alumno/sesion-3`. Si te quedaste en la sesión 1, la misma sección sirve desde `alumno/sesion-1`.

Si empiezas hoy, abre la carpeta del proyecto en VS Code, abre **Terminal > New Terminal** y ejecuta:

```text
git fetch origin
git switch -c alumno/sesion-3 origin/clase/sesion-3
```

`fetch` descarga lo publicado para la clase. `switch -c` crea tu rama, `alumno/sesion-3`, a partir de la rama de la clase; en ella quedan tus cambios, en tu ordenador. Al cambiar de rama aparecen en la carpeta `exercises/`, `explicaciones/`, `PREGUNTAS_TEST.md` y las guías de las sesiones, y el README cambia por el de la sesión.

Si `git status` muestra archivos modificados antes de cambiar de rama, [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservarlos.

## Las sesiones anteriores por tu cuenta

La sesión 2 con sus huecos sigue en la rama `clase/sesion-2`, con su [guía](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-2/SESION2.md). Para hacerla desde cero, `git switch -c alumno/sesion-2 origin/clase/sesion-2` después de `git fetch origin`.

Los ejercicios de la sesión 1 con sus huecos siguen en la rama `clase/sesion-1`, con su [guía](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-1/SESION1.md). Para hacerla desde cero:

```text
git fetch origin
git switch -c alumno/sesion-1 origin/clase/sesion-1
```

La guía explica qué es una rama, propone un experimento para verlo y acompaña los ejercicios uno a uno.

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
