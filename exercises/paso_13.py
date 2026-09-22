# ============================================================
# PASO 13: El analista explica
# ============================================================
#
# ── ¿Qué tenemos hasta ahora? ──────────────────────────────
#
# Un chat con memoria que genera código, lo ejecuta, y muestra
# el resultado. Si preguntas "¿Cuál es la tasa de churn del
# plan básico?" ves algo como:
#
#   6.852678571428572
#
# (En la sesión 2 salía 0.0685. Este prompt lleva la regla
# "tasa de churn: churned / total * 100", y por eso ahora
# sale en porcentaje.)
#
# Es correcto. Pero no es muy útil. Un analista humano no te
# diría solo "6.85". Te diría:
#
#   "La tasa de churn del plan básico es del 6,85 %, más de
#    seis veces la del plan premium (1,07 %). Esto sugiere que
#    los socios del plan más económico son más sensibles al
#    precio del competidor low-cost."
#
# Fíjate en que ese analista cita el premium, un número que
# no está en el resultado: lo trae de otro sitio. El modelo
# también lo hará. La pregunta es de dónde lo saca.
#
# ── La idea: dos pasadas ───────────────────────────────────
#
# Vamos a hacer DOS llamadas al LLM:
#
#   Pasada 1: "Genera código para calcular X"
#             → código → exec() → resultado numérico
#
#   Pasada 2: "El usuario preguntó X. El resultado calculado
#              es Y. Explica qué significa en el contexto del
#              negocio de FitLife."
#             → interpretación en lenguaje natural
#
# La primera pasada es la calculadora (ya la tenemos).
# La segunda es el analista (lo nuevo de este paso).
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa las dos líneas marcadas con ___ :
#
#   1. El prompt de interpretación (qué le pedimos al LLM)
#   2. La llamada a la API para obtener la interpretación
#
# Antes de rellenar nada, arranca y pregunta. La pasada 1
# funciona y verás su desplegable; el error rojo llega
# después, en el primer ___ de la pasada 2.
#
# Cuando funcione, prueba:
#   "¿Cuál es la tasa de churn del plan básico?"
#
# Ahora deberías ver una explicación en contexto. Son dos
# peticiones, y cada una tiene su desplegable "Lo que
# enviamos". Abre el de la pasada 2 y busca tu número dentro
# del system: el modelo no lo ha calculado, lo lee como texto.
#
# Ojo: como el paso 12 antes del reto de verdad, este archivo
# guarda la conversación en pantalla pero cada petición lleva
# solo la última pregunta.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Compara las interpretaciones de estas preguntas:
#        "¿Cuál es el margen medio por plan?"
#        "¿Los socios con app tienen menos churn?"
#        "¿Qué canal de captación trae socios más fieles?"
#      ¿Las explicaciones son útiles? ¿Añaden contexto real?
#      Busca cada número de la explicación dentro del system
#      de la pasada 2, que es lo único que el modelo ha visto.
#      ¿Están todos?
#
#   B. Prueba una pregunta donde el resultado sea un DataFrame
#      grande (como "Muestra el churn por centro y plan").
#      ¿La interpretación resume bien una tabla compleja?
#
#   C. Prueba a cambiar el tono del prompt de interpretación.
#      En vez de "analista de datos", pon "consultor senior
#      de McKinsey". ¿Cambia la calidad de la explicación?
#
# ── Vía avanzada ────────────────────────────────────────────
#
# Comprueba la explicación antes de enseñarla. Saca sus
# números con re.findall(r"\d+(?:[.,]\d+)?", interpretation)
# y busca cada uno en str(resultado). Si alguno no aparece,
# pon un st.warning debajo con los que faltan. Cuidado con los
# redondeos: 18.91 viene de 18.909556 y no aparece tal cual,
# y el modelo puede escribir 18,91 con coma. Prueba la
# pregunta del canal varias veces. ¿Qué número se escapa, y
# lo pilla tu comprobación?
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_13.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_13.py
# ============================================================

import streamlit as st
import pandas as pd
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"
MAX_RETRIES = 3

# ── Datos ───────────────────────────────────────────────────

@st.cache_data
def load_data():
    members = pd.read_csv("data/fitlife_members.csv")
    context = pd.read_csv("data/fitlife_context.csv")
    return members, context

df_members, df_context = load_data()

# ── Funciones auxiliares ────────────────────────────────────

def extract_code(text):
    """Extrae código Python de un bloque Markdown."""
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else None


def run_code(code, df_members, df_context):
    """Ejecuta código y devuelve (resultado, error)."""
    exec_globals = {
        "df_members": df_members,
        "df_context": df_context,
        "pd": pd,
    }
    try:
        exec(code, exec_globals)
        if "resultado" in exec_globals:
            return exec_globals["resultado"], None
        else:
            return None, "El código no definió la variable 'resultado'."
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ── Prompt del sistema (generación de código) ──────────────

SYSTEM_PROMPT = f"""Genera solo código Python/pandas que responda a la pregunta del usuario.

Tienes acceso a dos DataFrames ya cargados:

1. df_members: datos de socios ({len(df_members)} filas)
   Columnas: {list(df_members.columns)}
   Valores de 'plan': basic (29€), premium (49€), family (69€)
   Valores de 'center': downtown, northside, eastpark, westfield, southgate
   Valores de 'status': active, churned
   Valores de 'churn_reason': price, competitor, no_use, relocation, personal (null si activo)
   Valores de 'acquisition_channel': walk_in, referral, digital, january_campaign, corporate

2. df_context: contexto mensual ({len(df_context)} filas)
   Columnas: {list(df_context.columns)}

Reglas:
- Usa pandas para las operaciones.
- El código debe terminar con: resultado = <lo que calcules>
- NO uses print(). Solo asigna el resultado final a la variable "resultado".
- NO incluyas import ni read_csv: los datos ya están cargados.
- Devuelve SOLO el bloque de código, sin explicaciones antes ni después.
- Envuelve el código en triple backtick python.
- Si la pregunta requiere cruzar las dos tablas, usa df_members.merge(df_context, on="month").
- Para calcular tasa de churn: churned / total * 100."""

# ── Interfaz ────────────────────────────────────────────────

st.title("FitLife Analytics")
st.caption(f"Paso 13: El analista explica · {len(df_members)} registros")

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Socios: **{len(df_members)}** | Contexto: **{len(df_context)}** meses")
with col2:
    show_code = st.toggle("Mostrar código", value=False)

st.divider()

# ── Historial ───────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("code") and show_code:
            with st.expander("Código ejecutado"):
                st.code(msg["code"], language="python")

# ── Chat ────────────────────────────────────────────────────

if prompt := st.chat_input("Pregunta sobre los datos de FitLife..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generando y ejecutando código..."):

            # ── Pasada 1: generar y ejecutar código ─────────
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]

            resultado = None
            last_error = None
            last_code = None

            for intento in range(MAX_RETRIES):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                )
                generated = response.choices[0].message.content
                code = extract_code(generated)

                if not code:
                    last_error = "No se pudo extraer código de la respuesta."
                    last_code = generated
                    break

                last_code = code
                resultado, error = run_code(code, df_members, df_context)

                if error is None:
                    last_error = None
                    break
                else:
                    last_error = error
                    messages.append({"role": "assistant", "content": generated})
                    messages.append({
                        "role": "user",
                        "content": f"El código falló con este error:\n{error}\n\nCorrige el código.",
                    })
                    if intento < MAX_RETRIES - 1:
                        st.info(f"Intento {intento + 1} falló: {error}. Reintentando...")

        with st.expander("Lo que enviamos: pasada 1, el código"):
            st.json({"model": MODEL, "messages": messages})
        st.caption(f"Pasada 1: {intento + 1} petición(es), la última de {response.usage.prompt_tokens} tokens de prompt.")

        # ── Pasada 2: interpretar el resultado ──────────────
        if resultado is not None:
            if show_code and last_code:
                with st.expander("Código ejecutado"):
                    st.code(last_code, language="python")

            with st.spinner("Interpretando..."):

                # ── PASO A: construir el prompt de interpretación
                # Le damos al LLM la pregunta original, el resultado
                # calculado, y le pedimos que explique.
                #
                # ↓ Borra ___ y escribe el prompt. Ejemplo:
                #   f"""Eres un analista de datos experto en el negocio de FitLife,
                #   una red de 5 gimnasios de proximidad.
                #
                #   El usuario preguntó: {prompt}
                #   El resultado calculado sobre los datos reales es: {resultado}
                #
                #   Explica este resultado en el contexto del negocio.
                #   Sé conciso (2-3 frases). Usa los números reales.
                #   Si el resultado sugiere algo accionable, menciónalo."""

                interpretation_prompt = ___

                # ── PASO B: llamar al LLM para interpretar ──
                # Misma estructura que la pasada 1, pero esta vez
                # le pasamos el prompt de interpretación.
                #
                # ↓ Borra ___ y escribe:
                #   client.chat.completions.create(
                #       model=MODEL,
                #       messages=[
                #           {"role": "system", "content": interpretation_prompt},
                #           {"role": "user", "content": prompt}
                #       ]
                #   )

                interpretation_response = ___

                interpretation = interpretation_response.choices[0].message.content
                st.markdown(interpretation)
                answer_text = interpretation

                with st.expander("Lo que enviamos: pasada 2, la explicación"):
                    st.json({"model": MODEL, "messages": [{"role": "system", "content": interpretation_prompt}, {"role": "user", "content": prompt}]})
                st.caption(f"Pasada 2: {interpretation_response.usage.prompt_tokens} tokens de prompt, {interpretation_response.usage.completion_tokens} de respuesta.")
        else:
            error_msg = f"Sin resultado tras {intento + 1} intento(s) de {MAX_RETRIES}."
            if last_error:
                error_msg += f"\nÚltimo error: `{last_error}`"
            st.error(error_msg)
            answer_text = error_msg

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "code": last_code,
        })
