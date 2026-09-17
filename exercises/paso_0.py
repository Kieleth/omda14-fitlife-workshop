# PASO 0: arranca la app
#
# Streamlit es una librería de Python. Funciones como st.title
# y st.write muestran elementos en el navegador.
#
# Tu reto: hacer que esta app funcione. Tiene un error.
#
# 1. Abre la terminal en la carpeta omda14-fitlife-workshop.
#    Usa el entorno .venv creado siguiendo SETUP.md.
# 2. Ejecuta solo el comando de tu sistema:
#    Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_0.py
#    macOS:   .venv/bin/python -m streamlit run exercises/paso_0.py
# 3. Abre la dirección URL que aparece en la terminal.
#    Lee el error en el navegador o la terminal. ¿Qué módulo
#    intenta importar? Compara su nombre con Streamlit.
# 4. Corrige la errata y guarda con Ctrl+S o Cmd+S.
#    Si aparece Rerun, púlsalo. Always rerun permite que la
#    app se vuelva a ejecutar al guardar los siguientes cambios.
#
# Cuando veas el título y el mensaje, has completado el paso.
#
# Si has terminado antes:
# A. Cambia el texto del título o de st.write. Antes de guardar,
#    predice qué elemento cambiará. Guarda y compruébalo.
# B. Añade al final: st.balloons()
#    Guarda. Después sustituye esa línea por st.snow().
# C. Añade al final: st.slider("Tu edad", 0, 100, 25)
#    Guarda y mueve el control. ¿Qué has añadido a la página?
#
# Guía de la sesión y Git: SESION1.md.
# Siguiente: exercises/paso_1.py.

import streamlt as st

st.title("Hola Mundo")
st.write("Si ves esto en el navegador, tu primera app web funciona.")
