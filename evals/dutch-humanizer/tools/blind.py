#!/usr/bin/env python3
"""Maak geblindeerde beoordelingspakketten met een vaste seed.

Gebruik: python3 blind.py RUNMAP UITMAP --run N --conditions A B C [D] --seed S
RUNMAP bevat <conditie>-r<N>/<ID>.txt. Schrijft UITMAP/pakket-rN.md (voor de
beoordelaar) en UITMAP/sleutel-rN.json (alleen voor aggregatie).
"""
import argparse, json, random
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runmap", type=Path); ap.add_argument("uitmap", type=Path)
    ap.add_argument("--run", type=int, required=True)
    ap.add_argument("--conditions", nargs="+", required=True)
    ap.add_argument("--seed", type=int, default=20261008)
    a = ap.parse_args()
    cases = json.loads((HERE / "validatieset" / "beoordeling.json").read_text(encoding="utf-8"))["cases"]
    rng = random.Random(a.seed * 100 + a.run)
    labels = ["X", "Y", "Z", "W"][: len(a.conditions)]
    key, parts = {}, [f"# Beoordelingspakket run {a.run}\n"]
    for c in cases:
        order = a.conditions[:]
        rng.shuffle(order)
        key[c["id"]] = dict(zip(labels, order))
        parts.append(f"\n## {c['id']} ({c['type']}, taak: {c['task']})\n\n**Verzoek:** {c['verzoek']}\n\n**Input:**\n{c['input']}\n")
        parts.append("**Invarianten:** " + "; ".join(c["invarianten"]) + "\n\n**Niet:** " + "; ".join(c["niet"]) + "\n")
        for lab, cond in zip(labels, order):
            out = (a.runmap / f"{cond}-r{a.run}" / f"{c['id']}.txt")
            text = out.read_text(encoding="utf-8") if out.exists() else "[GEEN OUTPUT]"
            parts.append(f"\n### Output {lab}\n\n````text\n{text.rstrip()}\n````\n")
    a.uitmap.mkdir(parents=True, exist_ok=True)
    (a.uitmap / f"pakket-r{a.run}.md").write_text("".join(parts), encoding="utf-8")
    (a.uitmap / f"sleutel-r{a.run}.json").write_text(json.dumps(key, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main()
