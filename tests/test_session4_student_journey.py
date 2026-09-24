"""Execute the documented Git handoff with a student's own committed notes."""

from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StudentGitJourneyTests(unittest.TestCase):
    def test_documented_notes_handoff_preserves_previous_work_and_current_exercise(self):
        guide = (ROOT / 'SESION4.md').read_text(encoding='utf-8')
        section = guide.split('### Traer tus notas', 1)[1].split('Abre `exercises/paso_15.py`', 1)[0]
        self.assertIn('si está, conserva esa versión y no ejecutes', section)
        commands = re.search(r'```text\n(.*?)\n```', section, re.S)[1].splitlines()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.check_output(['git', '-c', 'user.name=Student fixture',
                                                '-c', 'user.email=student@example.invalid', *args],
                                               cwd=root, text=True, stderr=subprocess.STDOUT)

            git('init', '-b', 'main')
            exercise = root / 'exercise.py'
            exercise.write_text('print("course starter")\n', encoding='utf-8')
            git('add', 'exercise.py')
            git('commit', '-m', 'Course starter')
            git('switch', '-c', 'alumno/sesion-3')
            exercise.write_text('print("my completed session 3")\n', encoding='utf-8')
            notes = root / 'mis_notas.md'
            notes.write_text('My predictions and observations.\n', encoding='utf-8')
            git('add', 'exercise.py', 'mis_notas.md')
            git('commit', '-m', 'Save my session 3')
            git('switch', '-c', 'alumno/sesion-4', 'main')
            self.assertFalse(notes.exists())
            for command in commands:
                parts = shlex.split(command)
                self.assertEqual(parts[0], 'git')
                git(*parts[1:])
            self.assertEqual(notes.read_text(encoding='utf-8'), 'My predictions and observations.\n')
            self.assertEqual(exercise.read_text(encoding='utf-8'), 'print("course starter")\n')
            self.assertEqual(git('status', '--porcelain'), '')
            git('switch', 'alumno/sesion-3')
            self.assertEqual(notes.read_text(encoding='utf-8'), 'My predictions and observations.\n')
            self.assertEqual(exercise.read_text(encoding='utf-8'), 'print("my completed session 3")\n')
