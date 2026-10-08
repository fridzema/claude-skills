# Evaluatie dutch-humanizer (ontwikkelmateriaal)

Deze map hoort bij de repository, niet bij het skillpakket. `skill.zip` bevat alleen wat een agent tijdens gebruik nodig heeft, plus de unittests van het meegeleverde script. Testsets, beoordelingen, ruwe runs en bronverantwoording blijven hier, zodat ze niet bij elke herschrijving geladen worden.

| Pad | Inhoud |
|---|---|
| `baseline-v0.6.0/` | Hashes en probe-uitkomsten van v0.6.0 (vóór de wijzigingen) |
| `probes.json`, `tools/run_probes.py` | De 26 regressieprobes uit de opdracht v0.7.0, uitvoerbaar tegen elke versie van `check.py` |
| `ontwikkelset.md` | De 42 cases uit v0.6.0. Gebruikt tijdens ontwikkeling en reparatie |
| `validatieset/` | 26 nieuwe cases, bevroren op 2026-10-08. `taken/` is wat de generator ziet; `beoordeling.json` bevat de asserties |
| `prompts/` | Vastgelegde generator- en beoordelaarsprompts |
| `tools/` | Blinderen, aggregeren, lint over runs, drift na tweede bewerking |
| `runs/` | Ruwe synthetische outputs per conditie en run |
| `beoordeling/` | Geblindeerde pakketten, sleutels en oordelen |
| `rapport-v0.7.0.md` | Resultaten en beperkingen |
| `audit-voorbeelden.md` | Auditlog van gecorrigeerde voorbeelden |

## Reproduceren

```bash
# Mechanisch, zonder model
cd dutch-humanizer && python3 -m unittest discover -s tests -v
python3 ../evals/dutch-humanizer/tools/run_probes.py scripts/check.py

# Redactioneel (model nodig): zie prompts/generator.md, daarna
python3 evals/dutch-humanizer/tools/blind.py RUNMAP evals/dutch-humanizer/beoordeling --run 1 --conditions A B C D
python3 evals/dutch-humanizer/tools/aggregate.py evals/dutch-humanizer/beoordeling
python3 evals/dutch-humanizer/tools/lint_runs.py RUNMAP dutch-humanizer/scripts/check.py
```

## Beperkingen van deze opzet

- "Nieuw bedacht" is niet "ongezien": de ontwikkelaar die de validatieset schreef, schreef ook de skill.
- Generator en beoordelaar zijn taalmodellen. Een ander model als beoordelaar verkleint zelfvoorkeur maar garandeert geen onafhankelijkheid. Er is geen menselijke kalibratie.
- Activatie (wanneer de skill geladen wordt) is niet gemeten; zie `activatie.json` voor de testset.
