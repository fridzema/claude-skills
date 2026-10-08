#!/usr/bin/env python3
"""Draai de regressieprobes tegen een check.py-implementatie (oud of nieuw).

Gebruik: python3 run_probes.py PAD/NAAR/check.py [--json]
Werkt met de v0.6-API (check(output, source, ...)) en de v0.7-API (analyze(...)).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(script: Path):
    sys.path.insert(0, str(script.parent))
    spec = importlib.util.spec_from_file_location("check_under_test", script)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def run(mod, case):
    opts = case.get("options", {})
    if hasattr(mod, "analyze"):
        report = mod.analyze(case["output"], case["source"], **opts)
        return [{"severity": f.severity, "code": f.code, "message": f.message} for f in report.findings]
    kw = {}
    if "source_lang" in opts:
        kw["source_lang"] = opts["source_lang"]
    return [{"severity": f.level, "code": "", "message": f.message} for f in mod.check(case["output"], case["source"], **kw)]


def verdict(expect, findings):
    sev = {f["severity"] for f in findings}
    text = " ".join((f["code"] + " " + f["message"]).lower() for f in findings)
    serious = sev & {"ERROR", "WARNING"}
    equiv = "gelijkwaardig" in text and "niet" not in text.split("gelijkwaardig")[0][-12:]
    if expect == "detect":
        return bool(serious)
    if expect == "error":
        return "ERROR" in sev
    if expect == "clean":
        return not serious
    if expect == "warn_not_equivalent":
        return "WARNING" in sev and not equiv
    if expect == "not_called_equivalent":
        return not equiv and "ERROR" not in sev
    if expect == "precision_not_value":
        codes = {f["code"] for f in findings}
        if codes - {""}:
            return "QTY_PRECISION_CHANGED" in codes and not codes & {"QTY_VALUE_CHANGED", "QTY_REMOVED", "QTY_ADDED"}
        return "precisie" in text and "veranderd" not in text and "ontbreekt" not in text
    if expect == "no_value_change":
        return not serious
    if expect == "ambiguous":
        return "dubbelzinnig" in text or "ambigu" in text
    if expect == "optional":
        return True
    raise ValueError(expect)


def main():
    script = Path(sys.argv[1]).resolve()
    mod = load(script)
    cases = json.loads((HERE.parent / "probes.json").read_text(encoding="utf-8"))["cases"]
    rows = []
    for c in cases:
        try:
            f = run(mod, c)
            ok = verdict(c["expect"], f)
        except Exception as exc:  # oude API kent sommige opties niet
            f, ok = [{"severity": "CRASH", "code": "", "message": repr(exc)}], False
        rows.append({"id": c["id"], "case": c["case"], "expect": c["expect"], "pass": ok, "findings": f})
    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    else:
        for r in rows:
            first = "; ".join(f"{x['severity']} {x['message'][:70]}" for x in r["findings"][:2]) or "-"
            print(f"{r['id']} {'PASS' if r['pass'] else 'FAIL'} {r['case']:<28} {first}")
        print(f"{sum(r['pass'] for r in rows)}/{len(rows)} PASS")


if __name__ == "__main__":
    main()
