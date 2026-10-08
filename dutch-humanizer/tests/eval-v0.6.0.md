# Evaluatieverslag v0.6.0

Datum: 2026-10-08. Skillversie: 0.6.0 (werkversie, voor de laatste correcties hieronder).

**Opzet.** Drie subagents (Claude, via Claude Code) voerden de skill uit op de 42 cases in `fixtures/semantische-cases.md`. Ze kregen alleen Verzoek en Input. Een vierde agent van hetzelfde model scoorde de outputs met de rubric uit `evaluation.md`. Daarnaast draaide `scripts/check.py` op elke output.

**Beperkingen.** Uitvoerder en beoordelaar zijn hetzelfde model; er is geen menselijke beoordeling. Elke case is één keer gedraaid. De scores zijn een indicatie, geen meting.

## Resultaat eerste ronde

- Geslaagd: **40 van 42**.
- Gemiddelden: trouw 2,95; natuurlijkheid 2,93; register 2,98; stem 1,5 (n=2); grammatica 3,00; formulepatronen 2,88; techniek 3,00; onnodige wijzigingen 2,95.
- `check.py`: 0 ERROR, 15 WARNING over 42 outputs. Na handmatige controle bleken alle WARNINGs gelijkwaardige formuleringen ("naar verwachting" werd "we verwachten", "dient" werd de gebiedende wijs, "behalve" werd "de enige uitzondering"). Twee daarvan ("vermoedelijke", synoniemen voor voorwaarden en verplichtingen) zijn daarna in het script opgelost.

### Mislukt

| Case | Probleem | Oorzaak | Correctie |
|---|---|---|---|
| 07 | "Het gaat niet om de cijfers, het gaat om de mensen" werd een oorzaak van de groei | Het vage-inputvoorbeeld in `voorbeeld-linkedin.md` deed precies dat | Voorbeeld gecorrigeerd |
| 12 | Het expliciete "daarom" en de afgewezen optie verdwenen | Het modelvoorbeeld in `principes.md` (geval A) en patroon 5 liet "daarom" ook vallen | Beide voorbeelden gecorrigeerd |

### Overige verbeterpunten uit de beoordeling

- Stem (06): correct zonder lekkage, maar weinig van de droge toon van de schrijver. Werkwijzestap 5 in `stem-kalibratie.md` is aangescherpt.
- Resten opvulling in 04, 05, 11, 22, 32 ("flinke impact", "belangrijke mijlpaal", "het is essentieel dat"). Dit is de prijs van strikt betekenisbehoud: een oordeel van de schrijver blijft, in gewonere woorden.
- 10: de input sprak Karin aan met u in een vulzin; de output vermijdt de aanspreekvorm. Inhoudelijk correct, register scoort 2.

### Onduidelijkheden die de uitvoerders meldden, en wat ermee gedaan is

Toegevoegd aan `SKILL.md`: oplevering als de tekst al goed was; meerdere `Let op:`-punten; placeholder `[naam?]`; verzoeken die nieuwe feiten vragen ("maak concreter"); u en je bij "minder formeel"; onpersoonlijke tekst; aanhef in chat; formele brieven; opmaak van mails op één regel; afbakenende aanhalingstekens; notatie van tijden; welke tekst naar `check.py` gaat en `--source-lang other` bij vertalingen; wanneer een WARNING mag blijven staan. In de referenties: functionele en decoratieve emoji, labels in lijsten, evaluatieve woorden, cliché-openers, "gelieve" in informele Belgische tekst, stemvoorbeelden boven de registertabel.

## Herhaling na correcties (cases 06, 07, 10, 12)

| Case | Uitkomst |
|---|---|
| 06 | Iets meer stem ("Voor werknemers en voor werkgevers." als los fragment, zoals de schrijver); geen lekkage. |
| 07 | Geslaagd: "Waar het ons om gaat: de mensen, niet de cijfers." Alle drie oorzaken en de vraag blijven. |
| 10 | Ongewijzigd: inhoud correct, geen aanspreekvorm. |
| 12 | Geslaagd: afgewezen optie, gevolg en "daarom" behouden. |

Kanttekening: de outputs van 07 en 12 lijken sterk op de gecorrigeerde voorbeelden in de referenties. Deze twee cases toetsen daardoor vooral of de agent de voorbeelden volgt, niet of hij generaliseert. Voor een zuivere meting: varieer de input van deze cases.

## Scores per case (eerste ronde)

| Case | Trouw | Natuurlijk | Register | Stem | Grammatica | Patronen | Techniek | Onnodig | Geslaagd | Opmerking |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Ongewijzigd, correct voor N-case. |
| 02 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 2 | ja | Alle voorbehouden intact ("mogelijk", "misschien", "volgens Joost"). "nadrukkelijk" naar "uitdrukkelijk" is een overbodige ingreep. |
| 03 | 3 | 2 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | u, "lijkt", 10 werkdagen intact. "Dank voor uw bericht en uw geduld, en vervelend dat u hiermee te maken hebt" loopt stroef. |
| 04 | 3 | 3 | 3 | n.v.t. | 3 | 2 | 3 | 3 | ja | nl-BE behouden (gelieve, schepen, gsm, kan u). Restje opvulling: "een belangrijke wijziging, met een flinke impact op het schoolleven". |
| 05 | 3 | 3 | 3 | n.v.t. | 3 | 2 | 3 | 3 | ja | Citaat, vlag, URL, 9-17, datum letterlijk; nuttige Let op over datum. Restje "belangrijke mijlpaal". |
| 06 | 3 | 3 | 3 | 1 | 3 | 3 | 3 | 3 | ja | Geen lekkage uit voorbeeld, maar stem generiek: geen droge, korte toon van het voorbeeld. |
| 07 | 2 | 2 | 3 | n.v.t. | 3 | 3 | 3 | 3 | nee | Betekenis verschoven: "Het gaat niet om de cijfers, het gaat om de mensen" werd "dat danken we aan de mensen, niet aan de cijfers" (waardeuitspraak wordt oorzaak van groei, en "danken aan de cijfers" is onlogisch). |
| 08 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Geen valse vrienden; "niet alleen om tooling, maar vooral om cultuur" houdt de weging. |
| 09 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Feiten en oorzaak intact, niets verzonnen. |
| 10 | 3 | 3 | 2 | n.v.t. | 3 | 3 | 3 | 3 | ja | "tenzij", 1 december, "minstens twee weken" intact. Aanspreekvorm u verdwenen (geen je, wel neutraal). |
| 11 | 3 | 3 | 3 | n.v.t. | 3 | 2 | 3 | 3 | ja | Vier criteria letterlijk. "eenvoudig en efficiënt" blijft vage tweeslag. |
| 12 | 2 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | nee | Afweging omgegooid: "Een mogelijke oplossing is ... maar ... De vernieuwing gebeurt daarom zonder herstart" werd "Een herstart via een cronjob zou alle actieve sessies laten wegvallen." Het expliciete "daarom" en de framing als overwogen optie zijn weg. |
| 13 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Tijden, "vermoedelijke oorzaak", Team Platform, uiterlijk 14 maart intact. |
| 14 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Bron vervoerder, voorwaarde en toezegging intact. |
| 15 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Termijn, ondertekening, vier onderdelen en "ten minste" intact; verplichting via gebiedende wijs. |
| 16 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | "mits" naar "als jij dan nog tijd hebt": voorwaarde blijft. |
| 17 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | 73% en toeschrijving intact, Let op over bron. ("tonen aan" naar "volgens" is minimaal zwakker, binnen marge.) |
| 18 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | "zodra" Compliance en "verwachten" week 42 intact. |
| 19 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | "lijkt" behouden. |
| 20 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | uiterlijk vrijdag 17.00 uur, u. |
| 21 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | "binnen 30 dagen nadat u de factuur hebt ontvangen" correct. |
| 22 | 3 | 3 | 3 | n.v.t. | 3 | 2 | 3 | 3 | ja | Actoren en volgorde goed. Restje "Het is essentieel dat". |
| 23 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Uitzondering en "na 1 maart" intact. |
| 24 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Jargon en voorwaarde intact. |
| 25 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Vier punten met inhoud intact; vette labels weg (verdedigbaar). |
| 26 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Bronnen gescheiden, "Toch" voor "desondanks". |
| 27 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Verbod met "niet voordat", 02:00 UTC, "maximaal drie keer". |
| 28 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Idiomatisch, geen valse vrienden. |
| 29 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Verwijzing expliciet gemaakt ("Voor medewerkers in de nachtdienst"), "wel al" behouden. |
| 30 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Ongewijzigd. |
| 31 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Ongewijzigd, nl-BE behouden. |
| 32 | 3 | 3 | 3 | n.v.t. | 3 | 2 | 3 | 3 | ja | Feit intact, niets toegevoegd. "De digitale wereld verandert snel" blijft openingscliché ondanks "volledig". |
| 33 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Ongewijzigd, contrast behouden. |
| 34 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Citaat letterlijk, "waaronder" behouden. |
| 35 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | je-vorm, geen verzonnen ervaring. Persoonlijk maar zuinig. |
| 36 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Niets verzonnen, Let op vraagt bron en cijfers. |
| 37 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Formeel, u, alle feiten en ondertekening intact. |
| 38 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Alle cijfers exact; "boven de doelstelling" met cijfers erbij. |
| 39 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | "waarschijnlijk" en verplichting ("moeten") intact. |
| 40 | 3 | 2 | 3 | n.v.t. | 3 | 3 | 3 | 3 | ja | Geen verzonnen details; Let op over weekdag klopt (14-10-2026 is woensdag). "U wilt die eerst intern bespreken." klinkt bot. |
| 41 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | ja | Kort en droog, geen lekkage, geen verzonnen reden. Stem neutraal-kort, weinig eigen. |
| 42 | 3 | 3 | 3 | n.v.t. | 3 | 3 | 3 | 2 | ja | Emoji en toon behouden. "starten" naar "beginnen" overbodig. |
