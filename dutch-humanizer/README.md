# Dutch Humanizer

Een agent-skill die Nederlandse tekst natuurlijk en passend maakt zonder de inhoud te veranderen. De skill redigeert, schrijft of vertaalt naar natuurlijk Nederlands, in nl-NL of nl-BE, desgewenst in de stem van de schrijver.

Kernprincipe: **betekenis gaat voor stijl.** De skill is een redacteur, geen samenvatter. Feiten, cijfers, voorwaarden, ontkenningen, zekerheid, bronnen, termijnen, vaktermen en de communicatieve handeling (voorstel, vraag, verwachting) blijven gelijk. Een goede tekst ongewijzigd laten is een geldige uitkomst.

Versie: 0.7.0. Zie [CHANGELOG.md](CHANGELOG.md).

## Installatie

**Claude Code**: plaats of symlink de map in je skills-map.

```bash
ln -s /pad/naar/claude-skills/dutch-humanizer ~/.claude/skills/dutch-humanizer
```

**Claude.ai of ChatGPT**: upload `skill.zip` als skill in de instellingen. Het pakket bevat één skillmap. In de repository maakt `bundle.sh` hetzelfde pakket als `dist/dutch-humanizer.skill`; dat is een ZIP met dezelfde inhoud.

**Codex en andere agents**: kopieer de map naar de skills-map van de agent. `agents/openai.yaml` bevat de weergavenaam en een standaardprompt voor OpenAI-producten; andere platforms negeren dat bestand.

Normaal gebruik werkt zonder netwerk en zonder extra account. Het controlescript gebruikt alleen de Python-standaardbibliotheek (Python 3.9 of nieuwer; getest met 3.9.6 en 3.14.8).

## Gebruik

```text
Humaniseer deze tekst: ...
Maak dit minder AI-achtig, maar verander de inhoud niet: ...
Herschrijf dit in mijn eigen stijl. Voorbeelden van mij: ...
Make this sound like natural Dutch: ...
```

De skill bepaalt taak (`rewrite`, `create`, `translate`, `shorten`, `summarize`), register, locale en intensiteit, en vraagt alleen wat niet af te leiden is. Inkorten is geen toestemming om feiten te schrappen; samenvatten gebeurt alleen op uitdrukkelijk verzoek.

- **Licht** (standaard): gerichte ingrepen; structuur, volgorde en lengte blijven grotendeels gelijk.
- **Volledig**: opbouw en zinsbouw mogen veranderen, ook van lijst naar lopende tekst. Alle inhoud blijft.
- **Stem**: één of meer eigen teksten of een stijlgids. Expliciete voorkeuren gaan voor afgeleide kenmerken; feiten en privédetails uit voorbeelden komen niet in de output.
- **Strikte huisstijl**: geen em- of en-dashes, emoji of pijlen, rechte aanhalingstekens. Op verzoek; standaard zijn deze tekens afhankelijk van context.

## Controlescript

De skill controleert na elke bewerking de inhoud in twee richtingen. Kan de agent code uitvoeren, dan draait hij ook `scripts/check.py`. Het script zoekt in de skillmap, niet in de werkmap van de gebruiker, en heeft geen tekstbestanden in het project nodig:

```bash
python3 <skillmap>/scripts/check.py --stdin --task rewrite < bericht.json   # {"source": "...", "output": "..."}
python3 <skillmap>/scripts/check.py output.txt --input bron.txt             # oude aanroep werkt nog
```

| Optie | Betekenis |
|---|---|
| `--task` | `rewrite` (standaard met bron), `create` (standaard zonder bron), `translate`, `shorten`, `summarize` |
| `--style strict`, `--allow-dashes` | Strikte huisstijl: elk verboden teken in bewerkbare tekst is ERROR; citaten en code tellen niet mee |
| `--source-lang auto\|nl\|other` | Brontaal; bij Engels worden signaalwoorden over de talen heen vergeleken |
| `--source-locale`, `--target-locale` | Getalnotatie, bijvoorbeeld `en-US` naar `nl-NL`; `auto` laat "1.234" dubbelzinnig |
| `--format json` | Machineleesbaar: `schema_version`, regelcodes, ernst, bron- en outputposities, uitgevoerde en overgeslagen controles |
| `--fail-on-warning` | Exit 1 ook bij WARNING |

Wat het script controleert:

- **Letterlijke inhoud**: fenced en ingesprongen code, inline code, citaten (ook van één woord), linkdoelen, URL's, e-mailadressen, API- en bestandspaden, versienummers en frontmatter. Zonder normalisatie van witruimte of hoofdletters, met multipliciteit en volgorde.
- **Hoeveelheden**: waarden met `Decimal` volgens de locale; teken, precisie, eenheid (hoofdlettergevoelig: MB is niet Mb), procent tegenover procentpunt, werkdag tegenover kalenderdag, begrenzing (maximaal, minimaal), aantal voorkomens, en een hint als een waarde bij een andere zaak lijkt te staan.
- **Datums, tijden en weekdagen**, ook in Engelse notatie.
- **Signaalwoorden** in families: ontkenning, verplichting ("moet", "moet ... niet", "hoeft ... niet"), verbod, toestemming, mogelijkheid, onzekerheid (aanwijzing tegenover inschatting), voorwaarde en uitzondering ("mits", "tenzij", "zodra"), termijn en volgorde. Woorden binnen één familie mogen wisselen; een verschuiving tussen families geeft altijd een WARNING.

| Niveau | Betekenis |
|---|---|
| `ERROR` | Vastgestelde schending: gewijzigde of toegevoegde code bij herschrijven, gewijzigde frontmatter, lege output, verboden teken bij `--style strict` |
| `WARNING` | Mogelijke betekenisverandering; lees de zin en beslis |
| `INFO` | Stijlobservatie of overgeslagen controle |

Exitcodes: `0` geen ERROR, `1` ERROR (of WARNING met `--fail-on-warning`), `2` gebruiksfout. Nul meldingen betekent niet dat de betekenis klopt.

## Lokaal testen

```bash
cd dutch-humanizer
python3 -m unittest discover -s tests -v
```

De tests in het pakket dekken het controlescript: de regressies uit de opdracht, randgevallen, een set correcte parafrases (vals-positieven), perturbaties met een vaste seed en de CLI. De redactionele evaluatie (testsets, beoordelingen, ruwe runs) staat in de repository onder `evals/dutch-humanizer/`, niet in het pakket. Het pakket bouw je met `bundle.sh` in de repository; dat script hoort niet bij de skill.

## Bekende beperkingen

- **Betekenis is niet mechanisch te bewijzen.** Het script vergelijkt tekens, getallen, beschermde fragmenten en signaalwoorden. Een parafrase met dezelfde betekenis kan een WARNING geven (bijvoorbeeld een voorwaarde via inversie: "Bent u het niet eens, dan ..."); een andere betekenis met dezelfde woorden geeft er geen. Verwisselde waarden worden alleen als hint gemeld.
- **Markdown**: begrensde scanner, geen volledige CommonMark-parser. Code in blockquotes en diep geneste lijsten wordt niet herkend.
- **Taal**: signaalwoorden alleen voor Nederlands en Engels; bij andere brontalen overgeslagen. "Als" en "wanneer" tellen niet mee als voorwaarde.
- **Namen**: herkenning aan hoofdletters buiten zinsbegin.
- **Privacy**: de standaardwerkwijze gebruikt stdin of een tijdelijke map buiten het project. Opruimen is geen gegarandeerd veilig wissen, en het platform kan zelf loggen.
- **Evaluatie**: beoordeeld door taalmodellen, niet door mensen; activatie (wanneer de skill geladen wordt) is niet gemeten. Zie `evals/dutch-humanizer/rapport-v0.7.0.md` in de repository.
- **Locale**: de nl-BE-lijst is niet volledig.
