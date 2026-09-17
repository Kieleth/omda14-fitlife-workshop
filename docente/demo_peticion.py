"""Muestra los bytes exactos que la app envía a la API, sin red y sin clave.

Para la pantalla de Luis. Usa la capa HTTP del propio SDK con un transporte
simulado: la petición que se construye es la real; la respuesta es inventada.

Ejecuta desde la carpeta del proyecto con el Python de .venv:
    .venv/bin/python docente/demo_peticion.py
    .venv\\Scripts\\python.exe docente\\demo_peticion.py
"""

import json

import httpx2
from openai import OpenAI

PREGUNTA = "¿Cuál es la tasa de churn del plan básico?"


def responder(request):
    print(request.method, request.url)
    for name, value in request.headers.items():
        print(f"  {name}: {'Bearer sk-…' if name == 'authorization' else value}")
    print("BODY:", request.content.decode("utf-8"))
    return httpx2.Response(200, json={
        "id": "chatcmpl-demo", "object": "chat.completion", "created": 0, "model": "gpt-4.1-mini",
        "choices": [{"index": 0, "finish_reason": "stop",
                     "message": {"role": "assistant", "content": "Respuesta simulada."}}],
        "usage": {"prompt_tokens": 21, "completion_tokens": 4, "total_tokens": 25},
    })


client = OpenAI(api_key="sk-test", http_client=httpx2.Client(transport=httpx2.MockTransport(responder)))
response = client.chat.completions.create(model="gpt-4.1-mini",
                                          messages=[{"role": "user", "content": PREGUNTA}])
print("\nRESPUESTA (JSON completo):")
print(json.dumps(response.model_dump(), ensure_ascii=False, indent=2))
print("\nLo que muestra st.write:", response.choices[0].message.content)
