# PASO 12: sesión 3 resuelta, con la conversación completa en la petición
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
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_12.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_12.py

# ============================================================
# PASO 12: El chat recuerda
# ============================================================
#
# ── ¿Qué hicimos en la sesión 2? ───────────────────────────
#
# Construimos un sistema text-to-code: el LLM genera código
# Python, lo ejecutamos con exec(), y mostramos el resultado.
# Añadimos manejo de errores y, opcionalmente, reintentos.
#
# Pero hay un problema: cada vez que escribes una pregunta,
# la app se OLVIDA de todo lo anterior. No puedes preguntar:
#
#   "¿Cuántos planes tiene FitLife?"
#   "¿Cuál es el más caro?"          ← no sabe de qué hablas
#
# ── ¿Por qué se olvida? ────────────────────────────────────
#
# Streamlit funciona de una forma especial: cada vez que
# el usuario hace CUALQUIER acción (escribir en el chat,
# pulsar un botón...), Streamlit ejecuta TODO el archivo
# de arriba a abajo, desde la línea 1.
#
# Es como si pulsaras "play" de nuevo cada vez. Todas las
# variables se reinician. Todo lo que no esté guardado en
# un sitio especial, desaparece.
#
# ── ¿Qué es st.session_state? ──────────────────────────────
#
# st.session_state es un diccionario especial que Streamlit
# mantiene vivo entre ejecuciones. Lo que guardes ahí,
# sobrevive:
#
#   # Primera ejecución:
#   st.session_state["nombre"] = "Ana"
#
#   # Segunda ejecución (el usuario hizo algo):
#   st.session_state["nombre"]  # → "Ana" (¡sigue ahí!)
#
# Para el chat, lo usamos así:
#
#   # Al principio del archivo (solo la primera vez):
#   if "messages" not in st.session_state:
#       st.session_state.messages = []
#
#   # Cuando el usuario escribe algo:
#   st.session_state.messages.append({"role": "user", ...})
#
#   # Para mostrar el historial:
#   for msg in st.session_state.messages:
#       with st.chat_message(msg["role"]):
#           st.write(msg["content"])
#
# Ojo con los nombres. st.session_state.messages es el
# historial que ves en pantalla. messages, a secas, es la
# lista que se envía al modelo en cada petición, la de la
# sesión 2. Son dos listas distintas.
#
# ── Tres cosas nuevas en el código ─────────────────────────
#
#   @st.cache_data, encima de load_data(): Streamlit guarda
#   lo que devuelve la función y no vuelve a leer los CSV en
#   cada ejecución. Cada ejecución recibe su propia copia.
#
#   if prompt := st.chat_input(...):  hace lo mismo que las
#   dos líneas de la sesión 2, prompt = st.chat_input(...)
#   seguida de if prompt:, escrito en una sola.
#
#   El interruptor "Mostrar código" (st.toggle) enseña el
#   código de cada respuesta. Actívalo antes de preguntar: en
#   la sesión 2 viste que es la única forma de saber qué se
#   ha calculado. Al tocarlo, el archivo vuelve a ejecutarse:
#   el historial se queda y los desplegables de la última
#   pregunta desaparecen hasta la siguiente.
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa las tres líneas marcadas con ___ :
#
#   1. Inicializar la lista de mensajes en session_state
#   2. Guardar el mensaje del usuario en el historial
#   3. Guardar la respuesta del asistente en el historial
#
# Antes de rellenar nada, arranca la app. El error rojo es
# el primer ___: Python lo lee nada más empezar, antes de
# que escribas nada.
#
# Cuando funcione, prueba este diálogo:
#   "¿Cuántos planes tiene FitLife?"
#   "¿Cuál es el que tiene más socios?"
#   "¿Y el que tiene más churn?"
#
# Las preguntas anteriores se mantienen en pantalla. Antes de
# enviar la segunda, apunta qué esperas que responda. Después
# abre "Lo que enviamos en la última petición", debajo de la
# respuesta: ¿qué ha recibido el modelo? ¿Está la primera
# pregunta ahí?
#
# ── El reto de verdad ──────────────────────────────────────
#
# El reto de enviar la conversación ya está resuelto en esta rama.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Haz 5-6 preguntas seguidas. ¿El historial se mantiene?
#      ¿Las respuestas tienen en cuenta las preguntas anteriores?
#
#   B. Recarga la página (F5). ¿Qué pasa con el historial?
#      ¿Por qué? (Pista: session_state vive mientras la
#      sesión del navegador esté abierta.)
#
#   C. Prueba las preguntas de PREGUNTAS_TEST.md una a una.
#      ¿Cuántas responde correctamente? Anota los resultados.
#
# ── Vía avanzada ────────────────────────────────────────────
#
# Con el reto de verdad hecho, cada pregunta envía la
# conversación entera, y el pie de la app dice cuánto pesa.
# Haz diez preguntas y apunta cómo crecen los tokens. Después
# envía solo las últimas cuatro entradas del historial (una
# lista se corta con [-4:]) y busca la pregunta de
# seguimiento que deja de funcionar. ¿Qué harías con una
# conversación de cien preguntas?
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_12.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_12.py
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

# ── Funciones auxiliares (de la sesión 2) ───────────────────

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


# ── Prompt del sistema (enriquecido) ───────────────────────

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
st.caption(f"Paso 12: El chat recuerda · {len(df_members)} registros")

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Socios: **{len(df_members)}** | Contexto: **{len(df_context)}** meses")
with col2:
    show_code = st.toggle("Mostrar código", value=False)

st.divider()

# ── PASO 1: Inicializar el historial ───────────────────────
# session_state es un diccionario que Streamlit mantiene vivo
# entre ejecuciones. Lo usamos para guardar los mensajes.
#
# Solo hay que inicializarlo UNA VEZ (la primera ejecución).
# Por eso comprobamos si ya existe antes de crearlo.
#
# ↓ Borra ___ y escribe:
#   st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Mostrar el historial de mensajes ───────────────────────
# Cada vez que Streamlit ejecuta el archivo, necesitamos
# re-dibujar todos los mensajes anteriores.

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("code") and show_code:
            with st.expander("Código ejecutado"):
                st.code(msg["code"], language="python")

# ── Chat ────────────────────────────────────────────────────

if prompt := st.chat_input("Pregunta sobre los datos de FitLife..."):

    # ── PASO 2: Guardar el mensaje del usuario ──────────────
    # Añadimos el mensaje del usuario al historial para que
    # se muestre en la siguiente ejecución.
    #
    # ↓ Borra ___ y escribe:
    #   st.session_state.messages.append({"role": "user", "content": prompt})

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

            # Mostrar resultado
            if resultado is not None:
                st.write(resultado)
                answer_text = str(resultado)
            else:
                error_msg = f"Sin resultado tras {intento + 1} intento(s) de {MAX_RETRIES}."
                if last_error:
                    error_msg += f"\nÚltimo error: `{last_error}`"
                st.error(error_msg)
                answer_text = error_msg

            if last_code and show_code:
                with st.expander("Código ejecutado"):
                    st.code(last_code, language="python")

        # ── PASO 3: Guardar la respuesta del asistente ──────
        # Igual que con el usuario, guardamos la respuesta
        # para que se muestre en el historial.
        #
        # ↓ Borra ___ y escribe:
        #   st.session_state.messages.append({"role": "assistant", "content": answer_text, "code": last_code})

        st.session_state.messages.append({"role": "assistant", "content": answer_text, "code": last_code})

    with st.expander("Lo que enviamos en la última petición"):
        st.json({"model": MODEL, "messages": messages})
    st.caption(f"Peticiones: {intento + 1}. La última llevó {len(messages)} entradas en messages y pesó {response.usage.prompt_tokens} tokens de prompt.")
