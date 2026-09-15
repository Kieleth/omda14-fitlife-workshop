# OMDA14 · Verificación de la preparación y del paso 0

Fecha: 14 de septiembre de 2026.

## Instalación en main

La preparación publicada en `main` incluye los requisitos previos, `.venv`, dependencias fijadas, `pip check`, `check_setup.py` y la prueba interactiva `test_app.py`.

[GitHub Actions](https://github.com/Kieleth/omda14-fitlife-workshop/actions/runs/34928208238) comprobó el commit `033b2b0662f0c2b59c7821d52e9fda65775a34b5`: instalación desde cero y quince tests correctos en Windows, macOS y Linux. Los dos tests nuevos impiden reintroducir las instrucciones antiguas del entorno y el descarte de trabajo al actualizar.

## Paso 0 en codex/sesion-1

Los dieciocho tests locales pasaron con Python 3.13.3 en macOS ARM64. Incluyen:

- El error intencionado del import en el archivo que recibe el alumno.
- La app tras corregir solo ese import en una copia en memoria.
- Entrada, salida, texto vacío, contenido tratado como texto, trazas en la terminal y contadores.
- Cambio del título y de la transformación, y separación entre sesiones.
- La app sin API key y con conexiones de red bloqueadas durante las pruebas.
- La conservación exacta de los otros quince ejercicios, el extra y los dos CSV originales.

El paso 0 está adaptado. `material_base.json` conserva su hash original y el motivo del cambio. El original sigue disponible en el repositorio MDA13 y en `main` de OMDA14.

[GitHub Actions comprobó esta rama](https://github.com/Kieleth/omda14-fitlife-workshop/actions/runs/34928858698) en el commit `9f486a8155e77d1f70db44aa583875b7044eac27`: instalación desde cero y dieciocho tests correctos en Windows, macOS y Linux. El commit posterior que registra este resultado solo modifica este documento.

## Observado en un navegador real

Se arrancó una copia temporal de `paso_0.py` con el import corregido, usando el mismo entorno de verificación. El archivo publicado mantiene el reto inicial.

- Cambiar «Hola, FitLife» por «Hola, Madrid» mostró `HOLA, MADRID` y el contador de sesión pasó de 1 a 2.
- Pulsar el botón de repetir dejó el texto igual y aumentó el contador a 3. El contador local siguió en 1.
- Recargar la pestaña restauró el mensaje inicial y el contador de sesión a 1.
- Las líneas `[paso_0]` de la terminal coincidieron con cada entrada, salida y ejecución.

## Explicación HTML

`explicaciones/streamlit.html` contiene sus estilos y su JavaScript. No requiere nuevas dependencias, no carga recursos externos y no llama a una API. Sus referencias son enlaces que solo se visitan al pulsarlos.

Se ejecutó el JavaScript con una representación mínima del DOM para comprobar los cinco pasos, el momento en que cambia la salida, las entradas vacías, el texto con etiquetas, los botones de volver y reiniciar, Intro y el estado accesible del paso actual. Esta comprobación no es un renderizado de navegador.

La herramienta de navegador bloqueó la URL de archivo local. No se ha verificado visualmente el HTML en un navegador; no se afirma lo contrario. La prueba de apertura con doble clic en el portátil sigue pendiente de revisión.

## Límites

El HTML es una simulación didáctica, separada de la app. Los contadores y trazas de Streamlit proceden de la ejecución real de Python.

No se han probado llamadas a una API de LLM ni modelos locales. Los otros ejercicios no se han adaptado ni verificado con el SDK actual. Esta rama entrega el paso 0, no la sesión 1 completa.
