# Rapport dutch-humanizer v0.7.0

Datum: 2026-10-08. Basis: v0.6.0 (commit 569e1d1, tag v0.6.0). Kandidaat: werkboom na de wijzigingen in dit rapport. Niets gecommit of gepubliceerd.

## Status per testgroep

| Testgroep | Status | Resultaat |
|---|---|---|
| Unittests pakket (`python3 -m unittest discover -s tests`) | PASS | 85 van 85 (Python 3.14.8 en 3.9.6) |
| Regressieprobes opdracht sectie 8 (`tools/run_probes.py`) | PASS | v0.7.0: 26 van 26. v0.6.0: 4 van 26 (`baseline-v0.6.0/probes.txt`) |
| Vals-positieven op correcte parafrases (`tests/fixtures/equivalence.json`) | PASS | 32 parafrases; 3 met gedocumenteerde, bekende vals-positieven (9%) |
| Perturbaties met vaste seed (20261008) | PASS | elke toegepaste perturbatie gedetecteerd; zelfvergelijking zonder meldingen |
| Script op echte modeloutput (42 cases ontwikkelset, v0.6-outputs) | PASS | v0.7: 14 WARNING in 10 cases; v0.6: 15 WARNING in 11 cases. Alle 14 met de hand gecontroleerd: correcte parafrases, geen gemiste fouten gevonden |
| Redactionele vergelijking, 26 validatiecases x 3 runs | PASS (verkennend) | zie hieronder |
| Drift na tweede bewerking | PASS (verkennend) | zie hieronder |
| Compacte variant (alleen SKILL.md) | PASS (verkennend, 1 run) | zie hieronder |
| Activatie (wanneer de skill laadt) | NOT_RUN | testset in `activatie.json`; vraagt headless runs met de skill geregistreerd, wat een wijziging van de globale agentconfiguratie zou vergen |
| Menselijke beoordeling | NOT_RUN | geen menselijke beoordelaar beschikbaar |
| Officiële validator (`quick_validate.py`) | PASS | zie packaging |
| Upload naar claude.ai of ChatGPT | NOT_RUN | alleen lokaal gevalideerd |

## Gereproduceerde fouten (v0.6.0)

Alle uit de opdracht, met `probes.json`:

| Fout | Oorzaak | Oplossing |
|---|---|---|
| 1,5% naar 15% en 415% naar 41,5% niet gezien | Getallen vergeleken als cijferreeks zonder scheidingstekens | `Decimal` uit de tekens volgens locale |
| -5 naar 5 graden niet gezien | Teken genegeerd | Teken in de waarde; aparte code QTY_SIGN_CHANGED |
| 0,040 naar 0,04 mm gemeld als ander getal | Precisie niet onderscheiden | QTY_PRECISION_CHANGED, zelfde waarde |
| MB naar Mb, km weg, km erbij niet gezien | Eenheden kleingeschreven, alleen bij gelijke waarde vergeleken | Hoofdlettergevoelige eenheden; UNIT_CHANGED/REMOVED/ADDED |
| "1.234" stil gelijkgesteld | Scheidingstekens weggestript | Locale-parsing; onbekende locale geeft QTY_AMBIGUOUS |
| tenzij naar mits, moet naar verboden als "meestal gelijkwaardig" | Gelijkwaardigheidsgroepen | Families per betekenis; elke verschuiving is WARNING, nooit "gelijkwaardig" |
| kunt naar moet, klaar naar mogelijk klaar niet gezien | Alleen verdwenen woorden gemeld | Toevoegingen en verwijderingen in beide richtingen |
| tweemaal 21% naar eenmaal niet gezien | Verzamelingen zonder aantallen | Multipliciteit per waarde |
| /api/v1/orders naar /order niet gezien | Paden niet beschermd | Padherkenning |
| Spatie in code, verplaatste regel, verdwenen tweede `make test`, nieuwe code | Code vergeleken na witruimtenormalisatie en als verzameling | Letterlijke vergelijking met multipliciteit; CODE_ADDED bij herschrijven |
| Citaat "ja" naar "nee" niet gezien | Citaten pas vanaf twee woorden | Ook citaten van één woord |
| Lege output bij create gaf geen fout | Lege output alleen gecontroleerd met bron | EMPTY_OUTPUT ook zonder bron |

## Redactionele vergelijking

**Opzet.** Validatieset van 26 cases (9 Belgisch-Nederlandse of typisch Nederlandse taalgevallen), bevroren op 2026-10-08 vóór de runs. Vier condities: A eenvoudige redactieprompt zonder skill (`prompts/generator.md`), B v0.6.0, C kandidaat v0.7.0, D compacte variant (alleen SKILL.md en script). A, B en C drie runs, D één run. Elke run in een verse subagentcontext met alleen de takenmap en het skillpad. Generator: claude-opus-5-5 (door de agents zelf gerapporteerd), standaardinstellingen. Beoordelaar: een ander model (sonnet, Claude Code-subagent), geblindeerd met per case geschudde labels (seed 20261008 plus run), rubric in `prompts/beoordelaar.md`. Ruwe outputs in `runs/`, pakketten, sleutels en oordelen in `beoordeling/`, tokens en tijden in `runs-usage.csv`.

**Resultaat** (geslaagd = geen kritieke fout, inhoudsbehoud 3 en geen dimensie 0):

| Conditie | Geslaagd | Kritiek | Inhoud | Natuurlijk | Register/stem | Correct | Taak | Onnodig | Per run |
|---|---|---|---|---|---|---|---|---|---|
| A zonder skill | 53/78 | 2 | 2,64 | 2,90 | 2,86 | 3,00 | 3,00 | 2,87 | 17, 19, 17 van 26 |
| B v0.6.0 | 74/78 | 0 | 2,95 | 2,88 | 2,92 | 3,00 | 2,78 | 2,86 | 25, 24, 25 van 26 |
| C v0.7.0 | 75/78 | 0 | 2,96 | 2,87 | 2,96 | 2,99 | 2,86 | 2,96 | 23, 26, 26 van 26 |
| D compact | 25/26 | 0 | 2,96 | 2,92 | 2,96 | 3,00 | 2,92 | 3,00 | 25 van 26 |

**Interpretatie.**

- Beide skillversies scoren duidelijk beter dan geen skill op inhoudsbehoud (A: 25 van 78 niet geslaagd, twee kritieke fouten waarin "wordt verwerkt binnen 14 dagen" een terugbetaalbelofte werd).
- Tussen v0.6.0 en v0.7.0 is op deze set **geen aantoonbaar verschil in geslaagde cases** (74 tegen 75 van 78). Het verschil zit in onnodige wijzigingen (2,86 tegen 2,96: v0.6.0 voegt bij ongewijzigde tekst een toelichting toe), register (2,92 tegen 2,96) en taak (2,78 tegen 2,86). Met drie runs van 26 cases en één modelbeoordelaar is dat een verkennende bevinding, geen bewezen generalisatie.
- De compacte variant presteert in één run gelijkwaardig. De uitgebreide referenties zijn op deze set dus niet aantoonbaar nodig. Ze blijven omdat ze dekking geven voor gevallen die de validatieset weinig raakt (stemkalibratie, nl-BE, patronen); dit is een open vraag voor een volgende versie.
- Niet geslaagd bij C: V05 run 1 ("niet verwijderd, tenzij bevestigd" werd "alleen verwijderd als bevestigd"; logisch gelijkwaardig, de beoordelaar twijfelde), V06 run 1 ("zelf" toegevoegd bij "door de klant beschadigd"), V08 run 1 ("gebruikers" werd "iedereen"). Geen kritieke fouten.

**Eigen steekproef** van de beoordeling (V06, V22, V23, V24, V26 voor A, B, C run 1): oordelen van de beoordelaar herkenbaar en consistent. Beoordelaar run 2 gaf nul keer "kritiek"; dat kan mild zijn, maar de kritieke fouten in A run 1 en 3 zijn van hetzelfde type en in run 2 komt dat type niet voor.

## Reparatie na de evaluatie

De beoordeling vond bij C een onnodige toelichting bij een inkortopdracht (V20: "Weggevallen: alleen de inleidende formule"). Oorzaak: de opleveringsregel in SKILL.md. Reparatie: "Viel er iets inhoudelijks weg, noem dat in één regel; viel alleen opvulling weg, dan geen toelichting." Volgens het protocol is V20 naar de ontwikkelset verplaatst (case 43) en vervangen door V27.

Hertest met de gerepareerde kandidaat, drie runs: V20 3 van 3 zonder toelichting, V27 3 van 3 inhoudelijk volledig zonder toelichting. V27 met v0.6.0 (1 run) voegt de toelichting nog toe; zonder skill (1 run) niet. **Deze hertest is door de ontwikkelaar beoordeeld, niet geblindeerd.** V19 (samenvatting) in de hertest: twee van drie runs voegen "terwijl" toe, een tegenstelling die de bron niet maakt. Kleine nuancefout, niet gerepareerd om niet op de validatieset te tunen.

## Drift na een tweede bewerking

Tien herschrijfcases, run 1, opnieuw door dezelfde skillversie met "Humaniseer deze tekst." (`drift-v0.7.0.txt`):

| Versie | Gemiddelde tekengelijkenis | Ongewijzigd |
|---|---|---|
| v0.6.0 | 0,807 | 0 van 10 |
| v0.7.0 | 1,000 | 10 van 10 |

Eén run per versie; verkennend.

## Script over alle runs

`lint-runs-v0.7.0.txt` (definitief script, per run; V20 is uit de validatieset gehaald en V27 bestond nog niet tijdens deze runs, vandaar "ontbreekt: 1"): WARNING A 16-24, B 12-16, C 9-10, D 10; nergens ERROR. Een WARNING is een signaal, geen fout; dit getal is geen kwaliteitsmaat.

## Kosten

Gemiddeld per run van 26 cases: A 49.700 tokens en 161 s, B 76.500 tokens en 183 s, C 82.300 tokens en 231 s, D 68.500 tokens en 86 s (`runs-usage.csv`). De kandidaat kost ongeveer 8% meer tokens dan v0.6.0, vooral door het lezen van referenties en het draaien van het script.

## Beperkingen

- Generator en beoordelaar zijn taalmodellen van dezelfde leverancier. Een ander model als beoordelaar is geen garantie van onafhankelijkheid. Geen menselijke kalibratie.
- De validatieset is geschreven door dezelfde ontwikkelaar die de skill aanpaste; "nieuw" is niet "ongezien".
- Activatie en uploadcompatibiliteit zijn niet gemeten.
- Het script bewijst geen betekenisbehoud. Verwisselde waarden worden alleen als hint gemeld; voorwaarden via inversie ("Bent u het niet eens, dan ...") geven een vals-positief.

## Onafhankelijke diff-review

Een aparte reviewagent beoordeelde de wijziging tegen v0.6.0: 13 bevindingen (1 hoog, 8 middel, 4 laag).

- **Hoog, verwerkt**: inkorten sprak zichzelf tegen (`shorten` zonder feiten schrappen tegenover "noem wat wegviel" en "inkorten is een inhoudelijke bewerking"). Nu consequent: `shorten` schrapt geen inhoud en meldt niets; alleen `summarize` of uitdrukkelijk schrappen meldt wat wegviel.
- **Middel, verwerkt**: modaliteit en actor in voorbeeld-support, "wil" en "iedereen" in voorbeeld-zakelijk, intro en reikwijdte in voorbeeld-linkedin, eigen oordeel "erg onzeker" in patroon 9, verouderde verwijzingen in `bronnen.md`, het stdin-voorbeeld in SKILL.md (nu een heredoc in plaats van een bestand), en namen: een korte zin met gebiedende wijs ("Wacht 3 dagen.") gold als naam (opgelost, met regressietest).
- **Middel, toelichting**: `scripts/dhcheck/` staat nog niet in git; het moet in dezelfde commit mee. `skill.zip` en `bundle.sh` naast elkaar staan nu in de README.
- **Laag, grotendeels verwerkt**: helptekst van het script, melding bij toegevoegde code per taak, overgeslagen namencontrole in het rapport, strikte stijl en menupaden, kleine voorbeeldnuances. Bewust niet verwerkt: de regel over de dubbele punt staat zowel in SKILL.md als in patronen.md, omdat de opdracht die correctie expliciet vraagt en hij vaak nodig is.

Na de review: 85 van 85 tests, 26 van 26 probes, 14 WARNING in 10 van 42 cases op de echte ontwikkeloutputs (ongewijzigd).

Een herhaling van de volledige redactionele evaluatie na de review-wijzigingen is niet uitgevoerd (NOT_RUN). De wijzigingen betreffen voorbeelden, een opleveringsregel en de namenheuristiek; de opleveringsregel bij inkorten is apart hertest (zie boven).

## Packaging en platformchecks

- `dist/skill.zip` gemaakt met `package_skill.py` uit de skill-creator (Claude). SHA-256 `8a9443c336387c23ed4d44886ab615cd0219fe9431b8acdfa79776fd57d731d9`, 98 kB, 31 bestanden, één skillroot `dutch-humanizer/`, geen symlinks of onveilige paden. Manifest: `skill-zip-manifest.txt`.
- `bundle.sh` maakt hetzelfde pakket als `dist/dutch-humanizer.skill` (SHA-256 `f4d6039d5abdcb68c38968f0d997ba193303dd34c9db2a8a40a7b2728a270293`; andere hash door andere zip-metadata).
- Uitgepakt in een schone map: `quick_validate.py` (Codex skill-creator) PASS; 85 van 85 tests PASS; CLI via `--stdin` vanuit een andere map PASS; alle relatieve Markdown-links lossen op; `agents/openai.yaml` geldig volgens het schema van de Codex skill-creator.
- Netwerk: het script bevat geen netwerk-, subprocess- of exec-code (gecontroleerd met grep). Een run met netwerk uitgeschakeld is niet uitgevoerd (NOT_RUN).
- Uitgesloten uit het pakket: `evals/`, caches, ruwe runs, testsets en `tmp/`.
- Upload naar claude.ai of ChatGPT: NOT_RUN.
