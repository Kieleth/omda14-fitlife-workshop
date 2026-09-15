# OMDA14 · Analítica conversacional con GenAI

Cuatro sesiones de 2 h 30 min. Construiremos una aplicación para explorar los datos de FitLife con Python, Streamlit y un modelo de lenguaje. Mantendremos el caso y el contenido de MDA13, añadiendo ejercicios y explicaciones visuales que permitan ver qué ocurre en cada interacción.

## Empieza aquí: prepara tu portátil

1. Sigue [SETUP.md](SETUP.md). Incluye Windows y macOS.
2. Ejecuta el chequeo del entorno y abre `test_app.py` con Streamlit.
3. Mueve el control numérico y cambia el plan de FitLife. Comprueba que cambian el resultado y la tabla.
4. Lee [el caso FitLife](ENUNCIADO.md).

Para esta preparación no necesitas una API key ni descargar un modelo. La comprobación ejecuta Python sobre archivos locales. El acceso al LLM se configurará por separado.

La rama `main` es el punto de entrada para instalar y comprobar el entorno. Esta rama, `codex/sesion-1`, contiene la primera práctica. No tienes que completar los ejercicios antes de clase.

## Primera práctica: del navegador a Python

Sigue [SESION1_PASO0.md](SESION1_PASO0.md): crea tu rama, corrige el import de `paso_0.py`, prueba las entradas y observa las ejecuciones. La explicación [explicaciones/streamlit.html](explicaciones/streamlit.html) se abre directamente en el navegador desde tu copia local.

La app del ejercicio empieza con un error intencionado. La app de instalación `test_app.py` debe funcionar antes de iniciar la práctica.

## Qué encontrarás

| Archivo | Para qué sirve |
| :--- | :--- |
| [SETUP.md](SETUP.md) | Instalación y solución de problemas |
| `requirements.txt` | Versiones fijadas de las dependencias |
| `check_setup.py` | Diagnóstico desde la terminal |
| `test_app.py` | Comprobación interactiva en el navegador |
| `data/` | Los dos CSV originales de FitLife |
| [ENUNCIADO.md](ENUNCIADO.md) | El caso de negocio |
| [CONTENIDO_MDA13.md](CONTENIDO_MDA13.md) | Índice del contenido original, pendiente de adaptar por sesión |

## Sesiones en preparación

El resto del contenido original está conservado en `exercises/`, `exercises2/`, `exercises3/`, `extras/` y las guías de repaso. Algunos ejercicios tienen errores y huecos intencionados. No se usan para verificar la instalación.

`paso_0.py` está adaptado para OMDA14 en esta rama. Los demás ejercicios y los dos CSV mantienen los archivos originales de MDA13; `material_base.json` registra qué se conserva y qué se adapta. Los siguientes pasos de la sesión y las otras tres ramas siguen pendientes. La propuesta docente está en [PLAN_DOCENTE.md](PLAN_DOCENTE.md).
