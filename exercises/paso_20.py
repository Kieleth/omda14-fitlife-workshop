# PASO 20: el CSV no contiene la respuesta
#
# 1. Pregunta por el plazo de baja en los tres modos. Cada envío es una
#    petición nueva: las respuestas anteriores no se añaden como contexto.
# 2. Mira los fragmentos y la petición exacta. Localiza la frase que respalda
#    la respuesta; una referencia válida no demuestra que se interpretó bien.
# 3. En fitlife_documents.py, cambia retrieve para reconocer un sinónimo
#    de tu pregunta. Predice qué fragmentos cambiarán y compruébalo sin API.
# 4. Crea un .md con una condición ficticia, súbelo, inclúyelo, responde.
#    Después exclúyelo y repite: cargar texto aquí no entrena el modelo.
#
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_20.py
# macOS: .venv/bin/python -m streamlit run exercises/paso_20.py

import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from fitlife_documents import load_course_documents, document_chunks, select_context, answer_documents

MODEL = 'gpt-4.1-mini'
MODES = ['Sin documentos', 'Todos los fragmentos', 'Buscar fragmentos']


def main():
    load_dotenv()
    st.title('Paso 20: responder con documentos')
    st.caption('Políticas ficticias de FitLife. Cada envío usa solo la pregunta y los fragmentos que ves aquí.')
    chunks = load_course_documents(Path(__file__).resolve().parents[1] / 'data/conocimiento')
    uploaded = st.file_uploader('Añade documentos de texto (.md o .txt, UTF-8)',
                                type=['md', 'txt'], accept_multiple_files=True)
    try:
        for file in uploaded:
            if file.name in {chunk['file'] for chunk in chunks}:
                raise ValueError(f'El nombre {file.name} ya existe. Renombra la copia para poder comparar versiones.')
            chunks.extend(document_chunks(file.name, file.getvalue()))
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    files = sorted({chunk['file'] for chunk in chunks})
    included = st.multiselect('Documentos disponibles para esta consulta', files, default=files)
    available = [chunk for chunk in chunks if chunk['file'] in included]
    with st.expander('1. Texto cargado y dividido en fragmentos'):
        st.json(available)
    mode = st.radio('Qué contexto enviar', MODES)
    limit = st.slider('Máximo de fragmentos al buscar', 1, 8, 3)
    question = st.text_input('Pregunta', '¿Con cuántos días de antelación hay que solicitar la baja?')
    try:
        selected = select_context(question, available, mode, limit)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    with st.expander('2. Fragmentos seleccionados para enviar', expanded=True):
        st.json(selected)
        st.caption(f'{len(selected)} fragmentos; {len(json.dumps(selected, ensure_ascii=False))} caracteres JSON. No es un recuento de tokens.')
    st.caption('La búsqueda cuenta palabras compartidas; no entiende sinónimos. Su puntuación no mide la verdad ni la confianza.')
    if st.button('Responder con este contexto', disabled=not question.strip()):
        try:
            with st.spinner('Enviando esta pregunta y sus fragmentos...'):
                record = answer_documents(OpenAI(), question, selected, MODEL)
            record['mode'] = mode
            st.session_state.document_result = record
        except (OpenAIError, ValueError) as exc:
            st.error(f'No se ha completado la consulta: {exc}')
    if 'document_result' in st.session_state:
        record = st.session_state.document_result
        st.subheader('Respuesta de la consulta guardada')
        st.write('Pregunta enviada: ' + record['question'])
        st.caption('Modo enviado: ' + record['mode'])
        if question != record['question'] or mode != record['mode'] or selected != record['chunks']:
            st.info('La selección ha cambiado. Esta respuesta pertenece a la consulta anterior; pulsa Responder para probar la nueva.')
        st.write(record['answer']['answer'])
        st.caption('Estado declarado por el modelo: ' + record['answer']['status'] + '. Comprueba el respaldo leyendo las fuentes.')
        for chunk in record['chunks']:
            if chunk['id'] in record['answer']['source_ids']:
                with st.expander(f"Fuente citada: {chunk['file']} · {chunk['section']}"):
                    st.text(chunk['text'])
                    st.caption('Identificador: ' + chunk['id'])
        with st.expander('3. Petición exacta y uso de tokens'):
            st.json({'request': record['request'], 'usage': record['usage']})
        st.download_button('Guardar consulta con sus fuentes', json.dumps(record, ensure_ascii=False, indent=2),
                           file_name='fitlife-documentos.json', mime='application/json', on_click='ignore')


if __name__ == '__main__':
    main()
