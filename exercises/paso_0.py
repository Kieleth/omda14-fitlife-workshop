# OMDA14 · Paso 0: del navegador a Python y de vuelta
#
# Empieza por SESION1_PASO0.md. Este import tiene el error de MDA13.
# Léelo y corrige SOLO el nombre del módulo. No instales paquetes nuevos.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_0.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_0.py
#
# Después: predice qué cambiará, escribe un mensaje y pulsa Intro.
# Compara la pantalla, los dos contadores y la terminal.

import streamlt as st

st.set_page_config(page_title="OMDA14 · Paso 0", page_icon="🔎")

# RETO 2: cambia este título y guarda el archivo.
titulo = "Hola, FitLife"

# Esta variable vuelve a empezar en cada ejecución.
contador_local = 0
contador_local += 1

# Este valor se conserva entre ejecuciones de la misma sesión.
if "ejecuciones" not in st.session_state:
    st.session_state["ejecuciones"] = 0
st.session_state["ejecuciones"] += 1
ejecucion = st.session_state["ejecuciones"]

st.title(titulo)
st.caption("Paso 0 · Tu navegador habla con un programa de Python en tu portátil.")
st.write("Antes de tocar nada, predice qué cambiará en la pantalla y en la terminal.")

mensaje = st.text_input("Mensaje", "Hola, FitLife")
st.button("Volver a ejecutar sin cambiar el mensaje")

# RETO 3: cambia upper() por lower(), guarda y compara.
resultado = mensaje.upper()

st.subheader("1. Valor que recibe Python")
st.code(repr(mensaje), language="python")
st.subheader("2. Resultado que muestra el navegador")
st.code(repr(resultado), language="python")
st.caption("Las comillas representan una cadena de texto. '' es una cadena vacía.")

local, sesion = st.columns(2)
local.metric("Contador local", contador_local)
sesion.metric("Ejecuciones en esta sesión", ejecucion)

# print escribe en la terminal; st.write y st.code escriben en la página.
print(f"[paso_0] ejecución={ejecucion} | local={contador_local} | "
      f"entrada={mensaje!r} | salida={resultado!r}", flush=True)

st.write("El contador local empieza en 0 y sube a 1 en cada ejecución. "
         "El otro se guarda en st.session_state y aumenta entre ejecuciones. "
         "Recargar la pestaña inicia una sesión nueva y reinicia ese estado.")
st.info("Aquí Python transforma el texto con la regla que has escrito. "
        "No hay un LLM ni una llamada a una API. Streamlit organiza la interacción.")
st.caption("Abre explicaciones/streamlit.html para recorrer el proceso paso a paso. "
           "Es una simulación; la pantalla y la terminal de esta app muestran la ejecución real.")
