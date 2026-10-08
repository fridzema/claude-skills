#!/usr/bin/env python3
"""Ontblind beoordelingen en tel per conditie, zonder kritieke fouten weg te middelen.

Gebruik: python3 aggregate.py BEOORDELINGSMAP
Verwacht oordeel-rN.json (lijst {id, label, scores{...}, kritiek, bewijs, twijfel})
en sleutel-rN.json per run.
"""
import json, statistics, sys
from collections import defaultdict
from pathlib import Path

DIMS = ["inhoudsbehoud", "natuurlijk", "register_stem", "correctheid", "taak", "onnodig"]

def main():
    d = Path(sys.argv[1])
    per = defaultdict(lambda: {"n": 0, "kritiek": [], "dims": defaultdict(list), "geslaagd": 0, "runs": defaultdict(lambda: [0, 0])})
    for keyf in sorted(d.glob("sleutel-r*.json")):
        run = keyf.stem.split("-r")[1]
        key = json.loads(keyf.read_text())
        gf = d / f"oordeel-r{run}.json"
        if not gf.exists():
            continue
        for g in json.loads(gf.read_text()):
            cond = key[g["id"]][g["label"]]
            p = per[cond]
            p["n"] += 1
            for dim in DIMS:
                p["dims"][dim].append(g["scores"][dim])
            ok = not g["kritiek"] and g["scores"]["inhoudsbehoud"] == 3 and min(g["scores"].values()) >= 1
            p["geslaagd"] += ok
            p["runs"][run][0] += ok
            p["runs"][run][1] += 1
            if g["kritiek"]:
                p["kritiek"].append((run, g["id"], g.get("bewijs", "")))
    out = ["| Conditie | Beoordeeld | Geslaagd | Kritiek | " + " | ".join(DIMS) + " | Geslaagd per run |", "|" + "---|" * (5 + len(DIMS))]
    for cond in sorted(per):
        p = per[cond]
        means = [f"{statistics.mean(p['dims'][x]):.2f}" for x in DIMS]
        runs = ", ".join(f"r{r}: {a}/{b}" for r, (a, b) in sorted(p["runs"].items()))
        out.append(f"| {cond} | {p['n']} | {p['geslaagd']}/{p['n']} | {len(p['kritiek'])} | " + " | ".join(means) + f" | {runs} |")
    out.append("\nGeslaagd = geen kritieke fout, inhoudsbehoud 3 en geen dimensie 0. Gemiddelden per dimensie zijn aanvullend; kritieke fouten staan hieronder per geval.\n")
    for cond in sorted(per):
        for run, cid, ev in per[cond]["kritiek"]:
            out.append(f"- {cond} r{run} {cid}: {ev}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
