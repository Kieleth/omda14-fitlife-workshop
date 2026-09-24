# PASO 17: el modelo pide una herramienta; tu código decide qué puede ejecutar
#
# 1. Pregunta por socios activos y churn del básico en el último mes.
#    Abre el detalle: petición -> tool_calls -> resultado de Python -> respuesta.
# 2. Pregunta qué pasa si el precio baja a 24 euros. Solo has ofrecido resumen_plan.
#    Localiza HERRAMIENTAS y añade la segunda definición de TOOLS.
#    Repite. Señala el argumento new_price y quién calcula el nuevo ingreso.
# 3. Lee escenario_precio en fitlife_tools.py. Verifica su resultado con pandas
#    y explica por qué NO calcula cuántas personas dejarán de darse de baja.
# 4. Ampliación opcional: construye una herramienta para otra pregunta de PREGUNTAS_TEST.md:
#    define población, periodo y unidad; escribe la función, su esquema y
#    su entrada en execute_tool. Compruébala primero sin llamar al modelo.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_17.py
# macOS: .venv/bin/python -m streamlit run exercises/paso_17.py

from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from chat_history import draw_history, history_controls
from fitlife_tools import TOOLS, ask_with_tools

HERRAMIENTAS = [TOOLS[0]]
MODEL = 'gpt-4.1-mini'


def main(tools):
    load_dotenv()
    st.title('Paso 17: herramientas explícitas para FitLife')
    st.caption('Las funciones permitidas están en fitlife_tools.py. Aquí no se ejecuta código generado.')
    df = pd.read_csv(Path(__file__).resolve().parents[1] / 'data/fitlife_members.csv')
    with st.expander('Herramientas que ofrecemos al modelo'):
        st.json(tools)
    history_controls('tool_chat')
    draw_history(st.session_state.tool_chat)
    if prompt := st.chat_input('Pregunta por un plan y un mes...'):
        st.session_state.tool_chat.append({'role': 'user', 'content': prompt})
        try:
            with st.spinner('Consultando las herramientas...'):
                answer = ask_with_tools(OpenAI(), df, st.session_state.tool_chat, MODEL, tools)
        except (OpenAIError, ValueError) as exc:
            answer = {'role': 'assistant', 'content': f'No se ha completado la consulta: {exc}'}
        st.session_state.tool_chat.append(answer)
        st.rerun()


if __name__ == '__main__':
    main(HERRAMIENTAS)
