# Dutch Humanizer

Een agent-skill die Nederlandse tekst natuurlijk en passend maakt zonder de inhoud te veranderen. De skill redigeert, schrijft of vertaalt naar natuurlijk Nederlands, in nl-NL of nl-BE, desgewenst in de stem van de schrijver.

Kernprincipe: **betekenis gaat voor stijl.** De skill is een redacteur, geen samenvatter. Feiten, cijfers, voorwaarden, ontkenningen, zekerheid, bronnen, termijnen en vaktermen blijven gelijk.

Versie: 0.6.0. Zie [CHANGELOG.md](CHANGELOG.md).

## Installatie

**Claude Code**: plaats of symlink de map in je skills-map.

```bash
ln -s /pad/naar/claude-skills/dutch-humanizer ~/.claude/skills/dutch-humanizer
```

**Claude.ai of ChatGPT**: upload `skill.zip` (gemaakt met `bundle.sh` in de repository, of zie *Pakket maken*) als skill in de instellingen.

**Codex en andere agents**: kopieer de map naar de skills-map van de agent. `agents/openai.yaml` bevat de weergavenaam en een standaardprompt.

## Gebruik

Vraag in gewone taal:

```text
Humaniseer deze tekst: ...
Maak dit minder AI-achtig, maar verander de inhoud niet: ...
Herschrijf dit in mijn eigen stijl. Voorbeelden van mij: ...
Make this sound like natural Dutch: ...
```

De skill bepaalt zelf taak (herschrijven, opstellen, vertalen), register, locale en intensiteit, en vraagt alleen wat niet af te leiden is.

### Licht redigeren of volledig herschrijven

- **Licht** (standaard): gerichte ingrepen; structuur, volgorde en lengte blijven grotendeels gelijk. Goede tekst blijft staan.
- **Volledig**: opbouw en zinsbouw mogen veranderen. Vraag erom ("herschrijf dit volledig") of de skill kiest het bij tekst die met losse ingrepen niet te redden is. Ook dan blijft alle inhoud.

Wil je echt korter, vraag dan om inkorten of samenvatten. De skill meldt wat er inhoudelijk wegvalt.

### Stemkalibratie

Geef één of meer eigen teksten mee, eventueel uit verschillende kanalen, of een stijlgids. De skill haalt de vaste kenmerken van je stem eruit (woordkeus, ritme, directheid) en past het register aan het kanaal aan. Feiten uit je voorbeelden komen nooit in de output.

### Voorkeuren

Gedachtestreepjes, emoji en pijlen zijn standaard afhankelijk van context: de skill neemt ze over waar ze functioneel zijn en voegt zelf geen decoratie toe. Vraag om de **strikte huisstijl** voor de regel van eerdere versies: geen em- of en-dashes, emoji of pijlen, en rechte aanhalingstekens.

## Validatie

De skill doet na elke bewerking een verplichte semantische zelfcontrole (twaalf dimensies, zie `SKILL.md`). Kan de agent code uitvoeren, dan draait hij daarnaast:

```bash
python3 scripts/check.py output.txt --input input.txt [--style strict] [--allow-dashes] [--source-lang auto|nl|other] [--fail-on-warning]
```

| Niveau | Betekenis |
|---|---|
| `ERROR` | Zekere mechanische fout: gewijzigde of verdwenen code, gewijzigde frontmatter, lege output, verboden teken bij `--style strict`. |
| `WARNING` | Mogelijke betekenisverandering: getal, percentage, datum, tijd, URL, e-mailadres of naam verdwenen of nieuw; een citaat niet letterlijk teruggevonden; ontkenning, voorwaarde, onzekerheid, verplichting of termijnwoord verdwenen. Controleer de passage. |
| `INFO` | Stijlopmerking: nieuwe streepjes of emoji, Title Case, hoofdletter na dubbele punt, veel kortere output. |

Exitcodes: `0` geen ERROR, `1` ERROR (of WARNING met `--fail-on-warning`), `2` gebruiksfout.

Sinds v0.6.0 zijn nieuwe streepjes, emoji, pijlen en gekrulde aanhalingstekens standaard `INFO`. Gebruik `--style strict` voor het oude gedrag waarin ze een fout waren.

## Lokaal testen

```bash
cd dutch-humanizer
python3 -m unittest discover -s tests -v
```

De unittests dekken het controlescript. De redactionele kwaliteit test je met de 42 cases in `tests/fixtures/semantische-cases.md` en de rubric in `tests/evaluation.md`; daarvoor is een model nodig.

## Pakket maken

Vanuit de repository:

```bash
./bundle.sh dutch-humanizer
```

## Bekende beperkingen

- **Betekenis is niet mechanisch te bewijzen.** Het script vergelijkt tekens, getallen en signaalwoorden. Een herschrijving kan dezelfde betekenis hebben met andere woorden (geen WARNING nodig, toch een WARNING), of een andere betekenis met dezelfde woorden (geen WARNING). De semantische zelfcontrole van het model blijft leidend.
- **Vertalingen**: bij een niet-Nederlandse bron slaat het script de woordgebonden controles over; getallen, datums en code vergelijkt het wel.
- **Namen**: het script herkent namen aan hoofdletters buiten zinsbegin. Een naam aan het begin van een zin ziet het niet; een gewoon woord met hoofdletter kan als naam worden gemeld.
- **Getallen in woorden** herkent het script alleen voor veelvoorkomende telwoorden.
- **Evaluatie**: de cases zijn beoordeeld door een model, niet door menselijke beoordelaars. De scores zijn een indicatie, geen meting.
- **Locale**: de nl-BE-lijst is niet volledig; laat Belgische tekst bij twijfel door een Belgische lezer controleren.
