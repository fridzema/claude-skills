# Changelog

All notable changes to this repository are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The version applies to the repository as a whole. Individual skills may evolve
independently between releases; see each skill's `SKILL.md` frontmatter for
its own version metadata if present.

## [Unreleased]

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

[Unreleased]: https://github.com/fridzema/claude-skills/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/fridzema/claude-skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fridzema/claude-skills/releases/tag/v0.1.0
