"""CLI: JSON-uitvoer, stdin, exitcodes en draaien vanuit een andere map."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "check"


def run(*args, stdin=None, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True,
                          check=False, cwd=cwd)


class CommandLine(unittest.TestCase):
    def test_json_schema(self):
        res = run(str(FIXTURES / "deadline-output.txt"), "--input", str(FIXTURES / "deadline-input.txt"),
                  "--format", "json")
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["schema_version"], "1")
        self.assertEqual(data["task"], "rewrite")
        self.assertIn("woordsignalen", data["checks_run"])
        codes = {f["code"] for f in data["findings"]}
        self.assertIn("SIG_NEGATION", codes)
        self.assertIn("SIG_TEMPORAL", codes)
        for f in data["findings"]:
            self.assertIn(f["severity"], ("ERROR", "WARNING", "INFO"))
            self.assertTrue(f["code"].isupper())
        self.assertIn("geen bewijs", data["note"])

    def test_stdin_mode_needs_no_files(self):
        payload = json.dumps({"source": "Betalen moet.", "output": "Betalen is verboden."})
        res = run("--stdin", "--format", "json", stdin=payload)
        self.assertEqual(res.returncode, 0)
        self.assertIn("SIG_PROHIBITION", {f["code"] for f in json.loads(res.stdout)["findings"]})

    def test_stdin_create_with_empty_output_fails(self):
        res = run("--stdin", "--task", "create", stdin=json.dumps({"output": ""}))
        self.assertEqual(res.returncode, 1)

    def test_runs_from_another_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = run(str(FIXTURES / "dash-output.txt"), cwd=tmp)
            self.assertEqual(res.returncode, 0, res.stderr)

    def test_usage_errors(self):
        self.assertEqual(run(str(FIXTURES / "bestaat-niet.txt")).returncode, 2)
        self.assertEqual(run("--stdin", stdin="geen json").returncode, 2)
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run(str(FIXTURES / "dash-output.txt"), "--task", "onzin").returncode, 2)

    def test_text_output_states_limits(self):
        res = run(str(FIXTURES / "deadline-output-goed.txt"), "--input", str(FIXTURES / "deadline-input.txt"))
        self.assertIn("Geen meldingen betekent niet dat de betekenis klopt", res.stdout)


if __name__ == "__main__":
    unittest.main()
