# Evaluatie (rubric v0.6.0)

Dit is de rubric en procedure van v0.6.0, met acht dimensies. Sinds v0.7.0 geldt voor de vergelijkende evaluatie `prompts/beoordelaar.md` (zes dimensies plus kritiek) en `rapport-v0.7.0.md`.

Twee soorten tests, met verschillende zekerheid.

| Soort | Bestand | Automatisch? | Wat het aantoont |
|---|---|---|---|
| Mechanisch | `dutch-humanizer/tests/` | Ja: `python3 -m unittest discover -s tests -v` | Dat `scripts/check.py` getallen, datums, code, citaten, URL's, namen en signaalwoorden correct vergelijkt. Niet dat een herschrijving dezelfde betekenis heeft. |
| Redactioneel | `ontwikkelset.md` (42 cases, sinds v0.7.0 plus 1 uit de validatieset) | Nee: een model voert de skill uit, een beoordelaar scoort | Of de skill natuurlijk Nederlands oplevert zonder betekenis te veranderen. |

Een geslaagde mechanische test zegt niets over semantische trouw. Een WARNING van het script is geen bewijs van betekenisverandering, en het ontbreken van een WARNING is geen bewijs van trouw.

## Procedure redactionele evaluatie

1. **Geef de agent alleen Verzoek en Input** van elke case, niet de invarianten of verwachtingen. Een script dat die velden uitsplitst staat hieronder.
2. **Laat de agent de skill volgen** en per case de output opslaan als `NN.txt`.
3. **Draai het script** op elke output met de input ernaast, en noteer ERROR en WARNING:

   ```bash
   python3 scripts/check.py out/NN.txt --input in/NN.txt
   ```

4. **Scoor elke output** op de rubric hieronder, met de invarianten en verwachtingen van de case ernaast. Laat bij voorkeur een ander model of een mens scoren dan het model dat de output maakte.
5. **Leg vast**: datum, model, skillversie, scores per case, en elke case met een score 0 of 1 op semantische trouw met een citaat van de fout.

Uitsplitsen van de cases:

```bash
python3 - <<'EOF'
import re, pathlib
s = pathlib.Path("evals/dutch-humanizer/ontwikkelset.md").read_text()
out = pathlib.Path("eval/cases"); out.mkdir(parents=True, exist_ok=True)
for block in re.split(r"^## ", s, flags=re.M)[1:]:
    body = block.split("**Invarianten:**")[0].split("\n", 1)[1]
    (out / f"{block[:2]}.md").write_text(body.strip() + "\n")
EOF
```

## Rubric

Elke dimensie krijgt 0 tot 3.

| Dimensie | 3 | 2 | 1 | 0 |
|---|---|---|---|---|
| Semantische trouw | Alle invarianten intact, niets toegevoegd | Een nuance licht verschoven, geen feit veranderd | Een invariant verzwakt (zekerheid, voorwaarde, termijn, item) | Een feit, ontkenning, actor of bron veranderd, of iets verzonnen |
| Natuurlijkheid | Leest als goed Nederlands van een moedertaalschrijver | Goed, met een stroeve plek | Meerdere stijve of vertaalde constructies | Even onnatuurlijk als de input of erger |
| Register | Past precies bij lezer, kanaal en locale | Kleine afwijking | Duidelijk te formeel of te informeel, of u/je gewisseld | Verkeerd register of verkeerde locale |
| Stem van de auteur | Herkenbaar de schrijver (n.v.t. zonder voorbeeld) | Grotendeels | Algemeen | Feiten uit het voorbeeld gelekt of karikatuur |
| Grammatica en spelling | Foutloos | Eén kleine fout | Meerdere fouten | Storende fouten |
| Geen formulepatronen | Geen opvallende patronen, ook geen nieuwe | Eén restje | Meerdere, of een nieuwe tic (staccato, overal dubbele punten) | Formulematig |
| Technische precisie | Elke vakbewering, code en term klopt | Een term onnodig vertaald | Een technische bewering vager | Technisch onjuist |
| Onnodige wijzigingen | Alleen gewijzigd wat beter werd | Een paar overbodige ingrepen | Veel onnodige ingrepen | Goede tekst herschreven tot slechtere |

**Drempel:** een case slaagt als semantische trouw 3 is en geen andere dimensie 0. Semantische trouw 2 is een aandachtspunt; 0 of 1 is een fout die de skill moet voorkomen.

Voor negatieve cases (N) telt vooral *onnodige wijzigingen*: ongewijzigd laten scoort 3.

## Resultaten

### v0.6.0, 2026-10-08

Uitgevoerd door drie subagents van hetzelfde model (Claude, Claude Code) die de skill volgden, gescoord door een aparte beoordelaar-agent van hetzelfde model. Dat is geen onafhankelijke menselijke beoordeling; zie de beperkingen in de README.

Zie [`eval-v0.6.0.md`](eval-v0.6.0.md): 40 van 42 cases geslaagd in de eerste ronde; beide mislukte cases kwamen door fouten in referentievoorbeelden, die daarna zijn gecorrigeerd.
