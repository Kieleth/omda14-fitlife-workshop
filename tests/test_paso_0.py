"""Test the starter and each cumulative addition from the live-class guide."""

import ast
from contextlib import redirect_stdout
from io import StringIO
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "exercises/paso_0.py").read_text(encoding="utf-8")
GUIDE = (ROOT / "SESION1_PASO0.md").read_text(encoding="utf-8")


def block(name):
    matches = re.findall(r"<!-- build:" + name + r" -->\s*```python\n(.*?)```", GUIDE, re.S)
    if len(matches) != 1:
        raise ValueError(f"La guía debe contener exactamente un bloque build:{name}.")
    return matches[0].strip()


def stages():
    repaired = SOURCE.replace("import streamlt as st", "import streamlit as st")
    entry = repaired + "\n" + block("entrada") + "\n"
    if entry.count("st.write(mensaje)") != 1:
        raise ValueError("La etapa de entrada debe mostrar mensaje una sola vez.")
    transform = entry.replace("st.write(mensaje)", block("transformacion"))
    trace = transform + "\n" + block("traza") + "\n"
    rerun = trace.replace("import streamlit as st", "import streamlit as st\n" + block("arranque"))
    return repaired, entry, transform, trace, rerun


class Paso0Tests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ, {
            key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"
        }, clear=True))
        self.enterContext(patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")))
        self.output = self.enterContext(redirect_stdout(StringIO()))

    def test_starter_is_minimal_and_has_only_the_expected_import_error(self):
        self.assertEqual(len(ast.parse(SOURCE).body), 3, "Keep the starter small; students must add the interactive pieces.")
        app = AppTest.from_file(str(ROOT / "exercises/paso_0.py")).run()
        self.assertEqual(len(app.exception), 1)
        self.assertIn("No module named 'streamlt'", app.exception[0].message)
        repaired = AppTest.from_string(stages()[0]).run()
        self.assertEqual(len(repaired.exception), 0)
        self.assertEqual(len(repaired.title), 1)
        self.assertEqual(len(repaired.markdown), 1)
        self.assertEqual(len(repaired.text_input), 0)
        self.assertEqual(len(repaired.metric), 0)

    def test_every_addition_from_the_student_guide_runs(self):
        for number, code in enumerate(stages()):
            with self.subTest(stage=number):
                app = AppTest.from_string(code).run()
                self.assertEqual(len(app.exception), 0)
                if number == 0:
                    continue
                app.text_input[0].set_value("Hola, Madrid").run()
                expected = "Hola, Madrid" if number == 1 else "HOLA, MADRID"
                self.assertEqual(app.markdown[-1].value, expected)
                self.assertEqual(len(app.exception), 0)
                if number >= 3:
                    self.assertIn("Entrada: Hola, Madrid | Salida: HOLA, MADRID", self.output.getvalue())

    def test_code_changes_empty_input_and_rerun_trace(self):
        code = stages()[-1].replace('st.title("Hola, FitLife")', 'st.title("Equipo Madrid")').replace("mensaje.upper()", "mensaje.lower()")
        app = AppTest.from_string(code).run()
        self.assertEqual(app.title[0].value, "Equipo Madrid")
        before = self.output.getvalue().count("Se ejecuta paso_0")
        app.text_input[0].set_value("OTRO MENSAJE").run()
        self.assertEqual(app.markdown[-1].value, "otro mensaje")
        self.assertEqual(self.output.getvalue().count("Se ejecuta paso_0"), before + 1)
        app.text_input[0].set_value("").run()
        self.assertEqual(app.text_input[0].value, "")
        self.assertIn("Entrada:  | Salida: ", self.output.getvalue())
        self.assertEqual(len(app.exception), 0)
