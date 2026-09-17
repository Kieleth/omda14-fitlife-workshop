# ============================================================
# PASO 2: Carga datos
# ============================================================
#
# ── ¿Qué es pandas? ────────────────────────────────────────
#
# pandas es una librería de Python para trabajar con tablas de
# datos. Piensa en Excel, pero en código: filas, columnas, y
# funciones para filtrar, agrupar y calcular.
#
# La función clave:
#
#   pd.read_csv("ruta/al/archivo.csv")
#
# Carga un archivo CSV y lo convierte en un DataFrame, una
# tabla con filas y columnas que puedes explorar y manipular.
#
# ── ¿Qué es una ruta de archivo? ───────────────────────────
#
# Una ruta es la dirección de un archivo, como una dirección
# postal. Ejecuta el ejercicio desde la raíz del proyecto,
# con el comando de vuestro sistema al final de estas
# instrucciones. Las rutas son relativas a esa raíz.
#
# Estructura del proyecto (mira dónde están los CSV):
#
#   omda14-fitlife-workshop/        ← raíz (aquí se ejecuta)
#   ├── exercises/
#   │   ├── paso_0.py
#   │   ├── paso_2.py              ← estás aquí
#   │   └── ...
#   ├── data/
#   │   ├── fitlife_members.csv    ← este archivo
#   │   └── fitlife_context.csv
#   └── ...
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Esta app intenta cargar datos pero falla. Ejecútala, lee el
# error y arregla la ruta del archivo.
#
# Pista: el archivo no está suelto en la raíz. ¿En qué
# carpeta está?
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Prueba a cambiar df por df.head(10) en la última línea:
#        st.dataframe(df.head(10))
#      ¿Qué cambia? head(N) muestra solo las primeras N filas.
#
#   B. Prueba:
#        st.write(df.describe())
#      Esto muestra estadísticas básicas de cada columna
#      numérica (media, mínimo, máximo...). ¿Qué veis?
#
#   C. Prueba:
#        st.write(df["plan"].value_counts())
#      Esto cuenta cuántas filas hay de cada plan. ¿Cuál es
#      el plan más popular?
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_2.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_2.py
# ============================================================

import streamlit as st
import pandas as pd

st.title("FitLife Dashboard")

df = pd.read_csv("fitlife_members.csv")

st.write(f"El dataset tiene **{len(df)}** filas y **{len(df.columns)}** columnas.")
st.dataframe(df)
