# OMDA14 · Analítica conversacional con IA

Vas a construir, paso a paso, una aplicación para explorar los datos de FitLife y hacer preguntas a un modelo de lenguaje: añadirás código, probarás lo que cambia y explicarás qué has observado. Esta rama, `main`, contiene solo la preparación. Los ejercicios de cada sesión se publican en su propia rama y se descargan al empezar la sesión.

## Antes de empezar

1. Sigue [la guía de instalación](SETUP.md) de tu sistema operativo.
2. Comprueba que la app de prueba abre y responde a sus controles.
3. Lee [el caso FitLife](ENUNCIADO.md).

**Cuando termines la comprobación, ya estás preparado.** No necesitas una clave de acceso a un modelo para esta preparación; la clave del curso se usa a partir del paso 5 de la sesión 1.

## Sesión 4

Los ejercicios y la [guía de sesión 4](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-4/SESION4.md) están en `clase/sesion-4`. Esa rama trae los pasos 0 a 15 resueltos, con el historial corregido, y añade recuperación de conversaciones, herramientas, comparación de modelos, revisión con evidencia y una demo compartida.

Si ya tienes una rama de alumno, sigue «Preparar tu rama» en esa guía: primero guarda tus cambios con un commit y después crea `alumno/sesion-4`. Tu solución anterior permanece en su rama. [ACTUALIZAR.md](ACTUALIZAR.md) explica cómo conservar archivos y cambios antes de cambiar de rama.

Si empiezas hoy, completa la instalación, abre la carpeta del proyecto en VS Code y abre **Terminal > New Terminal**. Comprueba `git status`; cuando no queden cambios por guardar:

```text
git fetch origin
git switch -c alumno/sesion-4 origin/clase/sesion-4
```

`fetch` descarga lo publicado. `switch -c` crea tu rama de trabajo desde la rama de la clase. Al cambiar, aparecen los ejercicios y las guías en la carpeta, y cambia este README. Si `alumno/sesion-4` ya existe, vuelve con `git switch alumno/sesion-4`.

## Las sesiones anteriores por tu cuenta

La sesión 3 conserva sus ejercicios en `clase/sesion-3`, con su [guía](https://github.com/Kieleth/omda14-fitlife-workshop/blob/clase/sesion-3/SESION3.md). Para empezar esa práctica desde cero, guarda tus cambios, ejecuta `git fetch origin` y después `git switch -c alumno/sesion-3 origin/clase/sesion-3`. La guía de sesión 4 explica la corrección del historial al continuar.

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
