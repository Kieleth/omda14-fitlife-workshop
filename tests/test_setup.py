import csv
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from check_setup import Check, ROOT, check_dataset, expected_packages, run_checks


class SetupTests(unittest.TestCase):
    def test_real_installation(self):
        failed = [check for check in run_checks() if not check.ok]
        self.assertEqual(failed, [])

    def test_checker_from_another_directory_without_api_key(self):
        env = {key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"}
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / "check_setup.py")],
                                    cwd=directory, env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_configuration_is_an_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "Recupera"):
                expected_packages(Path(directory))

    def test_incomplete_configuration_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.in").write_text("streamlit==1.63.0\n")
            with self.assertRaisesRegex(ValueError, "debe declarar"):
                expected_packages(root)

    def test_missing_and_damaged_data_never_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            path = root / "data" / "test.csv"
            cases = [None, "id,id\n1,2\n", "wrong\n1\n", "id,name\n1\n",
                     "id,name\n1,A,extra\n", "id,name\n", "id,name\n1,A\n2,B\n"]
            for contents in cases:
                with self.subTest(contents=contents):
                    if contents is not None:
                        path.write_text(contents)
                    self.assertFalse(check_dataset(root, "test.csv", 1, {"id", "name"}).ok)

    def test_blank_optional_values_are_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "data" / "test.csv").write_text("id,churn_reason\n1,\n")
            self.assertTrue(check_dataset(root, "test.csv", 1, {"id", "churn_reason"}).ok)

    def test_wrong_package_version_is_rejected(self):
        from importlib.metadata import version
        def wrong_version(name):
            return "0.0.0" if name == "openai" else version(name)
        with patch("check_setup.metadata.version", side_effect=wrong_version):
            checks = run_checks()
        self.assertFalse(next(check for check in checks if check.name == "openai").ok)

    def test_wrong_python_is_rejected(self):
        with patch("check_setup.sys.version_info") as version_info:
            version_info.major, version_info.minor = 3, 10
            self.assertFalse(run_checks()[0].ok)

    def test_cli_failure_has_nonzero_exit(self):
        from check_setup import main
        with patch("check_setup.run_checks", return_value=[Check("Datos", False, "Falta CSV")]), \
             patch("builtins.print"):
            self.assertEqual(main(), 1)

    def assert_inherited_content(self, root):
        manifest = json.loads((ROOT / "docente" / "material_base.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["files"]), 19)
        for name, checksum in manifest["files"].items():
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), checksum)

    def test_inherited_content_is_unchanged(self):
        self.assert_inherited_content(ROOT)

    def test_checkout_preserves_content_with_autocrlf(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            result = subprocess.run(
                ["git", "-c", "core.autocrlf=true", "checkout-index", "--all",
                 f"--prefix={destination.as_posix()}/"],
                cwd=ROOT, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_inherited_content(destination)


class AppTests(unittest.TestCase):
    def test_controls_work_without_network_or_credentials(self):
        env = {key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"}
        with patch.dict(os.environ, env, clear=True), \
             patch("socket.socket.connect", side_effect=AssertionError("Unexpected network access")):
            app = AppTest.from_file(str(ROOT / "test_app.py")).run(timeout=20)
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.error), 0)
            self.assertEqual(app.metric[0].value, "9")
            app.slider[0].set_value(7).run()
            self.assertEqual(app.metric[0].value, "49")
            self.assertEqual(app.session_state["executions"], 2)
            app.selectbox[0].set_value("premium").run()
            with (ROOT / "data" / "fitlife_members.csv").open() as handle:
                expected = sum(row["plan"] == "premium" for row in csv.DictReader(handle))
            self.assertEqual(int(app.metric[1].value), expected)
            self.assertEqual(len(app.exception), 0)

    def test_failed_check_does_not_show_a_ready_screen(self):
        with patch("check_setup.run_checks", return_value=[Check("Datos", False, "Falta CSV")]):
            app = AppTest.from_file(str(ROOT / "test_app.py")).run()
        self.assertGreater(len(app.error), 0)
        self.assertEqual(len(app.success), 0)
        self.assertEqual(len(app.slider), 0)


if __name__ == "__main__":
    unittest.main()
