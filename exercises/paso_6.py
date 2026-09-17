# ============================================================
# PASO 6: Pregúntale sobre los datos
# ============================================================
#
# ── ¿Qué pasa cuando un LLM habla de datos que no ha visto?
#
# En paso_5 el LLM respondía bien a preguntas generales:
# historia, código, cuentas cortas. Pero esos son temas que
# estaban en su entrenamiento (todo internet).
#
# FitLife es un caso inventado. El LLM nunca ha visto estos
# datos. Si le preguntas "¿cuántos socios tiene FitLife?"
# sin darle ningún contexto, se inventará un número.
#
# En este paso le pasamos algo de contexto: una muestra de
# 5 filas y los nombres de las columnas. Así "sabe" de qué
# estamos hablando. ¿Es suficiente?
#
# ── Tu reto ─────────────────────────────────────────────────
#
# ESTE PASO NO TIENE NADA ROTO. Funciona tal cual.
#
# Tu misión es de detective: prueba estas 5 preguntas y anota
# para cada una si la respuesta es correcta o inventada.
#
#   1. ¿Cuántos registros tiene el dataset de socios?
#   2. ¿Qué planes ofrece FitLife?
#   3. ¿Cuál es el centro con más socios?
#   4. ¿Cuál es la tasa de churn del plan básico?
#   5. ¿Debería FitLife bajar el precio del plan básico?
#
# ── Anota tus resultados ────────────────────────────────────
#
#   Pregunta 1 (registros):  ¿Correcto?       ¿Qué dijo?
#   Pregunta 2 (planes):     ¿Correcto?       ¿Qué dijo?
#   Pregunta 3 (centro):     ¿Correcto?       ¿Qué dijo?
#   Pregunta 4 (churn):      ¿Correcto?       ¿Qué dijo?
#   Pregunta 5 (precio):     ¿Correcto?       ¿Qué dijo?
#
# Pista: para comprobar las respuestas con los datos de verdad,
# añade al final de paso_3 y ejecútalo:
#   st.write(df_members["center"].value_counts())
#   st.write(df_members[df_members["plan"] == "basic"]["status"].value_counts())
# La primera cuenta filas por centro. La segunda cruza plan y
# estado: churned entre el total es la tasa de churn del básico.
# Las 5 preguntas de arriba son para hoy. Las 12 de
# PREGUNTAS_TEST.md se repiten en todas las sesiones para
# comparar cómo mejora el sistema.
#
# Cuando termines, comparte tus resultados en el chat de clase.
#
# ── Pregunta para pensar ────────────────────────────────────
#
# Fíjate en el código de abajo, en la variable "context".
# ¿Qué datos le estamos pasando realmente al LLM?
# ¿Cuántas filas ve de 16.334? ¿Es suficiente para calcular
# una tasa de churn o decidir si bajar precios?
#
# ── Mira exactamente lo que ve el modelo ───────────────────
#
# Como en el paso 5: copia estas seis
# líneas al final del archivo, quita el "# " del principio y
# deja 4 espacios delante de with.
#
#     with st.expander("Lo que enviamos"):
#         st.json({"model": "gpt-4.1-mini", "messages": [{"role": "system", "content": context}, {"role": "user", "content": prompt}]})
#         st.caption(f"El contexto tiene {len(context)} caracteres. Es una de las dos entradas de messages.")
#     with st.expander("Lo que recibimos"):
#         st.json(response.model_dump())
#     st.caption(f"Tokens: {response.usage.prompt_tokens} enviados, {response.usage.completion_tokens} recibidos. finish_reason: {response.choices[0].finish_reason}")
#
# Ahora messages tiene dos entradas. La de rol "system" es el
# texto de la variable context: instrucciones y datos pegados
# como texto. La de rol "user" es tu pregunta. El modelo no
# recibe el CSV ni la conversación anterior: recibe exactamente
# este JSON, y nada más. finish_reason dice por qué paró de
# escribir: "stop" es el final normal; "length" es que se
# quedó sin espacio.
#
# Busca en el "content" del system las 5 filas. ¿De cuántos
# socios distintos son? ¿Qué planes aparecen? ¿Qué centros?
# Vuelve a la pregunta 3 con eso delante.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Haz la pregunta 4 (tasa de churn) tres veces seguidas.
#      Si en vez de un número te explica el procedimiento,
#      pide: "Dame solo el porcentaje, sin explicar el
#      procedimiento". ¿Da el mismo número cada vez? Si cambia,
#      no lo está calculando: se lo está inventando. Compáralo
#      con el recuento que hiciste en paso_3. Coincida o no, un
#      número que no sale de contar las filas es inventado. En
#      paso_7 A verás qué cambia con temperature=0.
#
#   B. Prueba una pregunta que SÍ pueda responder bien:
#        "Describe las columnas del dataset de socios"
#      ¿Por qué esta sí funciona y las numéricas no?
#
#   C. Prueba a preguntarle algo que no está en los datos:
#        "¿Cuál es el NPS de FitLife?"
#      ¿Dice que no lo sabe o se inventa un número?
#
#   D. Mira la línea 143: head(). Eso muestra solo 5 filas.
#      ¿Qué pasaría si cambias head() por head(50)?
#      ¿Mejorarían las respuestas? ¿Y head(1000)?
#      ¿Dónde está el límite? (No hace falta probarlo:
#      solo pensadlo. Lo exploraremos en el paso 7.)
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_6.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_6.py
# ============================================================

import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

st.title("FitLife Dashboard")

df_members = pd.read_csv("data/fitlife_members.csv")
df_context = pd.read_csv("data/fitlife_context.csv")

st.subheader("Datos cargados")
st.write(f"Socios: **{len(df_members)}** registros | Contexto: **{len(df_context)}** meses")

st.divider()

prompt = st.chat_input("Pregunta sobre los datos de FitLife...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        context = f"""Eres un analista de datos. Tienes acceso a datos de FitLife,
una red de gimnasios.

Dataset 1 - Socios (muestra de 5 filas de {len(df_members)} totales):
{df_members.head().to_string()}

Columnas: {list(df_members.columns)}

Dataset 2 - Contexto mensual (muestra de 5 filas de {len(df_context)} totales):
{df_context.head().to_string()}

Columnas: {list(df_context.columns)}"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ]
        )
        st.write(response.choices[0].message.content)
