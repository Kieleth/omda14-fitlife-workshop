"""Classroom deployment entrypoint: explicit tools and a shared access code."""

import hmac
import os

from dotenv import load_dotenv
import streamlit as st

from exercises.paso_17 import main
from fitlife_tools import TOOLS

load_dotenv()
st.set_page_config(page_title='FitLife · Herramientas', layout='wide')
password = os.environ.get('WORKSHOP_PASSWORD')
if not password:
    st.error('Falta WORKSHOP_PASSWORD en la configuración del servidor. El acceso está cerrado.')
    st.stop()
if not st.session_state.get('authenticated', False):
    with st.form('access'):
        entered = st.text_input('Código de acceso al taller', type='password')
        if st.form_submit_button('Entrar'):
            if hmac.compare_digest(entered.encode(), password.encode()):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error('Código incorrecto.')
    st.stop()
if not os.environ.get('OPENAI_API_KEY'):
    st.error('Falta OPENAI_API_KEY en la configuración del servidor. No se puede consultar el modelo.')
    st.stop()
main(TOOLS)
