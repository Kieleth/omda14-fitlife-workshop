"""Exercise the intentional error and the app after the one-line student fix."""

from contextlib import redirect_stdout
from io import StringIO
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "exercises" / "paso_0.py").read_text(encoding="utf-8")


class Paso0Tests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(os.environ, {
            key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"
        }, clear=True))
        self.enterContext(patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")))
        self.output = self.enterContext(redirect_stdout(StringIO()))

    def corrected_app(self, source=SOURCE):
        self.assertEqual(source.count("import streamlt as st"), 1)
        return AppTest.from_string(source.replace("import streamlt as st", "import streamlit as st"))

    def test_starter_fails_only_on_the_intentional_import(self):
        app = AppTest.from_file(str(ROOT / "exercises" / "paso_0.py")).run()
        self.assertEqual(len(app.exception), 1)
        self.assertIn("No module named 'streamlt'", app.exception[0].message)
        self.assertEqual(len(app.title), 0)

    def test_corrected_app_exposes_real_input_output_and_reruns(self):
        app = self.corrected_app().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual([code.value for code in app.code], [repr("Hola, FitLife"), repr("HOLA, FITLIFE")])
        self.assertEqual([metric.value for metric in app.metric], ["1", "1"])
        message = "Hola, Madrid <b>23</b>"
        app.text_input[0].set_value(message).run()
        self.assertEqual([code.value for code in app.code], [repr(message), repr(message.upper())])
        self.assertEqual([metric.value for metric in app.metric], ["1", "2"])
        self.assertIn("entrada=" + repr(message), self.output.getvalue())
        self.assertIn("salida=" + repr(message.upper()), self.output.getvalue())
        app.button[0].click().run()
        self.assertEqual([metric.value for metric in app.metric], ["1", "3"])
        app.text_input[0].set_value("").run()
        self.assertEqual([code.value for code in app.code], ["''", "''"])
        self.assertEqual(len(app.exception), 0)

    def test_code_edits_and_new_sessions_are_distinct(self):
        edited = SOURCE.replace('titulo = "Hola, FitLife"', 'titulo = "Equipo Madrid"').replace("mensaje.upper()", "mensaje.lower()")
        first = self.corrected_app(edited).run()
        first.text_input[0].set_value("OTRO MENSAJE").run()
        self.assertEqual(first.code[1].value, repr("otro mensaje"))
        second = self.corrected_app(edited).run()
        self.assertEqual(second.title[0].value, "Equipo Madrid")
        self.assertEqual(second.code[1].value, repr("hola, fitlife"))
        self.assertEqual(second.session_state["ejecuciones"], 1)
        self.assertEqual(first.session_state["ejecuciones"], 2)
        self.assertEqual(len(second.exception), 0)
