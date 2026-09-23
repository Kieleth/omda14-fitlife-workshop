"""Keep the student entry points aligned with the supported setup."""

from pathlib import Path
import unittest
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ("README.md", "SETUP.md", "SESION1_CHECKLIST.md", "ACTUALIZAR.md")
SESSION_GUIDES = tuple(sorted(p.name for p in ROOT.glob("SESION[0-9].md")))  # main has none


class StudentDocsTests(unittest.TestCase):
    def test_current_guides_do_not_send_students_to_the_old_environment(self):
        for name in GUIDES:
            with self.subTest(guide=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"conda\s+activate|mda13-fitlife-workshop|`mda13`")

    def test_student_text_is_self_paced_and_does_not_name_the_teacher(self):
        paths = [ROOT / name for name in GUIDES + SESSION_GUIDES + ("ENUNCIADO.md", "PREGUNTAS_TEST.md", "DE_EXPERIMENTO_A_PRODUCCION.md",
                                                                     "test_app.py", "check_setup.py")]
        paths += list((ROOT / "exercises").glob("*.py")) + list((ROOT / "explicaciones").glob("*.html"))
        for path in (path for path in paths if path.exists()):  # main carries only the preparation files
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(encoding="utf-8"),
                                    r"\bLuis\b|profesor|cuando .{0,20}lo indique",
                                    "El texto del alumno debe poder seguirse solo, sin nombrar al profesor.")

    def test_update_guide_does_not_discard_student_work(self):
        text = (ROOT / "ACTUALIZAR.md").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"git\s+(?:checkout\s+--|reset\b|clean\b|restore\b)")
        self.assertIn("git status", text)
        self.assertIn("git pull --ff-only", text)

    def test_student_route_has_no_editorial_history_or_teacher_notes(self):
        paths = [ROOT / name for name in GUIDES]
        paths += list((ROOT / "exercises").glob("*.py"))
        paths += [ROOT / name for name in SESSION_GUIDES]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(encoding="utf-8"),
                                    r"MDA13|mda13|material heredado|contenido original|pendiente de adapta|PLAN_DOCENTE")
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        for name in ("exercises2", "exercises3", "extras", "CONTENIDO_MDA13.md",
                     "SESION1_REPASO.md", "SESION2_REPASO.md", "PLAN_DOCENTE.md", "VERIFICACION.md"):
            self.assertFalse(any(path == name or path.startswith(name + "/") for path in tracked), name)
        if (ROOT / "exercises").is_dir():  # main carries only the preparation files
            names = {p.name for p in (ROOT / "exercises").glob("paso_*.py")}
            self.assertGreaterEqual(len(names), 8)
            self.assertEqual(names, {f"paso_{i}.py" for i in range(len(names))}, "los pasos van seguidos desde 0")
