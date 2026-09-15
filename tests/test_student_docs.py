"""Keep the student entry points aligned with the supported setup."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ("README.md", "SETUP.md", "SESION1_CHECKLIST.md", "ACTUALIZAR.md")


class StudentDocsTests(unittest.TestCase):
    def test_current_guides_do_not_send_students_to_the_old_environment(self):
        for name in GUIDES:
            with self.subTest(guide=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"conda\s+activate|mda13-fitlife-workshop|`mda13`")

    def test_update_guide_does_not_discard_student_work(self):
        text = (ROOT / "ACTUALIZAR.md").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"git\s+(?:checkout\s+--|reset\b|clean\b|restore\b)")
        self.assertIn("git status", text)
        self.assertIn("git pull --ff-only", text)
