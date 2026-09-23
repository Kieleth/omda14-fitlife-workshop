"""Session 3 branch: sessions 1 and 2 ship solved, today's exercises stay aligned with the baseline, everything runs offline."""

import ast
import io
import json
import os
from pathlib import Path
import re
import tokenize
import unittest
from unittest.mock import patch

import httpx2
import openai
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docente/referencia"
STEPS = range(16)

BONUS = "bonus_evaluacion.py"

# El cuerpo de evaluar(), el hueco grande del bonus de la sesión 2: su contrato está en el docstring.
EVALUAR = r'''
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
'''

INTERPRETATION_PROMPT = '''f"""Eres un analista de datos experto en el negocio de FitLife,
una red de 5 gimnasios de proximidad.

El usuario preguntó: {prompt}
El resultado calculado sobre los datos reales es: {resultado}

Explica este resultado en el contexto del negocio.
Sé conciso (2-3 frases). Usa los números reales.
Si el resultado sugiere algo accionable, menciónalo."""'''

INTERPRETATION_CALL = '''client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": interpretation_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )'''

# Las PISTAS del paso 14, copiadas dentro de las comillas sin el "#".
EXAMPLES = """Ejemplo 1. Tasa de churn por plan:
  churn_plan = df_members.groupby('plan')['status'].apply(
      lambda x: (x == 'churned').sum() / len(x) * 100
  )
  resultado = churn_plan

Ejemplo 2. Cruzar tablas (socios + contexto):
  merged = df_members.merge(df_context, on='month')
  resultado = merged.groupby('month')[['visits_this_month', 'competitor_lowcost_price']].mean()

Ejemplo 3. Margen por socio:
  df_members['margin'] = df_members['price_paid'] - df_members['cost_to_serve']
  resultado = df_members.groupby('plan')['margin'].mean()"""

RULES = """- Tasa de churn = churned / total * 100 (como porcentaje)
- Margen = price_paid - cost_to_serve
- Para cruzar tablas: df_members.merge(df_context, on='month')
- Un socio "churned" es uno con status == 'churned' en ese mes
- 'month' es string con formato YYYY-MM. Para extraer año: pd.to_datetime(df['month']).dt.year"""

# Huecos ___ y la solución documentada en sus comentarios. En esta rama los de la sesión 2
# se entregan rellenos (0 huecos) y los de hoy, vacíos; la referencia se resuelve con los mismos.
SOLUTIONS = {
    "paso_8.py": [('f"""___', 'f"""Genera solo código Python/pandas que responda a la pregunta del usuario.')],
    "paso_9.py": [("match = ___", 'match = re.search(r"```(?:python)?\\n(.*?)```", generated, re.DOTALL)'),
                  ("\n            ___\n", "\n            exec(code, exec_globals)\n")],
    "paso_10.py": [("with ___:", 'with st.expander("Ver código generado"):'),
                   ("\n                ___\n", '\n                st.error(f"Error al ejecutar el código: {e}")\n'),
                   ("with ___:", 'with st.expander("Detalles del error"):')],
    BONUS: [("lineas.append(___)",
             'lineas.append(f"   Valores de \'{columna}\': "'
             ' + ", ".join(str(valor) for valor in df[columna].dropna().unique()))'),
            ("\n    ___\n", EVALUAR),
            ("recuento = ___",
             "recuento = {etiqueta: veredictos.count(etiqueta) for etiqueta in ETIQUETAS}")],
    "paso_12.py": [('not in st.session_state:\n    ___', 'not in st.session_state:\n    st.session_state.messages = []'),
                   ('\n    ___\n\n    with st.chat_message("user")',
                    '\n    st.session_state.messages.append({"role": "user", "content": prompt})\n\n    with st.chat_message("user")'),
                   ("\n        ___\n",
                    '\n        st.session_state.messages.append({"role": "assistant", "content": answer_text, "code": last_code})\n')],
    "paso_13.py": [("interpretation_prompt = ___", "interpretation_prompt = " + INTERPRETATION_PROMPT),
                   ("interpretation_response = ___", "interpretation_response = " + INTERPRETATION_CALL)],
    "paso_14.py": [('\nEXAMPLES = """___"""', f'\nEXAMPLES = """{EXAMPLES}"""'),  # la cabecera nombra los dos huecos
                   ('\nRULES = """___"""', f'\nRULES = """{RULES}"""')],
}
SOLVED_BEFORE_TODAY = {"paso_8.py", "paso_9.py", "paso_10.py", BONUS}
TODAY = set()  # La sesión 4 entrega resueltos los pasos anteriores.

# El reto de verdad del paso 9, que el alumno pega en el prompt: esta rama lo entrega pegado.
PASTED = {"paso_9.py": [("   Columnas: {list(df_members.columns)}\n\n2.",
                         "   Columnas: {list(df_members.columns)}\n"
                         "   Valores de 'plan': basic (29€), premium (49€), family (69€)\n"
                         "   Valores de 'status': active, churned\n"
                         "   Valores de 'center': downtown, northside, eastpark, westfield, southgate\n\n2.")]}

# Correcciones de texto aprobadas sobre el material base; la copia en referencia/ no cambia.
# (texto, sustituto, apariciones esperadas en la referencia)
PROMPT_FIXES = [("FitLife — Text-to-Code", "FitLife: Text-to-Code", 1), ("df_members — datos", "df_members: datos", 1),
                ("df_context — contexto", "df_context: contexto", 1), ("read_csv — los datos", "read_csv: los datos", 1)]
# Un intento sin error borra el error del anterior, y el mensaje final cuenta los intentos que hubo de verdad.
RETRY_FIXES = [
    ("                if error is None:\n                    break\n",
     "                if error is None:\n                    last_error = None\n                    break\n", 1),
    ('"No se pudo obtener un resultado después de {MAX_RETRIES} intentos."',
     '"Sin resultado tras {intento + 1} intento(s) de {MAX_RETRIES}."', 1),
]
BASELINE_FIXES = {"paso_0.py": [("tu primer app web", "tu primera app web", 1)],
                  "paso_7.py": [("Paso 7 — Prompt enriquecido", "Paso 7: Prompt enriquecido", 1)],
                  **{f"paso_{n}.py": PROMPT_FIXES for n in range(8, 11)}}
BASELINE_FIXES["paso_11.py"] = PROMPT_FIXES + [
    ('"No se pudo obtener un resultado después de {MAX_RETRIES} intentos."',
     '"Sin resultado tras {intento + 1} intento(s) de {MAX_RETRIES}."', 1),
    ("                # ¡Éxito!\n                break\n", "                # ¡Éxito!\n                last_error = None\n                break\n", 1),
]
# Pasos de hoy: sin rayas largas, y 16.334 sin la coma de millares inglesa ("16,334").
TODAY_FIXES = PROMPT_FIXES[1:] + RETRY_FIXES
# "Mostrar código" enseña el código también cuando no hay resultado (resultado = None), como en el paso 12.
CODE_SHOWN_WITHOUT_RESULT = [(
    '        if resultado is not None:\n            if show_code and last_code:\n'
    '                with st.expander("Código ejecutado"):\n                    st.code(last_code, language="python")\n\n'
    '            with st.spinner("Interpretando..."):',
    '        if show_code and last_code:\n            with st.expander("Código ejecutado"):\n'
    '                st.code(last_code, language="python")\n\n'
    '        if resultado is not None:\n            with st.spinner("Interpretando..."):', 1)]
BASELINE_FIXES["paso_12.py"] = TODAY_FIXES + [("Paso 12 — El chat recuerda", "Paso 12: El chat recuerda", 1),
                                              ("{len(df_members):,}", "{len(df_members)}", 2)]
BASELINE_FIXES["paso_13.py"] = TODAY_FIXES + CODE_SHOWN_WITHOUT_RESULT + [("Paso 13 — El analista explica", "Paso 13: El analista explica", 1),
                                              ("{len(df_members):,}", "{len(df_members)}", 2)]
BASELINE_FIXES["paso_14.py"] = TODAY_FIXES + CODE_SHOWN_WITHOUT_RESULT + [("Paso 14 — Prompt experto", "Paso 14: Prompt experto", 1),
                                              ("{len(df_members):,}", "{len(df_members)}", 2)]
BASELINE_FIXES["paso_15.py"] = TODAY_FIXES + CODE_SHOWN_WITHOUT_RESULT + [("{len(df_members):,}", "{len(df_members)}", 3)] + [
    (f"Ejemplo {n} — ", f"Ejemplo {n}. ", 1) for n in range(1, 5)]

# Errores intencionados de la sesión 1; en esta rama los pasos 0 a 7 se entregan corregidos.
INTENDED_ERRORS = {"paso_0.py": [("import streamlt as st", "import streamlit as st", 1)],
                   "paso_2.py": [('pd.read_csv("fitlife_members.csv")', 'pd.read_csv("data/fitlife_members.csv")', 1)]}

# El reto de verdad del paso 12: tres líneas comentadas que el alumno activa quitando "# ".
HISTORY_SNIPPET = ('            # messages = [{"role": "system", "content": SYSTEM_PROMPT}]\n'
                   '            # for msg in st.session_state.messages:\n'
                   '            #     messages.append({"role": msg["role"], "content": msg["content"]})\n')


def blanks(source):
    """Huecos ___ en el código, también dentro de un texto; los comentarios no cuentan."""
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return "".join(token.string for token in tokens if token.type != tokenize.COMMENT).count("___")


def solved(source, name):
    for blank, solution in SOLUTIONS.get(name, []):
        if blank in source:
            source = source.replace(blank, solution, 1)
    return source


def with_history(source):
    return source.replace(HISTORY_SNIPPET, HISTORY_SNIPPET.replace("# ", "", 1).replace("\n            # ", "\n            "))


def reference(name):
    number = int(re.search(r"\d+", name).group())
    folder = "exercises" if number < 8 else "exercises2" if number < 12 else "exercises3"
    return (REFERENCE / folder / name).read_text(encoding="utf-8")


def is_st_call(node, name):
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == name
            and isinstance(node.func.value, ast.Name) and node.func.value.id == "st")


class WithoutPresentation(ast.NodeTransformer):
    """Los desplegables y pies de texto añadidos alrededor del ejercicio enseñan la petición; no son la lección."""

    def visit_With(self, node):
        if len(node.items) == 1 and is_st_call(node.items[0].context_expr, "expander"):
            return None
        return self.generic_visit(node)

    def visit_Expr(self, node):
        return None if is_st_call(node.value, "caption") else node


def fixed_history(source, number):
    state = "messages_v3" if number == 15 else "messages"
    old = '''            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]'''
    new = f'''            messages = [{{"role": "system", "content": SYSTEM_PROMPT}}]
            for msg in st.session_state.{state}:
                messages.append({{"role": msg["role"], "content": msg["content"]}})'''
    if source.count(old) != 1:
        raise AssertionError("La petición base ha cambiado: revisa la corrección del historial.")
    source = source.replace(old, new)
    if number == 13:
        source = source.replace('''                        {"role": "system", "content": interpretation_prompt},
                        {"role": "user", "content": prompt}
                    ]''', '''                        {"role": "system", "content": interpretation_prompt}
                    ] + [{"role": msg["role"], "content": msg["content"]}
                         for msg in st.session_state.messages]''')
    if number in (14, 15):
        source = source.replace("def interpret_result(client, model, prompt, resultado):", "def interpret_result(client, model, prompt, resultado, history):")
        source = source.replace('''            {"role": "system", "content": interp_prompt},
            {"role": "user", "content": prompt}
        ]''', '''            {"role": "system", "content": interp_prompt}
        ] + [{"role": msg["role"], "content": msg["content"]} for msg in history]''')
        source = source.replace("interpret_result(client, MODEL, prompt, resultado)", f"interpret_result(client, MODEL, prompt, resultado, st.session_state.{state})")
    return source


def lesson(source):
    return ast.dump(WithoutPresentation().visit(ast.parse(source)))


class ExerciseSourceTests(unittest.TestCase):
    def test_exercises_match_the_baseline_once_solved(self):
        names = {p.name for p in (ROOT / "exercises").glob("*.py")}
        steps = {f"paso_{i}.py" for i in STEPS}
        self.assertEqual({name for name in names if name.startswith("paso_")}, steps | {f"paso_{n}.py" for n in range(16, 20)})
        self.assertLessEqual(names - steps, {BONUS} | {f"paso_{n}.py" for n in range(16, 20)})
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        positions = []
        for number in STEPS:
            with self.subTest(step=number):
                name = f"paso_{number}.py"
                current = (ROOT / "exercises" / name).read_text(encoding="utf-8")
                baseline = reference(name)
                for old, new, count in BASELINE_FIXES.get(name, []) + INTENDED_ERRORS.get(name, []):
                    self.assertEqual(baseline.count(old), count, (name, old))
                    baseline = baseline.replace(old, new)
                for old, new in PASTED.get(name, []):
                    self.assertEqual(baseline.count(old), 1, (name, old))
                    baseline = baseline.replace(old, new)
                expected = len(SOLUTIONS.get(name, [])) if name in TODAY else 0
                self.assertEqual(blanks(current), expected,
                                 f"{name} debe entregarse con {expected} huecos ___ en el código.")
                if name in TODAY:
                    for blank, _ in SOLUTIONS.get(name, []):
                        self.assertIn(blank, current, "El hueco no tiene la forma documentada.")
                current, baseline = solved(current, name), solved(baseline, name)
                if number >= 12:
                    baseline = fixed_history(baseline, number)
                self.assertEqual((blanks(current), blanks(baseline)), (0, 0))
                self.assertEqual(lesson(current), lesson(baseline),
                                 f"{name} cambió más allá de sus instrucciones. Revisa su alcance con el docente.")
                positions.append(readme.index(f"](exercises/{name})"))
        self.assertEqual(positions, sorted(positions))

    def test_session_2_ships_solved_with_its_pasted_values(self):
        for name in SOLVED_BEFORE_TODAY:
            with self.subTest(name=name):
                source = (ROOT / "exercises" / name).read_text(encoding="utf-8")
                self.assertEqual(blanks(source), 0)
                self.assertIn("resuelto", source.splitlines()[1])
        self.assertIn("Valores de 'plan': basic (29€)", (ROOT / "exercises/paso_9.py").read_text(encoding="utf-8"))

    def test_solved_history_is_active_in_all_four_steps(self):
        for number in range(12, 16):
            source = (ROOT / f"exercises/paso_{number}.py").read_text(encoding="utf-8")
            self.assertIn('messages.append({"role": msg["role"], "content": msg["content"]})', source)
            self.assertNotIn(HISTORY_SNIPPET, source)

    def test_no_em_dashes_in_student_files(self):
        for path in list((ROOT / "exercises").glob("*.py")) + [ROOT / "SESION3.md", ROOT / "README.md"]:
            with self.subTest(path=path.name):
                self.assertNotIn("—", path.read_text(encoding="utf-8"))


GOOD_CODE = "```python\nresultado = len(df_members)\n```"
BAD_CODE = "```python\nresultado = df_members['satisfaccion'].mean()\n```"
NONE_CODE = "```python\n# No hay columna de satisfacción.\nresultado = None\n```"
EXPLANATION = "Hay 16334 registros, uno por socio y mes."


def completion(content):
    return {"id": "chatcmpl-test", "object": "chat.completion", "created": 0, "model": "gpt-4.1-mini",
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 250, "completion_tokens": 12, "total_tokens": 262}}


def answer(request):
    """Simula el modelo: explica si le piden explicar; si no, código roto al primer intento de la satisfacción,
    None para la edad, código válido para lo demás."""
    messages = json.loads(request.content)["messages"]
    if messages[0]["content"].startswith("Eres un analista"):
        return httpx2.Response(200, json=completion(EXPLANATION))
    last = messages[-1]["content"]
    first_attempt_on_failing_question = "satisfacción" in last and messages[-2]["role"] != "assistant"
    content = BAD_CODE if first_attempt_on_failing_question else NONE_CODE if "edad" in last else GOOD_CODE
    return httpx2.Response(200, json=completion(content))


class OfflineAppTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ, {
            key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"
        }, clear=True))
        self.enterContext(patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")))
        real = openai.OpenAI
        self.enterContext(patch("openai.OpenAI", lambda **kwargs: real(
            api_key="sk-test", http_client=httpx2.Client(transport=httpx2.MockTransport(answer)))))
        self.cwd = os.getcwd()
        os.chdir(ROOT)

    def tearDown(self):
        os.chdir(self.cwd)

    def app(self, number, *questions, solve=False, history=False):
        path = ROOT / "exercises" / (number if isinstance(number, str) else f"paso_{number}.py")
        source = path.read_text(encoding="utf-8")
        if solve:
            source = solved(source, path.name)
        if history:
            source = with_history(source)
        app = AppTest.from_string(source).run(timeout=30)
        for question in questions:
            app.chat_input[0].set_value(question).run(timeout=30)
        return app

    def assertClean(self, app):
        self.assertEqual([e.message for e in app.exception], [])

    def sent(self, app, label):
        expander = next(x for x in app.expander if x.label == label)
        return json.loads(expander.json[0].value)["messages"]

    def test_session_1_ships_solved_and_shows_the_request(self):
        self.assertEqual(self.app(0).title[0].value, "Hola Mundo")
        self.assertEqual(self.app(1).subheader[0].value, "Análisis de socios")
        self.assertEqual(len(self.app(2).dataframe), 1)
        app = self.app(3)
        self.assertClean(app)
        self.assertEqual([x.label for x in app.expander], ["Tu verdad: los recuentos de la sesión 1"])
        self.assertEqual(len(app.dataframe), 6)
        self.assertEqual(self.app(4, "hola").markdown[-1].value, "Has dicho: hola")
        for number in (5, 6, 7):
            with self.subTest(step=number):
                app = self.app(number, "¿Cuál es la tasa de churn del plan básico?")
                self.assertClean(app)
                self.assertEqual([x.label for x in app.expander], ["Lo que enviamos", "Lo que recibimos"])
                self.assertIn("250 enviados, 12 recibidos", app.caption[-1].value)
                sent = json.loads(app.json[0].value)
                self.assertEqual([m["role"] for m in sent["messages"]], ["user"] if number == 5 else ["system", "user"])

    def test_session_2_ships_solved(self):
        app = self.app(8, "¿Cuántos registros tiene el dataset?")
        self.assertClean(app)
        self.assertEqual(app.code[0].value, GOOD_CODE.strip())
        system = json.loads(app.json[0].value)["messages"][0]["content"]
        self.assertTrue(system.startswith("Genera solo código"))
        app = self.app(9, "¿Cuántos registros tiene el dataset de socios?")
        self.assertClean(app)
        self.assertEqual(app.markdown[-1].value, "`16334`")
        self.assertIn("Valores de 'plan': basic (29€), premium (49€), family (69€)",
                      json.loads(app.json[0].value)["messages"][0]["content"])
        app = self.app(10, "¿Cuál es la satisfacción media de los socios?")
        self.assertClean(app)
        self.assertTrue(app.error[0].value.startswith("Error al ejecutar el código: 'satisfaccion'"))
        self.assertEqual([x.label for x in app.expander],
                         ["Ver código generado", "Detalles del error", "Lo que enviamos", "Lo que recibimos"])
        app = self.app(11, "¿Cuál es la satisfacción media de los socios?")
        self.assertClean(app)
        self.assertTrue(app.info[0].value.startswith("Intento 1 falló: KeyError"))
        sent = json.loads(app.json[-1].value)["messages"]
        self.assertEqual([m["role"] for m in sent], ["system", "user", "assistant", "user"])

    def test_bonus_ships_solved_and_scores_the_twelve_questions_offline(self):
        app = self.app(BONUS)
        self.assertClean(app)
        app = app.button[0].click().run(timeout=60)
        self.assertClean(app)
        self.assertEqual(len(app.dataframe[0].value), 12)
        self.assertEqual(len([x for x in app.expander if x.label.startswith("Código de la pregunta")]), 12)
        self.assertEqual(app.markdown[-1].value, "correcta: 0 | parcial: 0 | inventada: 0 | no puede: 0")

    def test_paso_12_ships_solved(self):
        app = self.app(12)
        self.assertClean(app)
        self.assertEqual(len(app.chat_message), 0)

    def test_paso_12_remembers_on_screen_and_sends_the_conversation(self):
        app = self.app(12, "¿Cuántos planes tiene FitLife?", "¿Cuál es el que tiene más socios?", solve=True)
        self.assertClean(app)
        self.assertEqual([m.name for m in app.chat_message], ["user", "assistant", "user", "assistant"])
        self.assertEqual([m["role"] for m in app.session_state["messages"]], ["user", "assistant", "user", "assistant"])
        sent = self.sent(app, "Lo que enviamos en la última petición")
        self.assertEqual([m["role"] for m in sent], ["system", "user", "assistant", "user"])
        self.assertEqual(sent[-1]["content"], "¿Cuál es el que tiene más socios?")
        self.assertIn("4 entradas en messages y pesó 250 tokens", app.caption[-1].value)

    def test_paso_12_sends_roles_and_content_without_ui_fields(self):
        app = self.app(12, "¿Cuántos planes tiene FitLife?", "¿Cuál es el que tiene más socios?", solve=True, history=True)
        self.assertClean(app)
        sent = self.sent(app, "Lo que enviamos en la última petición")
        self.assertEqual([m["role"] for m in sent], ["system", "user", "assistant", "user"])
        self.assertEqual([m["content"] for m in sent[1:]],
                         ["¿Cuántos planes tiene FitLife?", "16334", "¿Cuál es el que tiene más socios?"])
        self.assertTrue(all(set(m) == {"role", "content"} for m in sent))

    def test_paso_12_counts_the_attempts_it_really_made(self):
        app = self.app(12, "¿Cuál es la edad media de los socios?", solve=True)
        self.assertClean(app)
        self.assertEqual(app.error[0].value, "Sin resultado tras 1 intento(s) de 3.")

    def test_paso_13_ships_solved_and_shows_both_requests(self):
        app = self.app(13, "¿Cuántos registros tiene el dataset de socios?")
        self.assertClean(app)
        self.assertEqual(len(app.expander), 2)
        app = self.app(13, "¿Cuántos registros tiene el dataset de socios?", solve=True)
        self.assertClean(app)
        self.assertEqual([x.label for x in app.expander],
                         ["Lo que enviamos: pasada 1, el código", "Lo que enviamos: pasada 2, la explicación"])
        self.assertIn(EXPLANATION, [m.value for m in app.markdown])
        second = self.sent(app, "Lo que enviamos: pasada 2, la explicación")
        self.assertIn("El resultado calculado sobre los datos reales es: 16334", second[0]["content"])
        self.assertEqual(app.session_state["messages"][-1]["content"], EXPLANATION)

    def test_paso_14_runs_before_and_after_the_examples(self):
        for solve in (False, True):
            with self.subTest(solved=solve):
                app = self.app(14, "¿Cuántos registros tiene el dataset de socios?", solve=solve)
                self.assertClean(app)
                system = self.sent(app, "Lo que enviamos: pasada 1, el código")[0]["content"]
                if solve:
                    self.assertIn("Ejemplo 1. Tasa de churn por plan:", system)
                    self.assertIn("- Margen = price_paid - cost_to_serve", system)
                else:
                    self.assertIn("Ejemplo 1. Tasa de churn por plan:", system)
                    self.assertNotIn("___", system)
                self.assertIn(EXPLANATION, [m.value for m in app.markdown])

    def test_paso_13_shows_the_code_when_there_is_no_result(self):
        app = AppTest.from_string(solved((ROOT / "exercises/paso_13.py").read_text(encoding="utf-8"), "paso_13.py")).run()
        app.toggle[0].set_value(True).run()
        app.chat_input[0].set_value("¿Cuál es la edad media de los socios?").run(timeout=30)
        self.assertClean(app)
        self.assertEqual(app.error[0].value, "Sin resultado tras 1 intento(s) de 3.")
        self.assertIn("resultado = None", app.code[-1].value)

    def test_paso_15_sends_the_conversation(self):
        app = self.app(15, "¿Cuántos planes tiene FitLife?", "¿Cuál es el que tiene más socios?")
        self.assertClean(app)
        self.assertEqual([m["role"] for m in self.sent(app, "Lo que enviamos: pasada 1, el código")],
                         ["system", "user", "assistant", "user"])

    def test_paso_15_retries_then_explains(self):
        app = self.app(15, "¿Cuál es la satisfacción media de los socios?")
        self.assertClean(app)
        self.assertTrue(app.info[0].value.startswith("Intento 1 falló: KeyError"))
        self.assertIn(EXPLANATION, [m.value for m in app.markdown])
        sent = self.sent(app, "Lo que enviamos: pasada 1, el código")
        self.assertEqual([m["role"] for m in sent], ["system", "user", "assistant", "user"])
        self.assertIn("Ejemplo 4. Comparar churn entre dos grupos:", sent[0]["content"])


if __name__ == "__main__":
    unittest.main()
