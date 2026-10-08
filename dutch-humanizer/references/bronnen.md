# Bronnen en regels

Welke bron voorgaat bij een taalvraag, en waar de belangrijkste regels van deze skill vandaan komen. Dit bestand is voor naslag; bij een gewone herschrijving hoef je het niet te laden.

## Welke bron voorgaat

1. **Taalnorm**: Woordenlijst Nederlandse Taal (spelling) en Taaladvies.net (Taalunie, met Team Taaladvies van de Vlaamse overheid en Onze Taal). Taaladvies.net geeft aan wat standaardtaal is in Nederland, in België of in beide.
2. **Schrijfadvies**: klaretaalrichtlijnen van de Rijksoverheid en de Vlaamse overheid, de checklist duidelijke tekst van Onze Taal, Van Dale voor betekenis en registerlabels.
3. **Deze skill**: hoe je die normen toepast bij redigeren, plus standaardvoorkeuren.
4. **Gebruiker**: expliciete voorkeuren, stijlgidsen en schrijfvoorbeelden. Die gaan voor op de standaardvoorkeuren van deze skill, niet op spelling en grammatica, en nooit op betekenisbehoud.

Een regel van de gebruiker is niet onjuist omdat hij strenger is dan de taalnorm. Een strikte huisstijl zonder gedachtestreepjes is een geldige keuze.

## Regels

Type: **taalnorm** (Taalunie), **schrijfadvies**, **voorkeur** (van de gebruiker of standaard in deze skill), **heuristiek** (engineeringkeuze van deze skill, niet wetenschappelijk bewezen voor Nederlandse zakelijke tekst). "Gecontroleerd" is de datum waarop de passage is nagelezen; "niet nagelezen" betekent dat de bron bij deze versie niet opnieuw is geraadpleegd.

| ID | Regel | Type | Bron | Toepassing en uitzondering | Gecontroleerd | Test |
|---|---|---|---|---|---|---|
| R01 | Betekenis gaat voor stijl; inhoud, voorwaarden, zekerheid en handelingen blijven gelijk | heuristiek | Eigen ontwerp | Alle taken; bij `summarize` kies je wat blijft | n.v.t. | `tests/test_regressions.py`; evaluatie in de repository |
| R02 | Na een dubbele punt een kleine letter na een verklaring, ook bij een volledige zin | taalnorm | Taaladvies.net, "Hoofdletter na dubbele punt" | Hoofdletter bij citaat, eigennaam, opsomming van meerdere volledige zinnen | 2026-10-08 | `test_capital_after_colon_is_info_only` |
| R03 | "Mits" = alleen als; "tenzij" = behalve als | taalnorm | Taaladvies.net, "Mits of tenzij" | "Mits het droog is" = "tenzij het regent"; "mits het regent" in de betekenis van tenzij is geen standaardtaal | 2026-10-08 | regressies P11, P12; `test_mits_to_als_is_reviewed` |
| R04 | Belgisch- en Nederlands-Nederlandse standaardtaal zijn allebei correct | taalnorm | Taalunie, "Standaardtaal en geografische variatie" (2018) | Zet niet om tussen variëteiten zonder vraag | niet nagelezen | in de repository: `evals/dutch-humanizer/ontwikkelset.md` (04, 31) en validatieset (V09, V11-V13) |
| R05 | Lezer en leesdoel eerst; kern vindbaar | schrijfadvies | Onze Taal, "Checklist duidelijke tekst" | Geen doel op zich bij columns en verhalen | niet nagelezen | evaluatie in de repository |
| R06 | Strikte huisstijl: geen em- of en-dashes, emoji, pijlen; rechte aanhalingstekens | voorkeur | Keuze van de gebruiker (v0.4.0), opt-in sinds v0.6.0 | Alle bewerkbare tekst; citaten, code en eigennamen letterlijk | n.v.t. | `test_14_dash_configuration`, `test_protected_versus_plain_typography` |
| R07 | Getallen met `Decimal` uit de tekens, nooit via float; notatie volgens opgegeven locale | heuristiek | Python-documentatie, `decimal` | Onbekende locale: "1.234" blijft dubbelzinnig | niet nagelezen | regressies P01-P10, `test_explicit_locales` |
| R08 | Code letterlijk, met multipliciteit; ongesloten fence loopt tot het einde | heuristiek | CommonMark 0.31.2 (fenced code, code spans) | Geen volledige parser; containerblokken niet ondersteund | niet nagelezen | regressies P20-P23, `test_unclosed_fence_runs_to_end` |
| R09 | Geen gebruikerstekst in projectmappen; stdin of tijdelijke map buiten het project | heuristiek | Python-documentatie, `tempfile` | Opruimen garandeert geen veilig wissen | niet nagelezen | `test_stdin_mode_needs_no_files` |
| R10 | "Het lijkt erop" (aanwijzing) is niet "waarschijnlijk" (inschatting) | heuristiek | Eigen ontwerp | Ook in voorbeelden en patroon 9 | n.v.t. | signaalfamilie EVIDENTIAL; voorbeeld-slack |
| R11 | Patronen zijn signalen, geen bewijs van AI-auteurschap | heuristiek | Wikipedia "Signs of AI writing"; blader/humanizer v3.1 | Beoordeel de tekst, niet de herkomst | 2026-10-08 (humanizer) | n.v.t. |
| R12 | Frontmatter: `name` en `description` verplicht; `license`, `metadata` e.d. optioneel | platform | agentskills.io/specification | OpenAI-weergavemetadata staat apart in `agents/openai.yaml` | 2026-10-08 | `quick_validate.py` uit de skill-creator van Codex (buiten deze repository) |
| R13 | `SKILL.md` onder 500 regels; verwijzingen één niveau diep; inhoudsopgave bij referenties boven 100 regels | platform | Anthropic, "Skill authoring best practices" | | 2026-10-08 | handmatig |
| R14 | Evalueren tegen een baseline in gescheiden context; herhaalde runs | heuristiek | agentskills.io, "Evaluating skills"; Anthropic, "Demystifying evals" | Eigen Nederlandse cases; geen BLEU, ROUGE of detectiescores | 2026-10-08 (agentskills) | in de repository: `evals/dutch-humanizer/` |

## Wat de onderzoeksbronnen niet aantonen

Onderzoek naar Engelse stijltransfer en revisie (zoals Mir e.a. 2019, Babakov e.a. 2022, Pauli e.a. 2025, Jourdan e.a. 2025) en CheckList (Ribeiro e.a. 2020) is gebruikt voor het ontwerp van de tests: inhoudsbehoud, natuurlijkheid en stijl apart beoordelen, en invariantie- en perturbatietests. Het bewijst niets over het effect van deze skill op Nederlandse zakelijke tekst. Daarvoor tellen alleen de eigen evaluaties.

## Bronnen noemen in de output

Lever herschreven tekst, geen bronvermeldingen. Noem een bron alleen als de gebruiker erom vraagt of als je een keuze moet uitleggen.
