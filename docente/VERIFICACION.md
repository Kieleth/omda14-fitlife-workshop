# Verificación de esta revisión

Los ejercicios y guías de referencia se conservan en docente/referencia. Los 19 hashes de ejercicios, extra y datos originales se comprueban desde docente/material_base.json. Las dependencias no cambian.

Los tests comprueban también que las entradas del alumno no contienen referencias editoriales ni actividades sin adaptar. La rama de la sesión añade pruebas de cada etapa de construcción.

Main pasó sus 16 tests y la instalación desde cero en Windows, macOS y Linux: [ejecución 34929628988](https://github.com/Kieleth/omda14-fitlife-workshop/actions/runs/34929628988), commit e22d23d09b67e5bcff00c9aae7d0e913eeca5a41.

La rama de sesión pasó 19 tests locales en macOS con Python 3.13.3. Incluyen la comprobación del starter mínimo y la ejecución acumulativa de los bloques reales de la guía. El error de import se comprueba como intencionado; cada etapa posterior se ejecuta sin credenciales y con conexiones de red bloqueadas. La comprobación de esta rama en GitHub Actions está pendiente de finalizar.

La lógica del HTML se ejecutó con una representación mínima del DOM: pasos, entrada vacía, texto literal, anterior, reinicio e Intro pasaron. No es una prueba de renderizado. El HTML es una ilustración sin Python ni llamadas a un LLM; su verificación visual sigue pendiente por la restricción de la herramienta sobre URLs de archivos locales.
