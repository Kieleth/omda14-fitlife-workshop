"""Session 2 branch: session 1 ships solved, today's exercises stay aligned with the baseline, everything runs offline."""

import ast
import io
import json
import os
from pathlib import Path
import tokenize
import unittest
from unittest.mock import patch

import httpx2
import openai
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docente/referencia"
STEPS = range(12)

# Huecos ___ de los ejercicios de hoy y la solución documentada en sus comentarios.
# Los pasos 0 a 7 se entregan resueltos: no tienen huecos.
SOLUTIONS = {
    "paso_8.py": [('f"""___', 'f"""Genera solo código Python/pandas que responda a la pregunta del usuario.')],
    "paso_9.py": [("match = ___", 'match = re.search(r"```(?:python)?\\n(.*?)```", generated, re.DOTALL)'),
                  ("\n            ___\n", "\n            exec(code, exec_globals)\n")],
    "paso_10.py": [("with ___:", 'with st.expander("Ver código generado"):'),
                   ("\n                ___\n", '\n                st.error(f"Error al ejecutar el código: {e}")\n'),
                   ("with ___:", 'with st.expander("Detalles del error"):')],
}

# Correcciones de texto aprobadas sobre el material base; la copia MDA13 en referencia/ no cambia.
PROMPT_FIXES = [("FitLife — Text-to-Code", "FitLife: Text-to-Code"), ("df_members — datos", "df_members: datos"),
                ("df_context — contexto", "df_context: contexto"), ("read_csv — los datos", "read_csv: los datos")]
BASELINE_FIXES = {"paso_0.py": [("tu primer app web", "tu primera app web")],
                  "paso_7.py": [("Paso 7 — Prompt enriquecido", "Paso 7: Prompt enriquecido")],
                  **{f"paso_{n}.py": PROMPT_FIXES for n in range(8, 12)}}

# Errores intencionados de la sesión 1; en esta rama los pasos 0 a 7 se entregan corregidos.
INTENDED_ERRORS = {"paso_0.py": [("import streamlt as st", "import streamlit as st")],
                   "paso_2.py": [('pd.read_csv("fitlife_members.csv")', 'pd.read_csv("data/fitlife_members.csv")')]}


def blanks(source):
    """Huecos ___ en el código, también dentro de un texto; los comentarios no cuentan."""
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return "".join(token.string for token in tokens if token.type != tokenize.COMMENT).count("___")


def solved(source, name):
    for blank, solution in SOLUTIONS.get(name, []):
        if blank in source:
            source = source.replace(blank, solution, 1)
    return source


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


def lesson(source):
    return ast.dump(WithoutPresentation().visit(ast.parse(source)))


class ExerciseSourceTests(unittest.TestCase):
    def test_exercises_match_the_baseline_once_solved(self):
        self.assertEqual({p.name for p in (ROOT / "exercises").glob("*.py")}, {f"paso_{i}.py" for i in STEPS})
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        positions = []
        for number in STEPS:
            with self.subTest(step=number):
                name = f"paso_{number}.py"
                current = (ROOT / "exercises" / name).read_text(encoding="utf-8")
                baseline = (REFERENCE / ("exercises" if number < 8 else "exercises2") / name).read_text(encoding="utf-8")
                for old, new in BASELINE_FIXES.get(name, []) + INTENDED_ERRORS.get(name, []):
                    self.assertEqual(baseline.count(old), 1, (name, old))
                    baseline = baseline.replace(old, new)
                solutions = SOLUTIONS.get(name, [])
                self.assertEqual(blanks(current), len(solutions),
                                 f"{name} debe entregarse con {len(solutions)} huecos ___ en el código.")
                for blank, _ in solutions:
                    self.assertIn(blank, current, "El hueco no tiene la forma documentada.")
                current, baseline = solved(current, name), solved(baseline, name)
                self.assertEqual((blanks(current), blanks(baseline)), (0, 0))
                self.assertEqual(lesson(current), lesson(baseline),
                                 f"{name} cambió más allá de sus instrucciones. Revisa su alcance con el docente.")
                positions.append(readme.index(f"](exercises/{name})"))
        self.assertEqual(positions, sorted(positions))

    def test_no_em_dashes_in_student_files(self):
        for path in list((ROOT / "exercises").glob("*.py")) + [ROOT / "SESION2.md", ROOT / "README.md"]:
            with self.subTest(path=path.name):
                self.assertNotIn("—", path.read_text(encoding="utf-8"))


GOOD_CODE = "```python\nresultado = len(df_members)\n```"
BAD_CODE = "```python\nresultado = df_members['satisfaccion'].mean()\n```"


def completion(content):
    return {"id": "chatcmpl-test", "object": "chat.completion", "created": 0, "model": "gpt-4.1-mini",
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 250, "completion_tokens": 12, "total_tokens": 262}}


def answer(request):
    """Simula el modelo: código roto al primer intento de la pregunta de satisfacción, código válido después."""
    messages = json.loads(request.content)["messages"]
    first_attempt_on_failing_question = "satisfacción" in messages[-1]["content"] and len(messages) == 2
    return httpx2.Response(200, json=completion(BAD_CODE if first_attempt_on_failing_question else GOOD_CODE))


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

    def app(self, number, question=None, solve=False):
        path = ROOT / "exercises" / f"paso_{number}.py"
        source = path.read_text(encoding="utf-8")
        if solve:
            source = solved(source, path.name)
        app = AppTest.from_string(source).run(timeout=30)
        if question:
            app.chat_input[0].set_value(question).run(timeout=30)
        return app

    def assertClean(self, app):
        self.assertEqual([e.message for e in app.exception], [])

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

    def test_paso_8_shows_the_code_as_text_before_and_after_the_blank(self):
        for solve in (False, True):
            with self.subTest(solved=solve):
                app = self.app(8, "¿Cuántos registros tiene el dataset?", solve=solve)
                self.assertClean(app)
                self.assertEqual(app.code[0].value, GOOD_CODE.strip())
                self.assertEqual([x.label for x in app.expander], ["Lo que enviamos", "Lo que recibimos"])
                system = json.loads(app.json[0].value)["messages"][0]["content"]
                self.assertTrue(system.startswith("Genera solo código" if solve else "___"))
                self.assertIn("finish_reason: stop", app.caption[-1].value)

    def test_paso_9_fails_loudly_until_solved_then_runs_the_code(self):
        app = self.app(9, "¿Cuántos registros tiene el dataset de socios?")
        self.assertIn("name '___' is not defined", app.exception[0].message)
        app = self.app(9, "¿Cuántos registros tiene el dataset de socios?", solve=True)
        self.assertClean(app)
        self.assertEqual(app.code[0].value, "resultado = len(df_members)")
        self.assertEqual(app.markdown[-1].value, "`16334`")
        self.assertEqual([x.label for x in app.expander], ["Lo que enviamos", "Lo que recibimos"])

    def test_paso_10_reports_a_failing_code_without_crashing(self):
        app = self.app(10, "¿Cuál es la satisfacción media de los socios?", solve=True)
        self.assertClean(app)
        self.assertTrue(app.error[0].value.startswith("Error al ejecutar el código: 'satisfaccion'"))
        self.assertEqual([x.label for x in app.expander], ["Ver código generado", "Detalles del error"])
        app = self.app(10, "¿Cuántos registros tiene el dataset de socios?", solve=True)
        self.assertClean(app)
        self.assertEqual(len(app.error), 0)
        self.assertEqual(app.markdown[-1].value, "`16334`")

    def test_paso_11_sends_the_error_back_and_shows_the_conversation(self):
        app = self.app(11, "¿Cuál es la satisfacción media de los socios?")
        self.assertClean(app)
        self.assertTrue(app.info[0].value.startswith("Intento 1 falló: KeyError"))
        self.assertEqual(len(app.error), 0)
        self.assertIn("`16334`", [m.value for m in app.markdown])
        sent = json.loads(app.json[-1].value)["messages"]
        self.assertEqual([m["role"] for m in sent], ["system", "user", "assistant", "user"])
        self.assertIn("KeyError", sent[3]["content"])
        self.assertEqual(app.caption[-1].value, "Peticiones enviadas: 2. Cada una lleva la lista messages completa.")


if __name__ == "__main__":
    unittest.main()
