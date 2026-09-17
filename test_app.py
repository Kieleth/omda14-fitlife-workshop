"""Abre con: python -m streamlit run test_app.py"""

import streamlit as st
from check_setup import ROOT, run_checks

st.set_page_config(page_title="OMDA14 | Comprueba tu instalación", page_icon="🔎")
st.title("OMDA14 · Comprueba tu instalación")
st.write("Primero comprobamos las herramientas. Después haces una pequeña prueba interactiva.")

checks = run_checks()
for check in checks:
    show = st.success if check.ok else st.error
    show(f"**{check.name}** · {check.detail}")

if not all(check.ok for check in checks):
    st.error("Instalación incompleta. Sigue SETUP.md para corregir los errores.")
    st.stop()

st.subheader("1. Mueve el control")
if "executions" not in st.session_state:
    st.session_state.executions = 0
st.session_state.executions += 1
number = st.slider("Elige un número", 0, 10, 3)
st.metric("Python calcula su cuadrado", number * number)
st.caption(f"Ejecuciones del script en esta sesión del navegador: {st.session_state.executions}.")
st.code("número = valor_del_control\nresultado = número * número", language="python")
st.write("Al mover el control, el navegador envía el nuevo valor al servidor de Streamlit. "
         "Python vuelve a ejecutar el script y Streamlit actualiza la pantalla. "
         "En este taller, ese servidor se ejecuta en tu portátil.")

st.subheader("2. Explora un archivo local")
import pandas as pd

members = pd.read_csv(ROOT / "data" / "fitlife_members.csv")
plan = st.selectbox("Plan de FitLife", sorted(members["plan"].unique()))
subset = members[members["plan"] == plan]
st.metric("Registros del plan seleccionado", len(subset))
st.caption("Cada registro es un socio en un mes. Este número no es el de socios únicos.")
st.dataframe(subset.head(5), hide_index=True)

st.info("Estas operaciones las ejecuta Python con los datos de tu portátil. "
        "Esta app no llama a un LLM, no necesita clave y no prueba el acceso a una API.")
st.success("Si el cuadrado y la tabla cambian al tocar los controles, has completado la comprobación local.")
