# ============================================================
# PASO 8: Haz que escriba código  (resuelto)
# ============================================================
#
# ── ¿Qué aprendimos en la sesión 1? ────────────────────────
#
# El LLM entiende las preguntas perfectamente, pero no puede
# calcular sobre 16.334 filas. Cuando le pides "¿cuál es la
# tasa de churn del plan básico?", se inventa un número.
#
# ── La idea clave de la sesión 2 ────────────────────────────
#
# ¿Y si en vez de pedirle LA RESPUESTA, le pedimos que
# escriba EL CÓDIGO para calcularla?
#
#   Antes (sesión 1):
#     Usuario: "¿Cuál es la tasa de churn?"
#     LLM:     "La tasa de churn es del 12.3%" ← inventado
#
#   Ahora (sesión 2):
#     Usuario: "¿Cuál es la tasa de churn?"
#     LLM:     "churned = df[df['status']=='churned']
#               tasa = len(churned)/len(df)*100"  ← código real
#     Python:  ejecuta el código → 2.52%  ← resultado real
#
# Esto se llama "text-to-code": el LLM traduce lenguaje
# natural a código Python. Python calcula. El número es real.
#
# ── El cambio está en el prompt ─────────────────────────────
#
# En paso_6, el prompt del sistema decía:
#   "Eres un analista de datos. Responde a las preguntas..."
#
# Ahora le vamos a decir:
#   "Genera solo código Python que responda a la pregunta.
#    No expliques nada. Solo el código."
#
# Eso es todo. El mismo LLM, la misma API, pero con una
# instrucción diferente.
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa la línea marcada con ___ en el prompt del sistema.
# Necesitas decirle al LLM que genere código Python, no texto.
#
# Antes de rellenarlo, un experimento con la misma pregunta,
# "¿Cuántos registros tiene el dataset?", tres veces: con el
# hueco tal cual; con "Responde con texto, en una frase, sin
# escribir código." en el hueco; y con la instrucción buena.
# Apunta qué devuelve cada vez. SESION2.md explica por qué.
#
# Cuando funcione, prueba preguntas como:
#   "¿Cuántos registros tiene el dataset?"
#   "¿Cuántos socios de cada plan hay?"
#   "¿Cuál es la tasa de churn del plan básico?"
#
# Verás que el LLM responde con CÓDIGO en vez de con texto.
# En el siguiente paso aprenderemos a ejecutar ese código.
#
# ── Mira lo que viaja ───────────────────────────────────────
#
# Los dos desplegables de la sesión 1 ya están al final del
# archivo. Ábrelos después de cada pregunta:
#
#   "Lo que enviamos": el content del system ya no lleva filas
#   de la tabla, solo los nombres de las columnas y unas reglas.
#   "Lo que recibimos": el código está dentro de content, entre
#   ```python y ```. Es texto. Nada se ha ejecutado todavía.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Prueba la misma pregunta que en paso_6:
#        "¿Cuál es la tasa de churn del plan básico?"
#      ¿El código que genera tiene sentido? ¿Lo entiendes?
#      Fíjate en el valor con el que filtra el plan. Apúntalo:
#      lo vas a necesitar en el paso 9.
#
#   B. Prueba una pregunta más compleja:
#        "¿Cuál es el margen medio por plan?"
#      ¿Genera código correcto? ¿Usa las columnas correctas?
#
#   C. Prueba en inglés y en español. ¿Genera mejor código
#      con preguntas en un idioma u otro?
#
#   D. Pregunta algo que NO se puede responder con los datos:
#        "¿Cuál es la satisfacción media de los socios?"
#      ¿Qué hace? ¿Genera código que falla? ¿Inventa una
#      columna que no existe?
#
# ── Vía avanzada ────────────────────────────────────────────
#
# Mira los prompt_tokens del pie: el del paso 6 pesaba 715.
# ¿Cuántos pesa este? Luego añade temperature=0 a la llamada,
# repite la misma pregunta tres veces y compara el código
# línea por línea. ¿Sale igual? Quita temperature=0 y
# repítelo. Apunta las dos respuestas en mis_notas.md.
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_8.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_8.py
# ============================================================

import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

st.title("FitLife: Text-to-Code")
st.caption("Paso 8: El LLM genera código en vez de responder")

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

        # ── PROMPT DEL SISTEMA ──────────────────────────────
        # La primera línea dice qué queremos; las reglas de abajo
        # también. Haz antes el experimento de la cabecera.
        # Borra ___ (solo el hueco, las comillas se quedan) y
        # escribe la instrucción para que el LLM genere código
        # Python en vez de responder con texto.
        #
        # Pista: necesitas decirle algo como
        #   Genera solo código Python/pandas que responda a la pregunta del usuario.
        #   o "Escribe únicamente código Python..."

        system_prompt = f"""Genera solo código Python/pandas que responda a la pregunta del usuario.

Tienes acceso a dos DataFrames ya cargados:

1. df_members: datos de socios ({len(df_members)} filas)
   Columnas: {list(df_members.columns)}

2. df_context: contexto mensual ({len(df_context)} filas)
   Columnas: {list(df_context.columns)}

Reglas:
- Usa pandas para las operaciones.
- El código debe terminar con: resultado = <lo que calcules>
- NO uses print(). Solo asigna el resultado final a la variable "resultado".
- NO incluyas import ni read_csv: los datos ya están cargados.
- Devuelve SOLO el bloque de código, sin explicaciones antes ni después.
- Envuelve el código en triple backtick python."""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        generated = response.choices[0].message.content
        st.write("**Código generado por el LLM:**")
        st.code(generated, language="python")
        st.write("👆 De momento solo lo muestra. En el paso 9 lo ejecutaremos.")

    with st.expander("Lo que enviamos"):
        st.json({"model": "gpt-4.1-mini", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]})
    with st.expander("Lo que recibimos"):
        st.json(response.model_dump())
    st.caption(f"Tokens: {response.usage.prompt_tokens} enviados, {response.usage.completion_tokens} recibidos. finish_reason: {response.choices[0].finish_reason}")
