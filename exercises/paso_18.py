# PASO 18: comparar modelos con la misma tarea y las mismas herramientas
#
# Antes de ejecutar, escribe qué respuesta aceptarías: periodo, población,
# unidades y límites. Solo después mira las salidas de los modelos.
# Cambia una cosa cada vez: pregunta, modelo o herramientas.
# Repite la misma comparación: una ejecución no establece un ganador.
# Un modelo de razonamiento puede consumir tokens que no aparecen en su texto.
# No estamos mostrando su razonamiento interno; mostramos peticiones y uso.
#
# Reto: añade a cada resultado tu veredicto y el motivo. Una respuesta más
# larga o más lenta no es una respuesta más correcta. Conserva el JSON.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_18.py
# macOS: .venv/bin/python -m streamlit run exercises/paso_18.py

import json
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from fitlife_tools import TOOLS, ask_with_tools, resumen_plan

load_dotenv()
st.title('Paso 18: mismo problema, distintos modelos')
st.caption('Los candidatos pueden requerir permisos de tu proyecto de API. Un error de acceso no mide calidad.')
df = pd.read_csv(Path(__file__).resolve().parents[1] / 'data/fitlife_members.csv')
models = st.multiselect('Modelos', ['gpt-4.1-mini', 'gpt-4.1-nano', 'o4-mini'], default=['gpt-4.1-mini'])
question = st.text_area('Pregunta común', '¿Cuántos socios activos tiene el plan básico en el último mes de los datos?')
criteria = st.text_area('Qué tendría que cumplir una respuesta correcta',
                        'Indicar el último mes del dataset, contar socios activos y no confundirlos con filas de tres años.')
with st.expander('Comprobación con Python, sin LLM'):
    st.json(resumen_plan(df, 'basic', 'ultimo'))

if st.button('Comparar', disabled=not models or not question.strip() or not criteria.strip()):
    results = []
    for model in models:
        try:
            with st.spinner(f'Consultando {model}...'):
                result = ask_with_tools(OpenAI(), df, [{'role': 'user', 'content': question}], model, TOOLS)
            results.append({'model': model, 'question': question, 'criteria': criteria, 'answer': result})
        except (OpenAIError, ValueError) as exc:
            results.append({'model': model, 'question': question, 'criteria': criteria, 'error': str(exc)})
    st.session_state.comparison = results

if 'comparison' in st.session_state:
    recorded = st.session_state.comparison[0]
    st.subheader('Resultados de la comparación guardada')
    st.write('Pregunta de esta ejecución: ' + recorded['question'])
    st.write('Criterio de esta ejecución: ' + recorded['criteria'])
    if question != recorded['question'] or criteria != recorded['criteria']:
        st.info('Has cambiado la pregunta o el criterio. Estos resultados siguen perteneciendo a la ejecución anterior. Pulsa Comparar para ejecutar la nueva.')
    for result in st.session_state.comparison:
        st.subheader(result['model'])
        if 'error' in result:
            st.error(result['error'])
            continue
        answer = result['answer']
        st.write(answer['content'])
        calls = answer['details']['calls']
        st.caption(f"{len(calls)} llamadas; {answer['details']['seconds']:.2f} segundos; "
                   f"{sum(c['usage']['prompt_tokens'] for c in calls)} tokens de entrada; "
                   f"{sum(c['usage']['completion_tokens'] for c in calls)} de salida.")
        with st.expander('Peticiones, resultados y uso devuelto por la API'):
            st.json(result)
    st.download_button('Guardar comparación', json.dumps(st.session_state.comparison, ensure_ascii=False, indent=2),
                       'fitlife-comparacion.json', 'application/json', on_click='ignore')
