"""Preserve the original exercise and verify its described corrections."""

import ast
import io
import os
from pathlib import Path
import re
import tokenize
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "exercises/paso_0.py").read_text(encoding="utf-8")
GUIDE = (ROOT / "SESION1_PASO0.md").read_text(encoding="utf-8")

# Huecos ___ de cada ejercicio y la solución documentada en sus comentarios.
# El archivo del alumno más estas soluciones debe ser el código de referencia.
SOLUTIONS = {
    "paso_1.py": [("\n___\n", '\nst.subheader("Análisis de socios")\n'),
                  ("\n___\n", '\nst.write("Bienvenido al panel de control de FitLife.")\n')],
    "paso_3.py": [("df_context = ___", 'df_context = pd.read_csv("data/fitlife_context.csv")'),
                  ("{___}", "{len(df_context)}"),
                  ("{___}", "{len(df_context.columns)}")],
    "paso_4.py": [("\n        ___\n", '\n        st.write(f"Has dicho: {prompt}")\n')],
    "paso_5.py": [("client = ___", "client = OpenAI()")],
    "paso_7.py": [("{___}", "{planes}"), ("{___}", "{centros}"),
                  ("{___}", "{status}"), ("{___}", "{canales}")],
}


# Correcciones de texto aprobadas sobre el material base; la copia MDA13 en referencia/ no cambia.
BASELINE_FIXES = {"paso_0.py": [("tu primer app web", "tu primera app web")],
                  "paso_7.py": [("Paso 7 — Prompt enriquecido", "Paso 7: Prompt enriquecido")]}


def blanks(source):
    """Huecos ___ en el código, sin contar los comentarios."""
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return sum(token.type == tokenize.NAME and token.string == "___" for token in tokens)


def optional(name):
    matches = re.findall(r"<!-- optional:" + name + r" -->\s*```python\n(.*?)```", GUIDE, re.S)
    if len(matches) != 1:
        raise ValueError(f"La guía debe contener exactamente un bloque optional:{name}.")
    return matches[0].strip()


class Paso0Tests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ, {
            key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"
        }, clear=True))
        self.enterContext(patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")))
        self.repaired = SOURCE.replace("import streamlt as st", "import streamlit as st")

    def test_session_keeps_the_original_exercise_code_and_order(self):
        self.assertEqual({p.name for p in (ROOT / "exercises").glob("*.py")},
                         {f"paso_{i}.py" for i in range(8)})
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        positions = []
        for number in range(8):
            with self.subTest(step=number):
                name = f"exercises/paso_{number}.py"
                current = (ROOT / name).read_text(encoding="utf-8")
                baseline = (ROOT / "docente/referencia" / name).read_text(encoding="utf-8")
                for old, new in BASELINE_FIXES.get(f"paso_{number}.py", []):
                    self.assertEqual(baseline.count(old), 1)
                    baseline = baseline.replace(old, new)
                solutions = SOLUTIONS.get(f"paso_{number}.py", [])
                self.assertEqual(blanks(current), len(solutions),
                                 f"paso_{number}.py debe entregarse con {len(solutions)} huecos ___ en el código.")
                solved = current
                for blank, solution in solutions:
                    self.assertIn(blank, solved, "El hueco no tiene la forma documentada.")
                    solved = solved.replace(blank, solution, 1)
                self.assertEqual(blanks(solved), 0)
                self.assertEqual(ast.dump(ast.parse(solved)), ast.dump(ast.parse(baseline)),
                                 "An exercise changed beyond its instructions. Review its scope with Luis.")
                positions.append(readme.index(f"]({name})"))
        self.assertEqual(positions, sorted(positions))

    def test_import_error_then_title_and_message_complete_the_exercise(self):
        app = AppTest.from_file(str(ROOT / "exercises/paso_0.py")).run()
        self.assertEqual(len(app.exception), 1)
        self.assertIn("No module named 'streamlt'", app.exception[0].message)
        app = AppTest.from_string(self.repaired).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Hola Mundo")
        self.assertEqual(app.markdown[0].value, "Si ves esto en el navegador, tu primera app web funciona.")
        self.assertEqual(len(app.text_input), 0)
        self.assertEqual(len(app.slider), 0)

    def test_editing_the_existing_text_changes_the_page(self):
        code = self.repaired.replace('"Hola Mundo"', '"Equipo Madrid"').replace(
            '"Si ves esto en el navegador, tu primera app web funciona."', '"Nuestra primera app"')
        app = AppTest.from_string(code).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Equipo Madrid")
        self.assertEqual(app.markdown[0].value, "Nuestra primera app")

    def test_original_optional_experiments_from_the_guide(self):
        for name in ("globos", "nieve", "slider"):
            with self.subTest(experiment=name):
                app = AppTest.from_string(self.repaired + "\n" + optional(name)).run()
                self.assertEqual(len(app.exception), 0)
                if name == "slider":
                    self.assertEqual(app.slider[0].value, 25)
                    app.slider[0].set_value(42).run()
                    self.assertEqual(app.slider[0].value, 42)
                    self.assertEqual(app.title[0].value, "Hola Mundo")
                    self.assertEqual(len(app.exception), 0)
                else:
                    self.assertEqual(len(app.get("balloons" if name == "globos" else "snow")), 1)
