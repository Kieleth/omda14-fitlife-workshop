# ============================================================
# BONUS: mide el sistema con las doce preguntas de test  (resuelto)
# ============================================================
#
# ── ¿Para qué es este ejercicio? ────────────────────────────
#
# PREGUNTAS_TEST.md tiene doce preguntas. Son las mismas en
# todas las sesiones, para poder comparar. Hasta ahora las has
# probado a mano y de tres en tres. Esta app las lanza las
# doce de una vez y te deja poner la nota al lado de cada una.
#
# Es opcional y no depende de nada. Sale del paso 10: el mismo
# prompt, la misma regex, el mismo exec dentro de un try. Lo
# único que cambia es que aquí se mide.
#
# ── Lo que hace la app ──────────────────────────────────────
#
# Un botón lanza doce peticiones, una por pregunta. De cada
# una guarda el código generado, el resultado, el error si lo
# hubo, los tokens y los segundos. Luego pinta una tabla, el
# código de cada pregunta en un desplegable y, debajo, cuatro
# etiquetas para que pongas nota:
#
#   correcta    el número sale de los datos y responde
#   parcial     responde a medias, o a otra pregunta parecida
#   inventada   hay un número, pero no responde a lo que pides
#   no puede    los datos no dan para responder eso
#
# La diferencia entre "inventada" y "no puede" es la lección
# del paso 10, y para verla tienes que leer el código.
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Tres huecos ___. La app arranca con ellos sin rellenar: no
# revientan hasta que pulsas el botón.
#
#   1. texto_de_valores(): los valores de las columnas ya no
#      se escriben a mano, salen del DataFrame.
#   2. evaluar(): una pregunta, una petición y un diccionario
#      con lo que pasó. El contrato está en su docstring.
#   3. el recuento final de tus doce notas.
#
# ── Después, el reto de verdad ──────────────────────────────
#
# Apunta tu nota: cuántas correctas de doce. Ahora cambia el
# prompt, vuelve a lanzarlo y vuelve a puntuar:
#
#   A. Añade las reglas de negocio de ENUNCIADO.md: precios de
#      lista, qué es price_paid, qué cuenta como baja.
#   B. Añade un ejemplo resuelto, una pregunta con su código.
#   C. Añade temperature=0 a la llamada.
#
# ¿Sube la nota? ¿Con cuál de los tres sube más? ¿Alguno la
# baja? Escribe las dos notas y qué cambiaste en mis_notas.md.
#
# Y una pregunta sin truco: en la doce, "¿Debería FitLife
# bajar el precio del plan básico?", ¿qué sería una respuesta
# correcta? ¿Un sí, un no, o unos números y una decisión que
# toma otra persona? Lo que contestes ahí es lo que vas a
# tener que decidir en cada sistema de estos que construyas.
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/bonus_evaluacion.py
# macOS:   .venv/bin/python -m streamlit run exercises/bonus_evaluacion.py
# ============================================================

import re
import time

import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

st.title("FitLife: las doce preguntas")
st.caption("Bonus: lanza la batería de test y ponle nota al sistema")

df_members = pd.read_csv("data/fitlife_members.csv")
df_context = pd.read_csv("data/fitlife_context.csv")

st.subheader("Datos cargados")
st.write(f"Socios: **{len(df_members)}** registros | Contexto: **{len(df_context)}** meses")

st.divider()

# ── Las doce preguntas de PREGUNTAS_TEST.md ─────────────────

PREGUNTAS = [
    "¿Cuántos socios activos hay en el último mes?",
    "¿Cuál es la distribución de socios por plan?",
    "¿Cuál es el precio medio pagado por los socios?",
    "¿Cuál es el margen medio por socio (price_paid menos cost_to_serve) por plan?",
    "¿Cuál es la tasa de churn mensual de cada plan?",
    "¿Los socios que usan la app tienen menos churn que los que no?",
    "¿Qué canal de captación trae socios más fieles (menor churn)?",
    "¿Los socios que se dan de baja son más o menos rentables que los que se quedan?",
    "¿Las bajas del plan básico aumentaron cuando el competidor bajó precios?",
    "¿Las campañas de enero traen socios de peor calidad (más churn)?",
    "¿Cuál es el lifetime value medio por plan?",
    "¿Debería FitLife bajar el precio del plan básico?",
]

ETIQUETAS = ["correcta", "parcial", "inventada", "no puede"]
SIN_MARCAR = "sin marcar"

# Las columnas cuyo vocabulario le falta al modelo. El resto
# son números, fechas o identificadores: no caben en un prompt
# y no le ayudarían a escribir el filtro.
COLUMNAS_CON_VALORES = ["plan", "status", "center", "acquisition_channel", "churn_reason"]


# ── El prompt se construye desde los datos ──────────────────

def texto_de_valores(df, columnas):
    """Las líneas de valores del prompt, sacadas del DataFrame.

    Una línea por columna, con este aspecto exacto y tres
    espacios delante para que quede bajo la de Columnas:

       Valores de 'plan': premium, family, basic

    Los valores son los que la columna tiene de verdad, sin
    repetir y sin los huecos vacíos. Devuelve todas las líneas
    en un solo texto, separadas por saltos de línea.
    """
    lineas = []
    for columna in columnas:
        lineas.append(f"   Valores de '{columna}': " + ", ".join(str(valor) for valor in df[columna].dropna().unique()))
    return "\n".join(lineas)


def construir_system_prompt(df_members, df_context):
    """El prompt del paso 10 con los valores de las columnas dentro."""
    return f"""Genera solo código Python/pandas que responda a la pregunta del usuario.

Tienes acceso a dos DataFrames ya cargados:

1. df_members: datos de socios ({len(df_members)} filas)
   Columnas: {list(df_members.columns)}
{texto_de_valores(df_members, COLUMNAS_CON_VALORES)}

2. df_context: contexto mensual ({len(df_context)} filas)
   Columnas: {list(df_context.columns)}

Reglas:
- Usa pandas para las operaciones.
- El código debe terminar con: resultado = <lo que calcules>
- NO uses print(). Solo asigna el resultado final a la variable "resultado".
- NO incluyas import ni read_csv: los datos ya están cargados.
- Devuelve SOLO el bloque de código, sin explicaciones antes ni después.
- Envuelve el código en triple backtick python."""


# ── Una pregunta, una petición ──────────────────────────────

def ejecutar_codigo(codigo):
    """Ejecuta el código y devuelve (resultado, error); uno de los dos es None."""
    # Los CSV se releen aquí, en cada pregunta, a propósito. El
    # código generado se ejecuta con exec y puede modificar
    # df_members: crear una columna, reasignarlo, dejarlo
    # filtrado. Si las doce preguntas compartieran el mismo
    # DataFrame, la séptima trabajaría sobre lo que dejó la
    # sexta y no sabrías de quién es el número que lees.
    exec_globals = {
        "df_members": pd.read_csv("data/fitlife_members.csv"),
        "df_context": pd.read_csv("data/fitlife_context.csv"),
        "pd": pd,
    }
    try:
        exec(codigo, exec_globals)
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    if "resultado" not in exec_globals:
        return None, "El código no definió la variable 'resultado'."
    return exec_globals["resultado"], None


def evaluar(pregunta, system_prompt):
    """Una pregunta, una petición, un diccionario con lo que pasó.

    Devuelve un diccionario con estas siete claves:

        pregunta            la pregunta, tal cual llegó
        codigo              el código extraído; si no venía en
                            un bloque, la respuesta entera
        resultado           lo que el código dejó en resultado
        error               el error, o None si no lo hubo
        prompt_tokens       los de usage en la respuesta
        completion_tokens   los de usage en la respuesta
        segundos            lo que tardó la petición

    Pide el código con client.chat.completions.create, modelo
    gpt-4.1-mini y los dos mensajes de siempre: el system con
    system_prompt y el user con la pregunta. Saca el código
    del bloque Markdown con la receta del paso 9 y ejecútalo
    con ejecutar_codigo(), que ya está escrita. Si no hay
    bloque de código no hay nada que ejecutar, y eso también
    cuenta como error. Los segundos son los de la petición,
    no los del exec.
    """
    inicio = time.time()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pregunta},
        ],
    )
    segundos = time.time() - inicio
    generado = response.choices[0].message.content
    match = re.search(r"```(?:python)?\n(.*?)```", generado, re.DOTALL)
    if match:
        resultado, error = ejecutar_codigo(match.group(1))
    else:
        resultado, error = None, "No se pudo extraer código de la respuesta."
    return {
        "pregunta": pregunta,
        "codigo": match.group(1) if match else generado,
        "resultado": resultado,
        "error": error,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "segundos": segundos,
    }


def resumen(valor):
    """El resultado en una línea corta, para que quepa en la tabla."""
    if valor is None:
        return ""
    texto = " ".join(str(valor).split())
    return texto if len(texto) <= 80 else texto[:77] + "..."


# ── La tirada ───────────────────────────────────────────────

if st.button("Lanzar las doce preguntas"):
    system_prompt = construir_system_prompt(df_members, df_context)
    barra = st.progress(0.0)
    resultados = []
    for numero, pregunta in enumerate(PREGUNTAS, 1):
        resultados.append(evaluar(pregunta, system_prompt))
        barra.progress(numero / len(PREGUNTAS))
    barra.empty()
    st.session_state["system_prompt"] = system_prompt
    st.session_state["resultados"] = resultados

resultados = st.session_state.get("resultados")

if resultados:

    st.subheader("Las doce de un vistazo")
    tabla = pd.DataFrame([{
        "#": numero,
        "Pregunta": r["pregunta"],
        "Resultado": resumen(r["resultado"]),
        "Error": r["error"] or "",
        "Tokens": f"{r['prompt_tokens']} / {r['completion_tokens']}",
        "Segundos": round(r["segundos"], 1),
    } for numero, r in enumerate(resultados, 1)])
    st.dataframe(tabla, hide_index=True)

    st.subheader("El código, pregunta por pregunta")
    st.write("Abre cada uno, lee el código y pon tu nota debajo.")

    veredictos = []
    for numero, r in enumerate(resultados, 1):
        with st.expander(f"Código de la pregunta {numero}: {r['pregunta']}"):
            st.code(r["codigo"], language="python")
            if r["error"]:
                st.warning(r["error"])
            else:
                st.write("**Resultado:**")
                st.write(r["resultado"])
        veredictos.append(st.selectbox(
            f"Nota de la pregunta {numero}",
            [SIN_MARCAR] + ETIQUETAS,
            key=f"veredicto_{numero}",
        ))

    st.subheader("Tu nota")

    # El recuento: cuántas preguntas has puesto en cada
    # etiqueta de ETIQUETAS. Las que sigan sin marcar no
    # cuentan en ninguna.
    recuento = {etiqueta: veredictos.count(etiqueta) for etiqueta in ETIQUETAS}

    st.write(" | ".join(f"{etiqueta}: {recuento[etiqueta]}" for etiqueta in ETIQUETAS))
    st.caption(f"Sin marcar: {len(PREGUNTAS) - sum(recuento.values())} de {len(PREGUNTAS)}.")

    with st.expander("Lo que enviamos en cada petición"):
        st.code(st.session_state["system_prompt"], language="text")
