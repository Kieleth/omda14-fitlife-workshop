# ============================================================
# PASO 5: Conecta el cerebro  (resuelto)
# ============================================================
#
# ── ¿Qué es un LLM? ────────────────────────────────────────
#
# Un LLM (Large Language Model) es un programa que ha leído
# cantidades absurdas de texto: miles de millones de páginas
# web, libros, artículos, código. De todo eso ha aprendido
# patrones de lenguaje.
#
# Cuando le haces una pregunta, no busca la respuesta en
# ningún sitio. Genera texto palabra por palabra basándose en
# los patrones que aprendió. Es como un compañero que ha leído
# todo internet, tiene una memoria impresionante para el
# lenguaje, pero no tiene calculadora.
#
# Retén eso: no tiene calculadora. Es importante después.
#
# ── ¿Qué es una API? ───────────────────────────────────────
#
# Una API es una puerta de entrada. Tú envías un mensaje
# de texto a través de internet, OpenAI lo recibe, se lo pasa
# al modelo, el modelo genera una respuesta, y os la devuelve.
# Todo en 2-3 segundos.
#
#   Tu app → mensaje → API de OpenAI → modelo → respuesta → tu app
#
# ── ¿Qué es una API key? ───────────────────────────────────
#
# Una contraseña que os identifica. Cada petición cuesta dinero
# (fracciones de céntimo), así que OpenAI necesita saber quién
# pide qué. El curso te da una clave para el taller, la misma
# en todas las sesiones, publicada en el chat del curso; no la
# compartas fuera de clase.
#
# ── Cómo crear el archivo .env ──────────────────────────────
#
# La API key no va en el código (si lo subierais a internet,
# todo el mundo la vería). Va en un archivo separado llamado
# .env que el código lee automáticamente.
#
#   1. En VS Code, ve al explorador de archivos (panel izquierdo)
#   2. Haz clic derecho en la carpeta raíz del proyecto
#      (omda14-fitlife-workshop)
#   3. Selecciona "New File" (Nuevo archivo)
#   4. Escribe exactamente:  .env
#      (sí, empieza con un punto, sin extensión)
#   5. Dentro del archivo, escribe esta línea:
#      OPENAI_API_KEY=aquí-pega-la-clave-del-curso
#   6. Guarda el archivo: Ctrl+S (Windows) o Cmd+S (Mac)
#
#   ¿No ves el archivo en el explorador? A veces VS Code
#   oculta archivos que empiezan con punto. Ve a Archivo →
#   Preferencias → Configuración, busca "files.exclude" y
#   asegúrate de que .env no esté excluido.
#
# ── Errores comunes ─────────────────────────────────────────
#
#   "Missing credentials" u "OpenAIError" al arrancar
#     → No existe el archivo .env o no se llama exactamente
#       así. Repasa los pasos de arriba; .env.template
#       muestra el formato de la línea.
#
#   "AuthenticationError" o "Incorrect API key"
#     → Revisa que la clave en .env esté bien copiada,
#       sin espacios extra al principio o final.
#
#   "No module named 'openai'"
#     → Revisa el entorno y la instalación completa en SETUP.md.
#
#   "No module named 'dotenv'"
#     → Revisa el entorno y la instalación completa en SETUP.md.
#
#   "RateLimitError"
#     → Has hecho muchas peticiones seguidas. Espera unos
#       segundos y prueba otra vez.
#
# ── Tu reto ─────────────────────────────────────────────────
#
# Completa la línea marcada con ___ para crear el cliente
# de OpenAI. Es solo una palabra: OpenAI()
#
# ── Mira lo que viaja ───────────────────────────────────────
#
# Copia estas cinco líneas al final
# del archivo y quita el "# " del principio de cada una.
# Deben quedar con 4 espacios delante de with, igual que la
# línea "with st.chat_message" de arriba: así siguen dentro
# de "if prompt:", después del bocadillo del asistente.
#
#     with st.expander("Lo que enviamos"):
#         st.json({"model": "gpt-4.1-mini", "messages": [{"role": "user", "content": prompt}]})
#     with st.expander("Lo que recibimos"):
#         st.json(response.model_dump())
#     st.caption(f"Tokens: {response.usage.prompt_tokens} enviados, {response.usage.completion_tokens} recibidos")
#
# Guarda, pregunta algo y abre los dos desplegables. response se
# creó dentro del bocadillo del asistente, pero una variable
# sigue existiendo después de su bloque with: el with solo
# decide dónde se pinta.
#
# "Lo que enviamos" es lo que pusimos en messages: una lista
# con un diccionario (pares clave: valor). "role" dice quién habla ("user" eres tú;
# en el paso 6 aparece "system"). "content" es el texto. Con
# el nombre del modelo y la clave, eso es todo lo que sale
# del portátil: un JSON con texto dentro. JSON es un formato de
# texto para escribir datos con llaves, comillas y comas; lo que
# ves en el desplegable es JSON.
#
# "Lo que recibimos" es el JSON completo que devuelve la API;
# model_dump() lo convierte en un diccionario para poder
# mostrarlo. st.write solo enseña choices[0].message.content.
# ¿Qué más viene? usage cuenta tokens: un token es el trozo
# de texto con el que trabaja el modelo, una palabra corta o
# un trozo de palabra. prompt_tokens es lo que ha leído;
# completion_tokens, lo que ha escrito.
#
# explicaciones/api.html recorre el viaje de la petición desde
# tu app hasta el modelo y de vuelta. Ábrelo con doble clic.
#
# ── Si has terminado antes ──────────────────────────────────
#
#   A. Prueba preguntas de distintos tipos:
#      - Conocimiento: "¿Quién escribió El Quijote?"
#      - Matemáticas: "¿Cuánto es 347 × 28?"
#      - Código: "Escribe una función en Python que sume dos números"
#      - Creatividad: "Escribe un haiku sobre datos"
#      ¿En cuáles responde mejor? ¿En cuáles peor?
#
#   B. Prueba a preguntarle en inglés y en español la misma
#      cosa. ¿Cambia la calidad de la respuesta?
#
#   C. Prueba: "¿Qué sabes sobre FitLife, una red de gimnasios?"
#      ¿Sabe algo? ¿Se lo inventa? ¿Cómo lo sabrías?
#
# Ejecuta desde la carpeta del proyecto, según tu sistema:
# Windows: .venv\Scripts\python.exe -m streamlit run exercises/paso_5.py
# macOS:   .venv/bin/python -m streamlit run exercises/paso_5.py
# ============================================================

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

st.title("FitLife Dashboard")

prompt = st.chat_input("Pregunta lo que quieras...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        st.write(response.choices[0].message.content)

    with st.expander("Lo que enviamos"):
        st.json({"model": "gpt-4.1-mini", "messages": [{"role": "user", "content": prompt}]})
    with st.expander("Lo que recibimos"):
        st.json(response.model_dump())
    st.caption(f"Tokens: {response.usage.prompt_tokens} enviados, {response.usage.completion_tokens} recibidos")
