"""Conversation data shared by the session-four apps. No network or file writes."""

import json

import streamlit as st

MAX_TRANSCRIPT_BYTES = 1_000_000


def api_messages(system_prompt, history):
    """The API receives roles and text, never the UI's extra fields."""
    return [{"role": "system", "content": system_prompt}] + [
        {"role": message["role"], "content": message["content"]} for message in history
    ]


def export_history(history):
    raw = json.dumps({"version": 1, "messages": history}, ensure_ascii=False, allow_nan=False, indent=2)
    import_history(raw.encode('utf-8'))
    return raw


def import_history(raw):
    """Validate before replacing the current conversation. No pickle, eval or exec."""
    if len(raw) > MAX_TRANSCRIPT_BYTES:
        raise ValueError("El archivo supera 1 MB. Recupera una conversación más pequeña.")
    def reject_constant(value):
        raise ValueError(f"El archivo contiene un número JSON inválido: {value}.")
    try:
        data = json.loads(raw, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        raise ValueError("No es un JSON válido. Usa el archivo descargado con Guardar conversación.") from exc
    if not isinstance(data, dict) or set(data) != {"version", "messages"} or type(data['version']) is not int or data['version'] != 1:
        raise ValueError("Faltan version=1 y messages, o hay campos desconocidos. Usa el formato de esta app.")
    history = data['messages']
    if not isinstance(history, list) or len(history) > 1000:
        raise ValueError("messages debe ser una lista de hasta 1000 mensajes.")
    for position, message in enumerate(history, 1):
        if not isinstance(message, dict) or not {'role', 'content'} <= set(message):
            raise ValueError(f"El mensaje {position} necesita role y content.")
        if message['role'] not in ('user', 'assistant') or not isinstance(message['content'], str):
            raise ValueError(f"El mensaje {position} necesita un rol user/assistant y texto en content.")
        if set(message) - {'role', 'content', 'code', 'details'}:
            raise ValueError(f"El mensaje {position} contiene campos desconocidos.")
        if 'code' in message and message['code'] is not None and not isinstance(message['code'], str):
            raise ValueError(f"El código del mensaje {position} debe ser texto.")
        if 'details' in message and not isinstance(message['details'], dict):
            raise ValueError(f"Los detalles del mensaje {position} deben ser un objeto JSON.")
    return history


def history_controls(key):
    if key not in st.session_state:
        st.session_state[key] = []
    st.caption("El historial vive en esta sesión. Descárgalo antes de recargar o cerrar la pestaña.")
    with st.expander("Guardar o recuperar conversación"):
        try:
            saved = export_history(st.session_state[key])
        except ValueError as exc:
            st.error(f"No se puede guardar esta conversación: {exc}")
        else:
            st.download_button("Guardar conversación", saved,
                               file_name="fitlife-conversacion.json", mime="application/json", on_click="ignore")
        uploaded = st.file_uploader("Conversación guardada (.json)", type=['json'], key=key + '_upload')
        if st.button("Recuperar conversación", disabled=uploaded is None, key=key + '_restore'):
            try:
                recovered = import_history(uploaded.getvalue())
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.session_state[key] = recovered
                st.rerun()
        st.caption("Recuperar sustituye la conversación actual. Guarda la actual primero si quieres conservarla.")


def draw_history(history, show_code=True):
    for message in history:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            if show_code and message.get('code'):
                with st.expander("Código ejecutado"):
                    st.code(message['code'], language='python')
            if 'details' in message:
                with st.expander("Detalle de este turno: petición y resultado"):
                    st.json(message['details'])
