#!/usr/bin/env python3
"""Draai check.py (kandidaat) op alle run-outputs en tel meldingen per conditie.

Gebruik: python3 lint_runs.py RUNMAP CHECK.PY
"""
import json, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

def main():
    runmap, script = Path(sys.argv[1]), sys.argv[2]
    cases = {c["id"]: c for c in json.loads((HERE / "validatieset" / "beoordeling.json").read_text())["cases"]}
    per = defaultdict(Counter)
    for d in sorted(p for p in runmap.iterdir() if p.is_dir()):
        for cid, c in cases.items():
            f = d / f"{cid}.txt"
            if not f.exists():
                per[d.name]["ontbreekt"] += 1
                continue
            src = c["input"] if c["input"] != "zie verzoek" else c["verzoek"].split('Tekst: "')[-1].rstrip('"')
            payload = {"output": f.read_text(encoding="utf-8"), "source": src}
            args = [sys.executable, script, "--stdin", "--format", "json", "--task", c["task"]]
            if c["task"] == "translate":
                args += ["--source-lang", "other"]
            r = subprocess.run(args, input=json.dumps(payload), capture_output=True, text=True)
            data = json.loads(r.stdout)
            for k, v in data["summary"].items():
                per[d.name][k] += v
    for name, cnt in per.items():
        print(name, dict(cnt))

if __name__ == "__main__":
    main()
