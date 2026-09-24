# PASO 21: pide un gráfico y comprueba de dónde salen sus puntos
#
# 1. Pide la evolución mensual del churn por plan. Localiza argumentos,
#    resultado de Python, gráfico y tabla. El modelo no suministra los valores.
# 2. Pide "ahora en barras". Ambos gráficos deben seguir visibles al hacer
#    otra pregunta o recuperar la conversación guardada.
# 3. Construye el soporte para otra métrica: define su población y unidad,
#    añádela a METRICS y a build_chart en fitlife_charts.py. No basta con
#    añadir un nombre al prompt. Comprueba primero una tabla pequeña a mano.
# 4. Prueba un mes sin datos y una petición ambigua. No confundas falta de
#    datos con cero ni un dibujo convincente con un cálculo correcto.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_21.py
# macOS: .venv/bin/python -m streamlit run exercises/paso_21.py

from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from chat_history import history_controls
from fitlife_tools import ask_with_tools
from fitlife_charts import CHART_TOOLS, SYSTEM, execute_chart, draw_chart

MODEL = 'gpt-4.1-mini'


def main():
    load_dotenv()
    st.title('Paso 21: gráficos a partir de tus preguntas')
    st.caption('El modelo elige argumentos. Python calcula sobre el CSV y Streamlit dibuja esos resultados.')
    df = pd.read_csv(Path(__file__).resolve().parents[1] / 'data/fitlife_members.csv')
    st.caption(f"Datos disponibles: {df['month'].min()} a {df['month'].max()}.")
    with st.expander('Herramienta de gráficos que recibe el modelo'):
        st.json(CHART_TOOLS)
    history_controls('chart_chat')
    chart_index = 0
    for message in st.session_state.chart_chat:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            if 'details' in message:
                details = message['details']
                if 'calls' in details:
                    try:
                        for call in details['calls']:
                            for tool in call['tool_results']:
                                if tool['name'] == 'crear_grafico':
                                    draw_chart(tool['result'], key=f'chart_csv_{chart_index}')
                                    chart_index += 1
                    except (KeyError, TypeError, ValueError) as exc:
                        st.error(f'No se puede dibujar el gráfico guardado: {exc}')
                with st.expander('Petición, argumentos y resultados de este turno'):
                    st.json(details)
    if prompt := st.chat_input('Por ejemplo: dibuja el churn mensual por plan durante 2024'):
        st.session_state.chart_chat.append({'role': 'user', 'content': prompt})
        try:
            with st.spinner('Preparando el cálculo y el gráfico...'):
                answer = ask_with_tools(OpenAI(), df, st.session_state.chart_chat, MODEL, CHART_TOOLS,
                                        executor=execute_chart, system=SYSTEM)
        except (OpenAIError, ValueError) as exc:
            answer = {'role': 'assistant', 'content': f'No se ha completado el gráfico: {exc}'}
        st.session_state.chart_chat.append(answer)
        st.rerun()


if __name__ == '__main__':
    main()
