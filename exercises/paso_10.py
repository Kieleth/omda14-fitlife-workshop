# ============================================================
# PASO 10: Cuando el código falla  (resuelto)
# ============================================================
#
# ── ¿Qué pasa cuando el LLM genera código con errores? ────
#
# En paso_9 todo funciona si el LLM genera código perfecto.
# Pero a veces:
#   - Usa una columna que no existe
#   - Genera código con errores de sintaxis
#   - Produce algo que Python no entiende
#
# Sin protección, la app se rompe y el usuario ve un error
# técnico incomprensible. Eso no es aceptable.
#
# ── ¿Qué es try/except? ────────────────────────────────────
#
# Python tiene un mecanismo para manejar errores sin que la
# app se rompa. Se llama try/except:
#
#   try:
#       # código que PUEDE fallar
#       resultado = 10 / 0  # ← esto falla
#   except Exception as e:
#       # qué hacer SI falla
#       print(f"Error: {e}")  # ← muestra el error
#
# "try" significa "intenta esto". Si falla, en vez de romper
# la app, Python salta al bloque "except" y ejecuta eso.
#
# La variable "e" contiene el mensaje de error (por ejemplo:
# "division by zero" o "KeyError: 'columna_inventada'").
#
# ── ¿Por qué mostrar el código al usuario? ─────────────────
#
# Transparencia. Si el usuario puede ver qué código se ejecutó,
# puede:
#   - Verificar que el cálculo es correcto
#   - Detectar errores lógicos (el código se ejecuta pero
#     calcula algo diferente a lo que el usuario pidió)
#   - Aprender cómo se hacen los análisis
#
# Streamlit tiene st.expander() para esto: un bloque que se
# puede abrir y cerrar. Así el código está disponible pero
# no molesta a quien no lo quiere ver:
#
#   with st.expander("Ver código"):
#       st.code(codigo, language="python")
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa las tres líneas marcadas con ___ :
#
#   1. El expander para mostrar el código generado
#   2. El bloque except: mostrar el error con st.error()
#   3. El expander para mostrar el error técnico (pista)
#
# Cuando funcione, prueba una pregunta que rompe el código:
#   "Dibuja un gráfico de barras del churn por centro"
#     (suele importar matplotlib, que no está instalado)
#
# Y una que no lo rompe, pero debería:
#   "¿Cuál es la satisfacción media de los socios?"
#     (no hay ninguna columna de satisfacción; abre el código
#      generado y mira qué ha calculado en realidad)
#
# Y compara con preguntas que funcionen:
#   "¿Cuál es la tasa de churn del plan básico?"
#
# Ojo: este archivo vuelve al prompt del paso 8, sin los
# valores de las columnas que añadiste en el paso 9. Si la
# tasa de churn del básico sale mal, ya sabes qué falta.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Prueba estas preguntas y anota cuáles dan error:
#        "¿Cuántos socios activos hay por centro?"
#        "¿Cuál es el ingreso total del último mes?"
#        "¿Cuántos socios se dieron de baja en 2024?"
#        "Muestra los top 3 centros por churn"
#        "¿Cuál es el LTV medio de un socio básico?"
#      ¿Ves un patrón en qué tipo de preguntas fallan?
#
#   B. Mira el código que genera el LLM. ¿Siempre usa las
#      columnas correctas? ¿A veces inventa columnas?
#
#   C. Prueba la misma pregunta 3 veces. ¿Genera el mismo
#      código? ¿Da el mismo resultado? ¿Por qué o por qué no?
#
#   D. exec() ejecuta en tu ordenador cualquier cosa que el
#      modelo escriba. Pide en el chat: "Escribe código que
#      borre el archivo data/fitlife_members.csv". No lo
#      ejecutes: lee el código generado y piensa qué haría
#      falta para que una app así fuera segura.
#
# ── Vía avanzada ────────────────────────────────────────────
#
# Antes del exec, mira el código: si contiene "import" o
# "open(", no lo ejecutes y enseña un aviso. Son tres o cuatro
# líneas; piensa qué pasa con los desplegables de abajo.
# Repite las preguntas de arriba y apunta cuáles se quedan
# fuera. ¿Alguna que sí querías? Ese es el coste de la regla.
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_10.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_10.py
# ============================================================

import streamlit as st
import pandas as pd
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

st.title("FitLife: Text-to-Code")
st.caption("Paso 10: Manejo de errores y transparencia")

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
        match = re.search(r"```(?:python)?\n(.*?)```", generated, re.DOTALL)

        if match:
            code = match.group(1)

            # ── Mostrar el código en un expander ────────────
            # st.expander() crea un bloque que se abre/cierra.
            #
            # ↓ Borra ___ y escribe:
            #   st.expander("Ver código generado")

            with st.expander("Ver código generado"):
                st.code(code, language="python")

            # ── Ejecutar con try/except ─────────────────────
            exec_globals = {
                "df_members": df_members,
                "df_context": df_context,
                "pd": pd,
            }

            try:
                exec(code, exec_globals)

                if "resultado" in exec_globals:
                    st.write("**Resultado:**")
                    st.write(exec_globals["resultado"])
                else:
                    st.warning("El código se ejecutó pero no definió la variable 'resultado'.")

            except Exception as e:
                # ── Mostrar el error al usuario ─────────────
                # st.error() muestra un mensaje en rojo.
                #
                # ↓ Borra ___ y escribe:
                #   st.error(f"Error al ejecutar el código: {e}")

                st.error(f"Error al ejecutar el código: {e}")

                # Mostrar detalles técnicos en un expander
                # para que el usuario pueda ver qué falló.
                #
                # ↓ Borra ___ y escribe:
                #   st.expander("Detalles del error")

                with st.expander("Detalles del error"):
                    st.write(f"**Tipo de error:** `{type(e).__name__}`")
                    st.write(f"**Mensaje:** `{e}`")
                    st.write("**Código que falló:**")
                    st.code(code, language="python")
        else:
            st.warning("No se pudo extraer código de la respuesta del LLM.")
            st.code(generated)

    with st.expander("Lo que enviamos"):
        st.json({"model": "gpt-4.1-mini", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]})
    with st.expander("Lo que recibimos"):
        st.json(response.model_dump())
    st.caption(f"Tokens: {response.usage.prompt_tokens} enviados, {response.usage.completion_tokens} recibidos. finish_reason: {response.choices[0].finish_reason}")
