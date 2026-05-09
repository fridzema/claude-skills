# Changelog

All notable changes to this repository are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The version applies to the repository as a whole. Individual skills may evolve
independently between releases; see each skill's `SKILL.md` frontmatter for
its own version metadata if present.

## [Unreleased]

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

[Unreleased]: https://github.com/fridzema/claude-skills/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/fridzema/claude-skills/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/fridzema/claude-skills/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fridzema/claude-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fridzema/claude-skills/releases/tag/v0.1.0
