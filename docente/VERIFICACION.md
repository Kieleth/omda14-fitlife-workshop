# Verificación de la corrección de alcance

Se conservan el código ejecutable de los pasos 0 a 7 y los 19 hashes del material base. Los pasos 1 a 7 vuelven a estar disponibles en exercises/, con comentarios de instalación actualizados. requirements.txt, check_setup.py y test_app.py no cambian.

La rama de sesión pasó 20 tests locales en macOS con Python 3.13.3: instalación, preservación del material, equivalencia del código y orden de ejercicios, error de import intencionado, corrección, cambios de texto y ampliaciones opcionales reales de la guía. Las pruebas del paso 0 bloquean las conexiones de red y no utilizan credenciales. No ejecutan los pasos posteriores contra un proveedor de LLM.

La lógica del HTML pasó una prueba con una representación mínima del DOM: editar, guardar, ejecutar, mostrar; títulos vacíos, comillas y texto literal; anterior y reinicio. Es una ilustración de la edición del título, sin transformaciones de mensajes. No es una prueba de renderizado; la comprobación visual sigue pendiente por la restricción de la herramienta sobre URLs de archivos locales.

La comprobación de esta corrección en GitHub Actions está pendiente de finalizar.
