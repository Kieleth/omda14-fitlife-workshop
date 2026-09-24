# PASO 14: sesión 3 resuelta, con la conversación completa en la petición
#
# Se conserva el ejercicio de la sesión 3 con sus huecos resueltos.
# Los comentarios siguientes describen el reto anterior para repasarlo;
# en esta rama ya no hay huecos que rellenar en este paso.
# En esta rama, las peticiones llevan las preguntas y respuestas anteriores.
# La sesión 3 original sigue disponible en clase/sesion-3 para comparar.
#
# Comprueba el historial con tres preguntas consecutivas y después cambia
# Mostrar código: deben seguir visibles las tres preguntas del usuario.
# El historial de session_state vive en esta conexión del navegador.
# Recargar la pestaña o reiniciar el servidor inicia otra sesión.
# La sesión 4 añade una copia descargable para recuperar la conversación.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_14.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_14.py

# ============================================================
# PASO 14: El prompt experto
# ============================================================
#
# ── ¿Qué hace con las preguntas difíciles? ─────────────────
#
# Prueba esta pregunta aquí, antes de rellenar los huecos
# (la app arranca con ellos vacíos):
#   "¿Las bajas del plan básico aumentaron cuando el
#    competidor bajó precios?"
#
# Puede que no falle: devolverá números. Abre el código y
# mira qué compara. ¿Cuenta bajas o calcula tasas? ¿Qué ha
# decidido que significa "cuando el competidor bajó precios"?
# Hazla dos veces: ¿decide lo mismo? Para responderla bien,
# el LLM tiene que:
#   1. Entender que necesita cruzar dos tablas
#   2. Saber que el competidor está en df_context
#   3. Calcular churn del básico por mes
#   4. Correlacionar con el precio del competidor
#
# Sin ayuda, el LLM tiene que adivinar toda esta lógica.
#
# ── La solución: enseñarle con ejemplos ─────────────────────
#
# Los humanos aprendemos con ejemplos. Los LLMs también.
# Si le muestras CÓMO resolver un tipo de pregunta, genera
# código mucho mejor para preguntas similares.
#
# Esto se llama "few-shot prompting": darle unos pocos
# ejemplos en el prompt para que entienda el patrón.
#
#   Prompt sin ejemplos (zero-shot):
#     "Genera código para responder a la pregunta."
#
#   Prompt con ejemplos (few-shot):
#     "Genera código para responder a la pregunta.
#      Ejemplo: para calcular tasa de churn por plan:
#        churn = df_members.groupby('plan')['status'].apply(
#            lambda x: (x == 'churned').sum() / len(x) * 100
#        )
#        resultado = churn"
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa las dos variables marcadas con ___ :
#
#   1. EXAMPLES: añadir ejemplos de código (la línea que
#      empieza por EXAMPLES, debajo de "PASO 1", fuera de
#      esta cabecera)
#   2. RULES: añadir reglas de cálculo del negocio (la línea
#      que empieza por RULES, debajo de "PASO 2")
#
# Los dos ___ están dentro de comillas: son texto, y la app
# arranca sin rellenarlos. Aprovéchalo. Antes de tocar nada,
# activa "Mostrar código", haz la pregunta del competidor
# y apunta dos cosas: qué compara el código y cuántos
# tokens pesa la petición (el pie de "Lo que enviamos").
# Después rellena, guarda, haz la misma pregunta y compara.
# En "Lo que enviamos" verás tus ejemplos dentro del system.
#
# Las PISTAS de más abajo llevan "#" delante porque son
# comentarios. Dentro de las comillas, cópialas sin el "#".
#
# Después, prueba las preguntas difíciles de PREGUNTAS_TEST.md
# (preguntas 7-12). ¿Cuántas más responde correctamente?
# Quizá ninguna daba error antes. Mira el código de cada una
# con y sin ejemplos: lo que cambia es qué calcula.
#
# En esta versión resuelta, ambas peticiones llevan el historial.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Añade más ejemplos al prompt. ¿Mejora la calidad?
#      ¿Hay un punto donde más ejemplos no ayudan?
#
#   B. Prueba a quitar los ejemplos que has añadido.
#      ¿Cuántas preguntas dejan de funcionar?
#
#   C. Prueba la pregunta 12: "¿Debería FitLife bajar el
#      precio del plan básico?" ¿Qué hace el sistema?
#      ¿La interpretación es útil? ¿Qué le falta? Abre el
#      código: ¿de dónde sale la recomendación?
#
# ── Vía avanzada ────────────────────────────────────────────
#
# Mide en vez de mirar. exercises/bonus_evaluacion.py lanza
# las doce preguntas de una vez. Pega tus ejemplos y tus
# reglas en el texto que devuelve construir_system_prompt(),
# encima de "Reglas:", lanza las doce y compara con una
# tirada sin ellos. Después quita un ejemplo cada vez: ¿qué
# respuestas cambian? El ejemplo que más cambia las
# respuestas no es por fuerza el que más ayuda.
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_14.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_14.py
# ============================================================

import streamlit as st
import pandas as pd
import re
from copy import deepcopy
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


def interpret_result(client, model, prompt, resultado, history):
    """Pide al LLM que interprete el resultado en contexto."""
    interp_prompt = f"""Eres un analista de datos experto en el negocio de FitLife,
una red de 5 gimnasios de proximidad.

El usuario preguntó: {prompt}
El resultado calculado sobre los datos reales es: {resultado}

Explica este resultado en el contexto del negocio.
Sé conciso (2-3 frases). Usa los números reales.
Si el resultado sugiere algo accionable, menciónalo."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": interp_prompt}
        ] + [{"role": msg["role"], "content": msg["content"]} for msg in history]
    )
    return response.choices[0].message.content


# ── Prompt del sistema (EXPERTO) ───────────────────────────
# Este es el prompt que vamos a mejorar con ejemplos y reglas.

# ── PASO 1: Escribe los ejemplos de código ──────────────────
# Copia aquí 2-3 ejemplos de las PISTAS de abajo.
# Reemplaza el ___ con el texto de los ejemplos.
#
# ↓ Borra ___ y escribe tus ejemplos (ver PISTAS más abajo)

EXAMPLES = """Ejemplo 1. Tasa de churn por plan:
  churn_plan = df_members.groupby('plan')['status'].apply(
      lambda x: (x == 'churned').sum() / len(x) * 100
  )
  resultado = churn_plan

Ejemplo 2. Cruzar tablas (socios + contexto):
  merged = df_members.merge(df_context, on='month')
  resultado = merged.groupby('month')[['visits_this_month', 'competitor_lowcost_price']].mean()

Ejemplo 3. Margen por socio:
  df_members['margin'] = df_members['price_paid'] - df_members['cost_to_serve']
  resultado = df_members.groupby('plan')['margin'].mean()"""

# ── PASO 2: Escribe las reglas de cálculo ───────────────────
# Copia aquí las reglas específicas del negocio.
# Reemplaza el ___ con las reglas.
#
# ↓ Borra ___ y escribe tus reglas (ver PISTAS más abajo)

RULES = """- Tasa de churn = churned / total * 100 (como porcentaje)
- Margen = price_paid - cost_to_serve
- Para cruzar tablas: df_members.merge(df_context, on='month')
- Un socio "churned" es uno con status == 'churned' en ese mes
- 'month' es string con formato YYYY-MM. Para extraer año: pd.to_datetime(df['month']).dt.year"""

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

{EXAMPLES}

REGLAS DE CÁLCULO:

{RULES}

Reglas generales:
- Usa pandas para las operaciones.
- El código debe terminar con: resultado = <lo que calcules>
- NO uses print(). Solo asigna el resultado final a la variable "resultado".
- NO incluyas import ni read_csv: los datos ya están cargados.
- Devuelve SOLO el bloque de código, sin explicaciones antes ni después.
- Envuelve el código en triple backtick python."""

# ═══════════════════════════════════════════════════════════
# PISTAS para los ___ de arriba:
#
# EJEMPLOS DE CÓDIGO: escribe 2-3 ejemplos como estos:
#
#   Ejemplo 1. Tasa de churn por plan:
#     churn_plan = df_members.groupby('plan')['status'].apply(
#         lambda x: (x == 'churned').sum() / len(x) * 100
#     )
#     resultado = churn_plan
#
#   Ejemplo 2. Cruzar tablas (socios + contexto):
#     merged = df_members.merge(df_context, on='month')
#     resultado = merged.groupby('month')[['visits_this_month', 'competitor_lowcost_price']].mean()
#
#   Ejemplo 3. Margen por socio:
#     df_members['margin'] = df_members['price_paid'] - df_members['cost_to_serve']
#     resultado = df_members.groupby('plan')['margin'].mean()
#
# REGLAS DE CÁLCULO: escribe reglas específicas del negocio:
#
#   - Tasa de churn = churned / total * 100 (como porcentaje)
#   - Margen = price_paid - cost_to_serve
#   - Para cruzar tablas: df_members.merge(df_context, on='month')
#   - Un socio "churned" es uno con status == 'churned' en ese mes
#   - 'month' es string con formato YYYY-MM. Para extraer año: pd.to_datetime(df['month']).dt.year
# ═══════════════════════════════════════════════════════════

# ── Interfaz ────────────────────────────────────────────────

st.title("FitLife Analytics")
st.caption(f"Paso 14: Prompt experto · {len(df_members)} registros")

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

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})

            resultado = None
            last_error = None
            last_code = None

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
                interpretation = interpret_result(client, MODEL, prompt, resultado, st.session_state.messages)
                st.markdown(interpretation)
                answer_text = interpretation
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
