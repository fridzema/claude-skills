# Changelog dutch-humanizer

Alle noemenswaardige wijzigingen aan deze skill. Formaat volgens [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versies volgens [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] — 2026-10-08

Betrouwbaarheidsronde op basis van de opdracht v0.7.0. Alle 22 gemelde fouten in het controlescript zijn gereproduceerd en opgelost; het redactionele contract is aangescherpt; de evaluatie is voor het eerst tegen een baseline en zonder skill uitgevoerd. Volledig rapport: `evals/dutch-humanizer/rapport-v0.7.0.md` in de repository.

### Gerepareerd (controlescript)

- **Getallen**: `Decimal` uit de tekens volgens locale in plaats van cijfers aan elkaar plakken. 1,5% naar 15%, 415% naar 41,5% en -5 naar 5 worden nu gezien; 0,040 naar 0,04 is een precisiewijziging, geen andere waarde.
- **Eenheden**: hoofdlettergevoelig (MB tegenover Mb); verdwenen en toegevoegde eenheden; procent tegenover procentpunt, werkdag tegenover kalenderdag; begrenzing (maximaal, minimaal, meer dan).
- **Notatie**: `--source-locale` en `--target-locale`; bij een onbekende locale blijft "1.234" dubbelzinnig en volgt QTY_AMBIGUOUS.
- **Aantallen**: multipliciteit voor getallen, datums, code, citaten, URL's en paden; tweemaal 21% naar eenmaal wordt gezien.
- **Letterlijke inhoud**: code zonder witruimtenormalisatie (spaties in strings, inspringing); verdwenen, gewijzigde en toegevoegde code; citaten van één woord; API- en bestandspaden; versienummers.
- **Signaalwoorden**: gelijkwaardigheidsgroepen verwijderd. "Tenzij" naar "mits" en "moet" naar "verboden" heten niet langer "meestal gelijkwaardig". Families per betekenis (ontkenning, verplichting, "moet ... niet", "hoeft ... niet", verbod, toestemming, mogelijkheid, onzekerheid als aanwijzing of inschatting, voorwaarde, uitzondering, termijn), toevoegingen en verwijderingen in beide richtingen.
- **Lege output** bij `create` geeft ERROR; een lege bron is expliciet gedefinieerd.
- **Strikte stijl** controleert alle bewerkbare output, niet alleen nieuwe tekens; citaten en code blijven uitgezonderd.

### Toegevoegd

- `scripts/dhcheck/`: pure in-memory kern (`analyze`) met modules voor Markdown-spans, hoeveelheden en signalen; `check.py` is de CLI-adapter. Oude aanroep en vlaggen werken nog.
- `--format json` (schema_version 1, stabiele regelcodes, bron- en outputposities, uitgevoerde en overgeslagen controles), `--stdin` (geen tekstbestanden nodig), `--task` (rewrite, create, translate, shorten, summarize).
- Begrensde Markdown-scanner volgens CommonMark: ongesloten fences, backtickreeksen van verschillende lengte, geneste linkhaken, escapes, afbakenende aanhalingstekens rond de hele input, apostrofs.
- Tests: 85 (was 50), waaronder 26 regressies uit de opdracht, 32 correcte parafrases voor vals-positieven, perturbaties met vaste seed, randgevallen, grote input en CLI vanuit een andere map.

### Gewijzigd (skill)

- **Taken** `shorten` (inkorten zonder feiten te schrappen) en `summarize` (alleen op uitdrukkelijk verzoek) naast `rewrite`, `create`, `translate`.
- **Communicatieve handelingen** beschermd: voorstel, vraag, verwachting en excuus blijven wat ze zijn. Een stijlopdracht voegt geen verplichting of belofte toe. Onbewezen bronbeweringen blijven beweringen.
- **Werkwijze**: contract, inventaris, gerichte redactie, mechanische controle, inhoudelijke controle in twee richtingen, hooguit twee herstelrondes, en ook de laatste tekst opnieuw controleren.
- **Opleveren**: ook bij ongewijzigde tekst alleen de tekst, zonder toelichting. Bij `shorten` geen toelichting; bij `summarize` of uitdrukkelijk schrappen één regel over wat wegviel.
- **Privacy**: het script via de skillmap aanroepen, tekst via stdin of een tijdelijke map buiten het project.
- **Dubbele punt**: volgens Taaladvies een kleine letter na een verklaring, ook bij een volledige zin; hoofdletter bij citaat, eigennaam en opsomming van volledige zinnen.
- **"Het lijkt erop"** is een aanwijzing en wordt niet "waarschijnlijk"; "zodra" wordt niet "na".
- **Voorbeelden**: 66 voor/na-paren in twee richtingen geaudit (9 kritieke en ongeveer 37 kleine bevindingen, verwerkt; auditlog in de repository). Onder meer: geen nieuw causaal verband in de LinkedIn-post, "in 3 dagen" in plaats van "in 3", "roteren" blijft roteren, het essay behoudt elke bewering. Nieuwe voorbeelden van bewust laten staan.
- **Generalisaties verwijderd**: "Zakelijk Nederlands is van nature direct", "Nederlands volgt vaker dan Amerikaans-Engels ...", "AI-tekst maakt er ... van".
- `references/bronnen.md`: regeltabel met type, bron, uitzondering, controledatum en gekoppelde test.
- `SKILL.md` korter: 1.757 woorden (was 1.879).

### Verplaatst

- De 42 ontwikkelcases, de rubric en het evaluatieverslag van v0.6.0 staan nu in `evals/dutch-humanizer/` in de repository, niet meer in het skillpakket. Het pakket bevat alleen de tests van het meegeleverde script.

### Evaluatie

Op 26 bevroren validatiecases, drie runs, geblindeerd beoordeeld door een ander model: zonder skill 53 van 78 geslaagd (2 kritiek), v0.6.0 74 van 78, v0.7.0 75 van 78 (geen kritiek). Tussen v0.6.0 en v0.7.0 is het aantal geslaagde cases niet aantoonbaar verschillend; v0.7.0 maakt minder onnodige wijzigingen en laat bij een tweede bewerking de eigen tekst ongewijzigd (10 van 10, tegen 0 van 10). Activatie en menselijke beoordeling: niet uitgevoerd.

## [0.6.0] — 2026-10-08

Semantische gelijkwaardigheid is nu de hoogste redactionele prioriteit. De skill is een redacteur, geen samenvatter: een patroon weghalen mag nooit informatie, voorwaarden, zekerheid of technische precisie kosten.

### Semantische veiligheid

- **Onveilige uitzondering verwijderd.** v0.5.0 liet een verloren bewering toe "tenzij een patroon het schrappen vraagt". Geen enkel patroon gaat nog voor betekenisbehoud.
- **Invarianten vooraf vastleggen** (werkwijzestap 2): feiten, getallen, eenheden, bronnen, actoren, voorwaarden, uitzonderingen, ontkenningen, toezeggingen, termijnen, zekerheid, oorzaak, vergelijking, rangorde, volgorde, vaktermen, code en elk afzonderlijk punt.
- **Verplichte semantische zelfcontrole** op twaalf dimensies, met herstellen en opnieuw controleren voor het opleveren.
- **`principes.md` deel 1: betekenis behouden**, met wat nooit mag en zes uitgewerkte gevallen (technische afweging, percentage en bron, voorwaarde, zekerheid, termijn, binnen tegenover na).
- **Voorbeelden die betekenis verloren gecorrigeerd**: de cronjob-afweging (patroon 5), "73%" dat "veel bedrijven" werd (patroon 18), bewijs over mislukte imports (patroon 35), drie LinkedIn-maatregelen die er twee werden, "en meer" dat verdween (patroon 24), de kennisgrens-gok die werd geschrapt (patroon 34), oordelen die verdwenen in patroon 2, 16, 17 en 21, de Slack-prioriteit en "vooral bij de betaalstap", de klantenservice-zin "komt vaker voor", en het essay dat de helft van de beweringen liet vallen.

### Natuurlijk Nederlands

- **Twee intensiteiten**: licht redigeren (standaard) en volledig herschrijven. Natuurlijk betekent niet vanzelf korter of informeler; lengte blijft ongeveer gelijk.
- **Voorkeuren in plaats van verboden**: gedachtestreepjes, emoji en pijlen zijn afhankelijk van context. De strikte huisstijl van eerdere versies is op verzoek beschikbaar (`--style strict`).
- **Hoofdletter na dubbele punt** gecorrigeerd: kleine letter is gebruikelijk; citaat en eigennaam krijgen een hoofdletter, bij een zelfstandige zin komen beide voor.
- Spelling en grammatica (normen) staan nu los van typografische voorkeuren.

### Patronen

- Drie soorten: sterk signaal, zwak signaal, legitieme constructie. Ook een sterk signaal vraagt een oordeel in context.
- Elk patroon heeft nu *Waarom het kan storen*, *Passend als*, *Herschrijf als* en *Bewaak*.
- Nieuwe sectie G met legitieme constructies (niet X maar Y, retorische vraag, korte zin, herhaling, drietal, passief, jargon, nadruk, opmaak, Engelse termen, marketing- en zakelijke taal).
- Claims over herkomst verwijderd, waaronder "tekst van voor 30 november 2022 is niet door een chatbot geschreven" en "mensen herkennen AI nauwelijks beter dan gokken".

### Stem

- Meerdere schrijfvoorbeelden, voorbeelden uit verschillende kanalen, expliciete voorkeuren en stijlgidsen.
- Onderscheid tussen vaste stem (woordkeus, ritme, directheid, humor) en register per context.
- Waarborgen: geen feiten of ervaringen uit voorbeelden, geen fouten overnemen, geen karikatuur, geen eerdere voorbeelden zonder toestemming, helderheid voor in technische en veiligheidskritische tekst.

### Validatie

- **`scripts/check.py` herschreven** met offset-bewuste maskering: fenced code (``` en ~~~), ingesprongen code, inline code, Markdown-links, URL's, e-mail, escapes, YAML-frontmatter en citaten. Regelnummers blijven kloppen.
- **Niveaus ERROR, WARNING, INFO** en gedocumenteerde exitcodes (0, 1, 2). Nieuw: `--style`, `--source-lang`, `--fail-on-warning`. `--allow-dashes` en de oude aanroep werken nog.
- **Nieuwe signalen**: verdwenen of nieuwe getallen, gewijzigde percentages, datums, tijden en weekdagen (ook Engelse notatie), eenheden en valuta, URL's, e-mailadressen, namen, gewijzigde code of frontmatter, niet letterlijk overgenomen citaten, en verdwenen ontkenningen, voorwaarden, onzekerheid, verplichtingen en termijnwoorden (zoals "binnen" dat "na" wordt).
- **Gedragswijziging**: nieuwe streepjes, emoji, pijlen en gekrulde aanhalingstekens zijn standaard INFO in plaats van fout. Gebruik `--style strict` voor het oude gedrag. Meldingen beginnen met `ERROR`, `WARNING` of `INFO` in plaats van `FOUT` en `LET OP`.

### Tests

- `tests/test_check.py`: 50 unittests voor het controlescript (standaardbibliotheek).
- `tests/fixtures/semantische-cases.md`: 42 redactionele cases, waaronder negatieve voorbeelden, nl-BE, vertalingen, Jira, incident, formele brieven en meerdere schrijfvoorbeelden.
- `tests/evaluation.md`: rubric (acht dimensies, 0 tot 3), procedure, en wat wel en niet automatisch te testen is.
- `tests/eval-v0.6.0.md`: evaluatieronde met drie uitvoerende agents en een beoordelende agent (hetzelfde model, geen menselijke beoordeling). 40 van 42 cases geslaagd; beide mislukte cases kwamen door fouten in referentievoorbeelden, die zijn gecorrigeerd en opnieuw getest.

### Pakket

- Frontmatter bevat alleen `name` en `description`; versiegeschiedenis staat in dit bestand.
- Nieuw in de skillmap: `LICENSE`, `README.md`, `CHANGELOG.md`, `agents/openai.yaml`, `tests/`.
- Description beschrijft taak, triggers en het behoud van betekenis, en sluit gewone schrijfverzoeken en een losse spellingcontrole uit.
- `SKILL.md` groeit van ongeveer 1200 naar 1900 woorden, door de verplichte zelfcontrole, de registerregels en de opleveringsgevallen. Uitleg, gevallen en voorbeelden staan in de referenties en worden alleen geladen als de taak erom vraagt.

## [0.5.0] — 2026-10-08 (niet apart uitgebracht, onderdeel van release 0.6.0)

Correctheidsronde voor `dutch-humanizer`, op basis van twee statische reviews en de wijzigingen in upstream [blader/humanizer](https://github.com/blader/humanizer) v2.6 tot v3.1. Hoofdpunt: de voorbeelden verzonnen feiten, precies wat de skill verbiedt. Drie daarvan kwamen uit upstream v2.5 en waren daar in v2.9.0 (#187) al gerepareerd.

### Fixed

- **Verzonnen feiten in voorbeelden verwijderd.** Onder meer: endpoint en supportadres in docs-variant A, "donderdag", Q3-opties en "volgende sprint" in zakelijk-variant A, het hele oorzaakverhaal in LinkedIn-variant A, de afzender "Sanne" (support), het tijdstip 14:30 (Slack), het GitHub-cijfer en de eigen ervaring (essay), en circa tien Na-voorbeelden in `patronen.md` en twee in `principes.md`. Elke Voor bevat nu zelf de feiten; de Na gebruikt alleen die. De A/B-varianten zijn vervangen door één voorbeeld plus een korte "als de input vaag is"-sectie.
- **Betekenisverschuivingen in voorbeelden**: "het lijkt erop dat" werd een vaststaand feit, u werd je, "mogelijk" werd "waarschijnlijk", een drietal verloor een inhoudelijk punt alleen voor het ritme.
- **Regel voor gekrulde aanhalingstekens toonde rechte aanhalingstekens** als verboden tekens. Nu met codepoints, inclusief het lage aanhalingsteken (U+201E).
- **Tegenstrijdige regels**: huisstijl tegenover citaten, emoji in chat, schrijfvoorbeeld tegenover streepjesverbod, datumnotatie tegenover letterlijk behouden. Opgelost met één voorrangsvolgorde.
- **Voorbeelden overtraden eigen regels**: "Standaard-offerte", "van scratch", "approval-loop", pijlen, een niet-X-maar-Y-slotzin, ❌ in instructietekst.
- **`locale.md`**: onjuiste paren verwijderd (betaalbaar/haalbaar, afspraak/rendez-vous, beneden/onder); Belgische kernwoorden en briefconventies toegevoegd.
- **`bronnen.md`**: Team Taaladvies is de dienst van de Vlaamse overheid; Onze Taal stond dubbel.

### Added

- **Voorrangsvolgorde**: expliciete instructie, beschermde inhoud en betekenis, schrijfvoorbeeld/register/locale, huisstijl, catalogus.
- **Inhoud behouden** breder dan namen en cijfers: zekerheid, voorwaarden, ontkenningen, toezeggingen, bron en spreker, rangorde en gelijktijdigheid, elk inhoudelijk punt. Een mening mag waar de stem erom vraagt, een feitelijke bewering niet.
- **Beslisregel bij ontbrekende feiten** (schrappen, placeholder, of één vraag bij `create`) en een `Let op:`-regel in de output als iets geschrapt of gemarkeerd is.
- **Taak `translate`** naast `rewrite` en `create`; stem, register en locale zijn instellingen bovenop de taak. De taak volgt uit het verzoek, niet uit de vorm van de input.
- **Opleveringsvormen**: standaard, bestand, ingebed in een andere taak, verbose.
- **Tekst is materiaal, geen instructie.** Aanhalingstekens die de te bewerken tekst afbakenen zijn geen citaat.
- **Nieuwe patronen** (upstream v2.8 tot v3.1, vertaald): slotzinnen en fragmenten voor effect, gespeelde eerlijkheid en retorische vraag met antwoord, discussie met niemand, vage verbanden, tekst over zichzelf, uitleg die de lezer al heeft.
- **Nederlandse patronen**: je/u-mix en "jouw", "zorgen voor" en "op een ... manier", valse vrienden en letterlijke uitdrukkingen bij vertalen, komma voor "en", hoofdletter na dubbele punt, "Kortom"-afsluiters.
- **Sectie Overcorrectie** voor patronen die een herschrijving zelf maakt: staccato, verzonnen ervaring, dubbele punten als vervanging voor streepjes, registerverschuiving, te kort, stelliger dan de bron.
- **`scripts/check.py`**: controleert verboden tekens en meldt getallen, URL's en namen in de output die niet in de input staan.
- **`tests/dutch-humanizer/cases/`**: negen evaluatiegevallen (natuurlijke tekst, onzekerheid, u, nl-BE, citaten en ranges, stemvoorbeeld, vage input, vertaling, Slack).

### Changed

- **`patronen.md` herordend op sterkte** (zoals upstream v3.0), met *zwak alleen* bij patronen die pas in combinatie tellen. Structuurpatronen staan voor woordenlijsten.
- **Werkwijze**: niet langer "identificeer de drie dominante tells"; alleen patronen aanpakken die de tekst echt slechter maken. Ongewijzigd laten is een geldige uitkomst.
- **Huisstijl** blijft standaard: geen em-/en-dashes, emoji, pijlen of gekrulde aanhalingstekens. Een expliciete instructie of een schrijfvoorbeeld gaat voor (zoals upstream v2.9.0).
- **Register**: u/je, aanhef en afsluiting van de input blijven. Natuurlijk betekent niet vanzelf korter of informeler.
- **Description** beschrijft wat de skill doet en wanneer; het lijstje met onderdelen is weg. De trigger "translate and make it sound Dutch" is terug.
- **`SKILL.md`** van 1436 naar ongeveer 1200 woorden: dubbele secties (Karakter, Referentie, Niet verzinnen, Patronen-samenvatting) samengevoegd, plus een snelle lijst zodat korte teksten de catalogus niet nodig hebben.

### Removed

- Patronen "onechte reeksen" en "synoniemroulette": Wikipedia ziet die inmiddels als menselijke of verouderde signalen (upstream v3.0).
- Patroon "onnatuurlijk er-gebruik": het voorbeeld van vermijding was gewoon correct Nederlands.
- Ongefundeerde frequentieclaims ("statistisch oververtegenwoordigd").

## [0.4.0] — 2026-05-09

Grote heroriëntatie van `dutch-humanizer` op basis van een externe deep-research review. De skill verandert van zuiver subtractief ("verwijder AI-tells") naar additief plus subtractief: verwijder AI-patronen, en hanteer tegelijk een positief stijlmodel verankerd in Taaladvies.net, Team Taaladvies en de Rijksoverheid/Vlaamse Overheid klare-taal-richtlijnen. Plus: drie modi, locale-bewustzijn (nl-NL/nl-BE), formele fact-inventory, severity-gestructureerde patroon-catalogus, en register-specifieke voorbeelden voor support en Slack.

De ene contentieuze externe aanbeveling, "soften de hard-zero em-dash regel naar context-aware", is na expliciete user-keuze afgewezen. De hard-zero regel blijft, nu duidelijk gemarkeerd als bewuste huisstijl-keuze in plaats van als Taaladvies-regel.

### Added

- **`references/principes.md`**: positief stijlmodel met tien principes (lezer eerst, doel boven onderwerp, concreet boven abstract, belangrijkste eerst, ritme variëren, channel-fit, actief boven passief, gewone woorden, eerlijk over onzekerheid, stem boven stijl-regels). Verankerd in Taaladvies.net en klare-taal-richtlijnen. Adres voor het vroegere gat "skill zegt wel wat niet, niet wat wel".
- **`references/bronnen.md`**: bron-hiërarchie. Niveau 1 (Woordenlijst Nederlandse Taal, Taaladvies.net) > niveau 2 (Team Taaladvies, Rijksoverheid klare taal, Vlaamse Overheid heerlijk helder) > niveau 3 (Van Dale, Onze Taal) > niveau 4 (dit repository) > niveau 5 (gebruiker-context). Conflict-resolutie: hogere niveaus winnen.
- **`references/locale.md`**: nl-NL/nl-BE-bewustzijn. Detectie-heuristieken, lexicale verschilstabel, juridische false-positives (wedde, schepen, OCMW), datum/cijfer-conventies (geen verschil tussen variaties), wanneer wel/niet automatisch converteren.
- **`references/voorbeeld-support.md`**: subtle voorbeeld voor customer support reply. AI-bad: "Het spijt ons oprecht ... wij begrijpen volkomen". Na: directe oplossing + concrete actie + naam in plaats van "het supportteam".
- **`references/voorbeeld-slack.md`**: extreme voorbeeld voor incident-update in chat. Toont fragmentaire chat-stijl met expliciete `feit/vermoeden/onderzoek/volgende update`-structuur in plaats van AI-formele incident-rapportage.
- **Drie modi in `SKILL.md`**: `rewrite` (default, bestaande tekst), `create` (uit bullets/brief, vraag om missende feiten), `voice-match` (met schrijfvoorbeeld). Vroeger werkte de skill impliciet alleen in rewrite-mode, ook als input bullets waren.
- **Formele fact-inventory in `SKILL.md` workflow-stap 5**: extract names/dates/amounts/percentages/versions/quotes/code/URLs → mark vaststaand/afgeleid/ontbrekend → herschrijf alleen binnen "safe rewrite zone" → final audit vergelijkt output tegen inventory. Vervangt eerdere informele "niet verzinnen"-tekst door uitvoerbare procedure.
- **Locale-detectie in workflow-stap 4**: `auto` → nl-NL fallback. Behoud bestaande locale; converteer niet automatisch.
- **Uitgebreide trigger-set in frontmatter**: voegt Engelse triggers toe (`make this sound like native Dutch`, `rewrite in idiomatic Dutch`, `translate and make it sound Dutch`, `don't translate literally`, `make this read like it was written in Dutch originally`). Skill activeert nu ook bij Engelstalige verzoeken om Nederlandse output.
- **Uitgebreide register-tabel in `SKILL.md`**: van 5 naar 9 registers. Toegevoegd: support reply, Slack/chat, vacaturetekst, beleids-/overheidstekst.
- **Bron-referentie in `SKILL.md`**: expliciete vermelding van Taaladvies.net, Woordenlijst Nederlandse Taal, Rijksoverheid en Vlaamse Overheid als gezaghebbende bronnen.

### Changed

- **`references/patronen.md` volledig gereorganiseerd op severity** in plaats van platte 44-genummerde lijst. Vijf nieuwe niveaus: Blockers (must-fix; raken betekenis/veiligheid), Major signals (sterke AI-tells), Moderate signals (contextueel), Contextual signals (channel-/huisstijl-afhankelijk), Communicatie-tics, Algemene spelcontrole. Plus expliciete "False positives" sectie tegen overcorrectie. Resultaat: makkelijker om top-3 dominante tells te kiezen in plaats van alle 44 mechanisch toepassen.
- **Per-pattern template** ingevoerd in `patronen.md`: Symptoom, Waarom AI, Niet fixen wanneer, Vervanging, Voorbeeld. Eerdere entries hadden alleen Voor/Na zonder false-positive guidance.
- **`references/voorbeeld-zakelijk.md`, `voorbeeld-linkedin.md`, `voorbeeld-docs.md` herschreven met two-NA-variant pattern**: variant A (input bevat geen specifieke feiten, output blijft algemeen) en variant B (input bevat concrete feiten, output gebruikt ze). Lost training-signal-conflict op waarbij eerdere voorbeelden tegelijk "voeg specificiteit toe" toonden en "verzin geen feiten" vertelden. Twee voorbeelden, dezelfde voor-tekst, twee correcte na-versies afhankelijk van wat in de input staat.
- **`SKILL.md` "Hard regels" sectie nu expliciet als huisstijl-keuze gemarkeerd**, niet als Taaladvies-regel. Tekst nu: "Dit is een huisstijl-keuze, bewust restrictiever dan officiële Nederlandstalige stijladvies (zoals Taaladvies.net), omdat AI-modellen 2024-2026 deze elementen produceren als visuele tic." Inclusief noot voor gebruikers die literaire/redactionele dashes wel willen: "dan is dit niet de juiste skill".
- **`SKILL.md` workflow van 6 naar 9 stappen** met expliciete modus-detectie en fact-inventory als aparte stappen. Volgorde: input lezen → modus → register → locale → fact-inventory → top-3 tells → herschrijven → zelf-audit (met fact-inventory-vergelijking) → opleveren.
- **`SKILL.md` zelf-audit-stap (8) breed uitgebreid** met expliciete check-list (kernboodschap, em-dashes, fact-inventory-vergelijking, register/locale-fit, "wat is hier nog AI-achtig").

### Fixed

- **Voorbeeld-conflict opgelost**: eerdere `voorbeeld-{zakelijk,linkedin,docs}.md` toonden NA-versies met verzonnen specifics ("twee weken eerder", "18% naar 12%", "90 dagen rotatie"), terwijl de aandachtspunt-noot onderaan tegen exact die fabricatie waarschuwde. Nu opgesplitst in variant A (zonder verzonnen specifics) en variant B (alleen als feiten uit input komen). Lost de strongest-learning-signal-versus-explicit-rule contradictie op.
- **Frontmatter description hercht**: vermeldt nu Taaladvies.net en Team Taaladvies-verankering, expliciete locale-modus, drie modi, fact-inventory, en huisstijl-positie van de hard-zero regel. Eerder vooral een opsomming van patroon-categorieën zonder positief frame.

### Note (over de scope-keuzes)

Het externe rapport adviseerde ook: een eval-rubric, gestructureerde test-corpus (`tests/cases/*.yaml`), output-linter (`scripts/lint_output.py`), publish-time regression-checks, en tien nieuwe register-voorbeelden. Deze zijn **niet** opgenomen. Reden: kosten-baten klopt niet voor een persoonlijke skill-collectie. Twee voorbeelden zijn toegevoegd (support, slack); de overige acht zijn als toekomstige uitbreiding gemarkeerd als gewenst, niet als blocker.

Het rapport baseerde zijn aanbevelingen ook op "OpenAI skill best practices" en "agents/openai.yaml metadata"; deze zijn voor Anthropic/Claude-skills niet van toepassing en niet gevolgd. Algemene principes (clear structure, eval-driven, edge-case coverage) wel.

## [0.3.0] — 2026-05-09

Hard regel toegevoegd: geen em-dashes (`—`) of en-dashes (`–`) in de output. Aanleiding: gebruiker rapporteerde dat gehumaniseerde tekst nog steeds AI-typische em-dashes bevatte. Onderzoek toonde drie root causes — twee NA-block bugs die het verkeerde gedrag voorbeeldden, plus ~50 em-dashes verspreid door de skill-instructies zelf, wat het model leerde dat matig em-dash-gebruik acceptabel is.

### Added

- **Hard regels-sectie** in `dutch-humanizer/SKILL.md`. Eén plek voor regels die in alle registers gelden: geen em-dash, geen en-dash, geen spatie-hyphen-spatie als gedachtestreepje, geen emoji's in lopende tekst, geen gekrulde aanhalingstekens, sentence case in koppen.
- **Self-audit-stap (5) bevat nu expliciete dash-check**: "Staan er nog em-dashes (`—`), en-dashes (`–`) of spatie-hyphen-spatie als gedachtestreepje in de output? Zo ja: vervangen." Vervangt de eerdere generieke "wat is hier nog AI-achtig?".
- **Frontmatter `description` vermeldt em-dashes** als hard regel naast emoji's en gekrulde aanhalingstekens.
- **Pattern #14 (gedachtestreepjes) heeft nu drie voor/na-voorbeelden** in plaats van één: dramatic pause/parenthetical (origineel), parenthetical achteraf (`"Dit werkt — meestal."` → `"Dit werkt meestal."`), list-intro (`"Drie redenen — snelheid, prijs, support."` → `"Drie redenen: snelheid, prijs, support."`).
- **Toelichting bij #14**: "AI-modellen produceren em-dashes als visuele tic. In Nederlandstalige output zijn ze bijna altijd vervangbaar door komma, punt of dubbele punt zonder betekenisverlies. Een fix voor één tell mag geen andere introduceren."

### Changed

- **Pattern #14 hernoemd** van "Overmatig gedachtestreepjes" naar "Gedachtestreepjes (em-dash en en-dash)". Verwijderd: bijwoord *overmatig*, dat suggereerde dat matig gebruik acceptabel was.
- **`SKILL.md` instructie-em-dashes (~18 stuks) vervangen** door komma, punt of dubbele punt. Skill modelt nu het gewenste gedrag.
- **`references/patronen.md` instructie-em-dashes (~9 buiten voor/na-blokken) vervangen.** "Subtieler — voor:" → "Subtieler. Voor:" (5×). "Probleem A — gesplitst" → "Probleem A. Gesplitst" (2×). Inline em-dashes in pattern-uitleg (#5, #29, #34, dt-fouten) vervangen door komma of punt.
- **`references/voorbeeld-{zakelijk,linkedin,docs}.md` titels gebruiken nu dubbele punt** in plaats van em-dash.
- **`references/stem-kalibratie.md` instructie-em-dashes (9 stuks) vervangen** door dubbele punt of punt.

### Fixed

- **`patronen.md` pattern #37 (echter) NA-block introduceerde em-dash** terwijl pattern #14 die juist verbiedt. Voorbeeld `"Dit werkt — meestal."` is verplaatst naar pattern #14 als VOOR-voorbeeld; #37 NA leest nu `"Dit werkt niet altijd." of "Dit werkt meestal."`.
- **`voorbeeld-linkedin.md` NA-blok bevatte em-dash** op regel 33 (`"Standaard-offerte ... — kost nu een uur..."`). Vervangen door punt + nieuwe zin.
- **`voorbeeld-linkedin.md` audit-bullet** quoteerde de VOOR-tekst inclusief em-dash. Vervangen door placeholder ("het gaat niet om X, het gaat om Y").

### Note

Em-dashes blijven aanwezig in expliciete VOOR-blokken (de slechte AI-voorbeelden) en in code-fenced illustraties van de regel zelf (bijvoorbeeld `\`—\`` in de tekst van de hard regel). Dat is bedoeld: de skill leert het patroon herkennen door het ALS BAD voorbeeld te tonen.

## [0.2.0] — 2026-05-09

Major rework of `dutch-humanizer` for correctness, maintainability and
context-efficiency. Skill output is now safer (no fabricated bron-citations),
the structure is split for progressive disclosure, and the pattern catalogue
is broader and more nuanced.

### Added

- **Anti-fabricatie regel** in `dutch-humanizer/SKILL.md`. The skill must now
  remove or mark vague bron-claims (`experts zeggen`, `onderzoek wijst uit`)
  rather than substitute invented specifics. Hard rule: never invent a bron,
  organisation, jaartal, percentage, naam or citaat to make a vague
  formulering "concreter".
- **"Niet aanraken" sectie** with explicit preservation rules for
  code-blokken, citaten, cijfers, datums, eigennamen, voetnoten, bronvermeldingen
  and intentional Markdown structure.
- **Register-specifieke voorbeelden** in `dutch-humanizer/references/`:
  - `voorbeeld-zakelijk.md` — email/notitie/memo
  - `voorbeeld-linkedin.md` — socials, korte post
  - `voorbeeld-docs.md` — technische documentatie
- **`stem-kalibratie.md`** — explicit workflow for matching a user's own
  schrijfvoorbeeld, with profile-extraction checklist (zinslengte,
  vulwoorden, leestekens, persoonsvorm, overgangen, eigenaardigheden) and
  guardrails (don't karikaturiseren, don't reproduce typo's, one stem per
  opdracht).
- **Verbose-modus triggers** documented: `--verbose`, `--toon-proces`,
  "toon proces", "laat zien hoe".
- **Nieuwe NL-specifieke patronen** in `references/patronen.md`:
  - `welke` als betrekkelijk voornaamwoord (waar `die`/`dat` hoort)
  - `middels` en officialese-voorzetsels (`alvorens`, `doch`, `immer`,
    `thans`)
  - `men` waar `je`/`we` natuurlijker is
  - `echter` mid-zin als komma-vulling
  - cliché-openers (`In een wereld waarin...`, `In tijden van...`)
  - bijvoeglijk-naamwoord-stapeling
  - vage opsomming-terminators (`en meer`, `etc.`)
  - NL datum/cijfer-format (komma als decimaal, dag-maand-jaar,
    kleine letters in maandnamen)
  - onnodige Engelse termen (`stakeholders`, `deliverables`, `alignment`,
    `bandwidth`, `ownership`, `commitment`, `leverage`)
  - meta-verwijzingen (`zoals eerder genoemd`)

### Changed

- **`SKILL.md` split for progressive disclosure**: from 367 regels naar
  ~120 regels. Volledige patroon-catalogus en voorbeelden zijn verplaatst
  naar `references/`. Resultaat: ~60% minder context-load wanneer de skill
  triggert; diepe details worden alleen geladen als de agent ze opzoekt.
- **Output-spec disambigueerd**: default-modus levert *uitsluitend* de
  herschrijving op. De drie-staps-procedure (eerste herschrijving →
  audit-bullets → definitieve versie) is nu expliciet verbose-only.
- **Patroon-merge: assistent-tics** — `chatbot-artefacten` (#20) en
  `slijmerige toon` (#22) zijn samengevoegd; de overlap was groot en de
  remediatie identiek.
- **Patroon-merge: samenstellings-regels** — `samenstellingen splitsen`
  (#34) en `koppelteken-overgebruik` (#26) zijn samengevoegd tot één
  regel met expliciete uitzonderingen voor klinkerbotsing
  (`data-analyse`, `zee-eend`), drie gelijke medeklinkers, voor-/
  achtervoegsels (`niet-roker`, `Nederlands-Duits`) en ingeburgerde
  leenwoorden (`e-mail`).
- **Patroon-herclassificatie: d/t-fouten** verplaatst van AI-specifiek
  naar "Algemene spelcontrole". Niet AI-uniek; blijft wel onderdeel van
  de zelf-audit omdat een dt-fout de hele tekst onverzorgd maakt.
- **Workflow expliciet gemaakt** met genummerde 6-staps-procedure
  (lezen → register → top-3 tells → herschrijven → zelf-audit → opleveren).
- **Frontmatter description verkort**: vaste count "37 patronen" verwijderd
  (groeit/krimpt), trigger-zinnen behouden en uitgebreid (`minder AI`).
- **Pattern #5 (vage bronvermeldingen) voorbeeld vervangen.** Het oude
  voorbeeld substitueerde `experts zeggen X` met `Sovon Vogelonderzoek
  (2023) zegt 10 miljoen trekvogels` — d.w.z. de skill leerde het model
  om bron-citations te verzinnen. Nu drie correcte aanpakken: claim
  verwijderen, markeren als `[bron?]`, of bestaande bron behouden.

### Fixed

- Conflict tussen "lever alleen de definitieve herschrijving op" en
  "sluit af met overzicht van wijzigingen (max 5 regels)" in de oude
  output-spec. Beide regels stonden gelijktijdig actief.
- Pattern #5 example die hallucinatie aanmoedigde (zie hierboven).

### Renamed

- `dutch-humanizer/references/voorbeeld.md` →
  `dutch-humanizer/references/voorbeeld-essay.md`. Maakt ruimte voor
  register-specifieke voorbeelden naast het oorspronkelijke
  essay-voorbeeld.

## [0.1.0] — 2026-05-09

Initial bootstrap of the `claude-skills` collection.

### Added

- Repository structure: each skill as an unpacked directory at repo root,
  containing `SKILL.md` plus optional `references/`, `scripts/`, `assets/`.
- `bundle.sh` — packages a skill source directory into a distributable
  `.skill` archive (zip) under `dist/`. Supports per-skill or all-skills
  bundling.
- `README.md` met installatie-instructies (from-source via symlink, of
  via gebouwd bundle), repo-layout, en proces voor het toevoegen van
  een nieuwe skill.
- `LICENSE` (MIT).
- `.gitignore` exclusions for `dist/`, `*.skill`, `.DS_Store`.
- `dutch-humanizer` skill — eerste skill in de collectie. Verwijdert
  AI-schrijfpatronen uit Nederlandstalige tekst, gebaseerd op Wikipedia
  "Signs of AI writing" plus NL-specifieke patronen. 37 patronen, register-
  detectie, voice-calibration via een `references/voorbeeld.md`.

[0.7.0]: https://github.com/fridzema/claude-skills/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/fridzema/claude-skills/compare/v0.4.0...v0.6.0
[0.4.0]: https://github.com/fridzema/claude-skills/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/fridzema/claude-skills/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fridzema/claude-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fridzema/claude-skills/releases/tag/v0.1.0
