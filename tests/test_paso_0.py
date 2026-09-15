"""Preserve the original exercise and verify its described corrections."""

import ast
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "exercises/paso_0.py").read_text(encoding="utf-8")
GUIDE = (ROOT / "SESION1_PASO0.md").read_text(encoding="utf-8")


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
                self.assertEqual(ast.dump(ast.parse(current)), ast.dump(ast.parse(baseline)),
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
        self.assertEqual(app.markdown[0].value, "Si ves esto en el navegador, tu primer app web funciona.")
        self.assertEqual(len(app.text_input), 0)
        self.assertEqual(len(app.slider), 0)

    def test_editing_the_existing_text_changes_the_page(self):
        code = self.repaired.replace('"Hola Mundo"', '"Equipo Madrid"').replace(
            '"Si ves esto en el navegador, tu primer app web funciona."', '"Nuestra primera app"')
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
