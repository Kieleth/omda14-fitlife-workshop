# Verificación de la instalación de OMDA14

Fecha: 14 de septiembre de 2026.

## Comprobado

Se creó un entorno vacío con Python 3.13.3 en macOS ARM64 y se ejecutó `pip install -r requirements.txt`. La instalación terminó correctamente; `pip check` no detectó incompatibilidades.

Los nueve chequeos del entorno pasaron. Los doce tests automáticos pasaron, incluidos los controles de Streamlit sin credenciales ni conexión de red, los errores de configuración y datos, y la conservación exacta de los 16 ejercicios, el extra y los dos CSV originales.

También se arrancó Streamlit y se comprobó la app en un navegador real:

- El control numérico pasó a 7 y el resultado a 49.
- El contador mostró nuevas ejecuciones del script.
- El plan cambió de `basic` a `premium` y los registros pasaron de 4.480 a 6.826; la tabla mostró filas del plan `premium`.

Los archivos se ejecutaron desde el nuevo repositorio, usando un entorno temporal de verificación fuera del repositorio. Ese entorno no se distribuye: cada alumno crea su propio `.venv` con las instrucciones de `SETUP.md`.

## Pendiente

El repositorio de GitHub todavía no se ha creado. Su visibilidad está pendiente de decisión. La guía de instalación necesita la dirección de clonación final antes de enviarla al alumnado.

Las instalaciones de Windows y Linux no se han ejecutado. La configuración de GitHub Actions incluye ambas y macOS, pero sus resultados solo se podrán comprobar después de publicar.

No se han probado llamadas a una API ni la ejecución de un modelo local. Los ejercicios originales se han conservado; eso no demuestra su compatibilidad completa con las versiones fijadas. Las ramas de las sesiones y las explicaciones HTML siguen pendientes de diseño y adaptación.
