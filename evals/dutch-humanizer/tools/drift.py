#!/usr/bin/env python3
"""Instabiliteit na een tweede bewerking: verschil tussen eerste en tweede output.

Gebruik: python3 drift.py EERSTE_MAP TWEEDE_MAP
Rapporteert per case de tekengelijkenis (difflib) en het gemiddelde.
"""
import difflib, statistics, sys
from pathlib import Path

def main():
    a, b = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    for f in sorted(b.glob("*.txt")):
        first = (a / f.name).read_text(encoding="utf-8")
        second = f.read_text(encoding="utf-8")
        ratio = difflib.SequenceMatcher(None, first, second).ratio()
        rows.append((f.stem, ratio))
        print(f"{f.stem}: {ratio:.3f}")
    if rows:
        print(f"gemiddeld: {statistics.mean(r for _, r in rows):.3f}; ongewijzigd: {sum(r == 1.0 for _, r in rows)}/{len(rows)}")

if __name__ == "__main__":
    main()
