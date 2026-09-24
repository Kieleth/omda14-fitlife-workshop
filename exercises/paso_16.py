# PASO 16: guardar, enviar y recuperar son tres acciones distintas
#
# Parte del analista del paso 15. Conserva el cálculo y la explicación.
# Ahora cada respuesta guarda también su petición, código y resultado.
#
# 1. Haz tres preguntas encadenadas. Cambia Mostrar código: deben seguir
#    las tres preguntas del usuario y los detalles de las tres respuestas.
# 2. Descarga la conversación. Recarga el navegador: estará vacío.
#    Recupera el JSON: vuelven los mensajes y sus detalles, sin llamar al modelo.
# 3. Abre chat_history.py. Lee api_messages: system primero, después role y
#    content de cada mensaje en orden. Sustituye la construcción repetida.
#    Conéctala a la petición inicial sustituyendo el bucle y también a la
#    petición de interpret_result, con su propio interp_prompt e history.
#    No copies code ni details a la API. Compara el JSON antes y después.
# 4. Prueba un archivo sin content: debe rechazarse sin borrar tu chat actual.
#
# Avanzado: limita la petición a los últimos dos turnos completos, pero
# conserva toda la conversación visible. Busca una pregunta que ya no
# pueda resolverse. No confundas limitar contexto con borrar mensajes.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_16.py
# macOS: .venv/bin/python -m streamlit run exercises/paso_16.py

import streamlit as st
import pandas as pd
import re
from copy import deepcopy
from chat_history import history_controls, draw_history
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"
MAX_RETRIES = 3

# ── Configuración de página (debe ir antes de cualquier otro comando st.) ──
st.set_page_config(page_title="FitLife Analytics v3", layout="wide")

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


def interpret_result(client, model, prompt, resultado, history):
    """Pide al LLM que interprete el resultado en contexto de negocio."""
    interp_prompt = f"""Eres un analista de datos experto en el negocio de FitLife,
una red de 5 gimnasios de proximidad con planes basic (29€), premium (49€) y family (69€).
Su competidor low-cost cobra 19€ y los socios del plan básico se están dando de baja.

El usuario preguntó: {prompt}
El resultado calculado sobre los datos reales ({len(df_members)} registros) es:
{resultado}

Explica este resultado en el contexto del negocio de FitLife.
Sé conciso (2-3 frases). Usa los números reales del resultado.
Si el resultado sugiere algo accionable para la decisión de precios, menciónalo."""

    messages = [
        {"role": "system", "content": interp_prompt}
    ] + [{"role": msg["role"], "content": msg["content"]} for msg in history]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content, messages


# ── Prompt del sistema (experto, con ejemplos) ─────────────

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

EJEMPLOS DE CÓDIGO:

Ejemplo 1. Tasa de churn por plan:
  churn_plan = df_members.groupby('plan')['status'].apply(
      lambda x: (x == 'churned').sum() / len(x) * 100
  )
  resultado = churn_plan

Ejemplo 2. Cruzar tablas (socios + contexto por mes):
  merged = df_members.merge(df_context, on='month')
  resultado = merged.groupby('month')[['visits_this_month', 'competitor_lowcost_price']].mean()

Ejemplo 3. Margen por socio y plan:
  df_members['margin'] = df_members['price_paid'] - df_members['cost_to_serve']
  resultado = df_members.groupby('plan')['margin'].mean()

Ejemplo 4. Comparar churn entre dos grupos:
  group_a = df_members[df_members['uses_app'] == True]
  group_b = df_members[df_members['uses_app'] == False]
  churn_a = (group_a['status'] == 'churned').sum() / len(group_a) * 100
  churn_b = (group_b['status'] == 'churned').sum() / len(group_b) * 100
  resultado = f"Con app: {{churn_a:.2f}}% churn, Sin app: {{churn_b:.2f}}% churn"

REGLAS DE CÁLCULO:
- Tasa de churn = (status == 'churned').sum() / total * 100
- Margen = price_paid - cost_to_serve
- Para cruzar tablas: df_members.merge(df_context, on='month')
- 'month' es string YYYY-MM. Para año: pd.to_datetime(df['month']).dt.year
- Un socio churned es uno con status == 'churned' en ese mes
- Para ingreso observado por socio en 2022-2024: agrupa por member_id y suma price_paid. No lo presentes como LTV completo: faltan periodos fuera de la muestra y una definición de valor y vida del cliente.

Reglas generales:
- Usa pandas para las operaciones.
- El código debe terminar con: resultado = <lo que calcules>
- NO uses print(). Solo asigna el resultado final a la variable "resultado".
- NO incluyas import ni read_csv: los datos ya están cargados.
- Devuelve SOLO el bloque de código, sin explicaciones antes ni después.
- Envuelve el código en triple backtick python."""

# ── Interfaz ────────────────────────────────────────────────

st.title("Paso 16: una conversación que puedes recuperar")
st.caption(f"Analista conversacional · {len(df_members)} registros · {MODEL}")

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Socios: **{len(df_members)}** | Contexto: **{len(df_context)}** meses")
with col2:
    show_code = st.toggle("Mostrar código", value=False)

st.divider()

# ── Historial ───────────────────────────────────────────────

history_controls("messages_v3")
draw_history(st.session_state.messages_v3, show_code)

# ── Chat ────────────────────────────────────────────────────

if prompt := st.chat_input("Pregunta sobre los datos de FitLife..."):
    st.session_state.messages_v3.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generando y ejecutando código..."):

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in st.session_state.messages_v3:
                messages.append({"role": msg["role"], "content": msg["content"]})

            sent_for_calculation = deepcopy(messages)
            resultado = None
            last_error = None
            last_code = None
            sent_for_interpretation = None  # No hay petición si el cálculo falla.

            for intento in range(MAX_RETRIES):
                last_request = deepcopy(messages)
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
            st.json({"model": MODEL, "messages": last_request})
        st.caption(f"Pasada 1: {intento + 1} petición(es), la última de {response.usage.prompt_tokens} tokens de prompt.")

        if show_code and last_code:
            with st.expander("Código ejecutado"):
                st.code(last_code, language="python")

        if resultado is not None:
            with st.spinner("Interpretando..."):
                interpretation, sent_for_interpretation = interpret_result(
                    client, MODEL, prompt, resultado, st.session_state.messages_v3)
                st.markdown(interpretation)
                answer_text = interpretation
        else:
            error_msg = f"Sin resultado tras {intento + 1} intento(s) de {MAX_RETRIES}."
            if last_error:
                error_msg += f"\nÚltimo error: `{last_error}`"
            st.error(error_msg)
            answer_text = error_msg

        st.session_state.messages_v3.append({
            "role": "assistant",
            "content": answer_text,
            "code": last_code,
            "details": {
                "peticion_inicial": sent_for_calculation,
                "ultimo_intento": last_request,
                "peticion_interpretacion": sent_for_interpretation,
                "resultado_calculado": str(resultado),
                "intentos": intento + 1,
            },
        })
    st.rerun()
