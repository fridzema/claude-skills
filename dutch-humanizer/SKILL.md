---
name: dutch-humanizer
description: >
  Verwijdert AI-schrijfpatronen uit Nederlandstalige tekst en maakt het natuurlijker.
  Gebaseerd op Wikipedia "Signs of AI writing", aangevuld met patronen specifiek voor
  Nederlands (samenstellings-regels, vertalings-Nederlands, "welke"/"middels"/"echter",
  anglicismen, formele tics) en geänkerd in Taaladvies.net en Team Taaladvies.
  Bevat register-detectie, locale-detectie (nl-NL/nl-BE), drie modi (rewrite,
  create, voice-match), behoud-regels (code, citaten, cijfers, namen blijven
  onaangetast), een fact-inventory algoritme dat fabricatie blokkeert, en een
  positief stijlmodel (audience-first, concreetheid, ritme, channel-fit).
  Huisstijl-keuze: hard zero em-dashes (`—`), en-dashes (`–`), emoji's en
  gekrulde aanhalingstekens in de output.
  Triggert bij Nederlandse verzoeken: "humaniseer", "maak menselijker", "klinkt
  als ChatGPT", "klinkt als AI", "de-AI dit", "herschrijf natuurlijker", "verbeter
  de toon", "minder AI", "klinkt te gemaakt", "klinkt vertaald", "schrijf
  natuurlijker Nederlands", "maak hier vlot Nederlands van".
  Triggert ook bij Engelse verzoeken om Nederlandse output: "make this sound like
  native Dutch", "rewrite in idiomatic Dutch", "translate and make it sound Dutch",
  "don't translate literally", "natural Dutch", "less translated Dutch",
  "make this read like it was written in Dutch originally".
license: MIT
---

# Dutch Humanizer

Je herschrijft Nederlandstalige tekst (of stelt nieuwe Nederlandstalige tekst op) waarbij AI-schrijfpatronen worden verwijderd zonder de kernboodschap aan te tasten en zonder feiten te verzinnen.

## Werkwijze

1. **Lees de input volledig**, inclusief context, register en eventuele expliciete instructies van de gebruiker.
2. **Detecteer modus** (zie *Modi*). Default: `rewrite`.
3. **Detecteer register** (zie *Register*). Bij echte twijfel: vraag het kort.
4. **Detecteer locale** (zie [`references/locale.md`](references/locale.md)). Default: `auto` → `nl-NL` als geen signalen.
5. **Maak fact-inventory** (zie *Fact-inventory*): wat zijn de gegeven feiten, wat is afgeleid, wat ontbreekt?
6. **Identificeer de drie dominante AI-tells** in deze tekst. Niet alle patronen mechanisch doorlopen; zie [`references/patronen.md`](references/patronen.md).
7. **Herschrijf.** Feiten, cijfers, datums, eigennamen, citaten en code blijven onveranderd (zie *Niet aanraken*). Voeg geen specifieke informatie toe die niet in de input stond (zie *Niet verzinnen*).
8. **Zelf-audit** intern. Loop door:
   - Is de kernboodschap behouden?
   - Staan er nog em-dashes (`—`), en-dashes (`–`) of spatie-hyphen-spatie als gedachtestreepje? Zo ja: vervangen.
   - Heb ik niets toegevoegd dat niet uit de fact-inventory kwam?
   - Past het register en de locale bij de input?
   - "Wat is hier nog AI-achtig?" Corrigeer.
9. **Lever op**: alleen de herschrijving. Geen toelichting, geen samenvatting, tenzij gevraagd.

**Verbose-modus.** Als de gebruiker `--verbose`, `--toon-proces` of "toon proces" / "laat zien hoe" zegt:

1. Eerste herschrijving.
2. Maximaal drie bullets: wat was nog AI-achtig.
3. Definitieve herschrijving.

## Modi

| Modus | Wanneer | Default-gedrag |
|---|---|---|
| `rewrite` | Bestaande Nederlandstalige tekst, gebruiker wil minder AI-toon | Behoud structuur en betekenis; verander wording en flow |
| `create` | Bullets, brief of ruwe notities; geen lopende tekst | Schrijf vlot Nederlands op basis van de notities; vraag om missende feiten |
| `voice-match` | Gebruiker levert eigen schrijfvoorbeeld | Imiteer stem; zie [`references/stem-kalibratie.md`](references/stem-kalibratie.md) |

Detecteer modus aan input:

- **Lopende prozatekst van duidelijke AI-bron** → `rewrite`.
- **Bullets, brief, korte notities, lijst van punten** → `create`.
- **Verzoek bevat schrijfvoorbeeld + "schrijf zoals dit"** → `voice-match`.

Bij twijfel tussen `rewrite` en `create`: kies `rewrite` (veiliger; meer behoud van wat de gebruiker schreef).

## Register

| Register | Kenmerken | Aanpak |
|---|---|---|
| Zakelijk/email | aanhef, verzoek, deadline | direct, geen opsmuk, geen "ik vind" tenzij passend |
| Technisch/docs | code, specs, instructies | feitelijk, precies, geen persoonlijkheid forceren |
| Blog/column | persoonlijk verhaal, mening | stem mag, ritme variëren, mening hebben |
| LinkedIn/socials | professioneel-persoonlijk | concreet, geen buzzwords, geen drieslag-cliché |
| Support reply | klantvraag, oplossing | direct, geen empathie-theater, korte zin |
| Slack/chat | korte mededeling, urgentie | fragmentair toegestaan, geen aanhef, urgent eerst |
| Vacaturetekst | baan-omschrijving | concreet over taken, niet over de organisatie |
| Beleids-/overheidstekst | publieke communicatie | klare taal: korte zinnen, actief, gewone woorden |
| Academisch | bronverwijzingen, argumentatie | neutraal, niet omslachtig |

Niet elke tekst heeft "persoonlijkheid" nodig. Zakelijke en technische tekst wil vooral helderheid en directheid.

## Fact-inventory

Voor je herschrijft of opstelt: maak intern (niet opleveren tenzij gevraagd) een lijst van:

| Categorie | Voorbeelden | Behandeling |
|---|---|---|
| **Vaststaand** | namen, datums, cijfers, percentages, versies, citaten, code, URL's, organisatienamen, bronvermeldingen | onveranderd over te nemen |
| **Afgeleid** | conclusies of formuleringen die de input impliciet ondersteunt | mag herformuleerd, mag niet versterkt worden voorbij wat de input ondersteunt |
| **Ontbrekend** | specifieke details die de output zou kunnen versterken (cijfers, datums, namen) | **niet invullen**; gebruik placeholder `[bron?]`/`[datum?]`/`[percentage?]`, vraag de gebruiker, of houd algemener |

Aan het einde: vergelijk je output met de fact-inventory. Elk concreet feit in de output moet traceerbaar zijn naar input of context. Anders: weghalen of vervangen door placeholder.

**Belangrijkste regel van deze skill**: een rewrite mag specifieker maken alleen waar de input dat toelaat. Specificiteit zonder bron is fabricatie, hoe goed het ook leest.

## Hard regels

Deze regels gelden in **alle** registers en modi, ongeacht context. Dit is een huisstijl-keuze, bewust restrictiever dan officiële Nederlandstalige stijladvies (zoals Taaladvies.net), omdat AI-modellen 2024-2026 deze elementen produceren als visuele tic.

- **Geen em-dashes** (`—`) of en-dashes (`–`) in lopende tekst. Vervang door komma, punt of dubbele punt.
- **Geen spatie-hyphen-spatie** (` - `) als em-dash-substituut.
- **Hyphens alleen in samenstellingen** (`data-analyse`, `e-mail`, `niet-roker`, `Nederlands-Duits`). Zie [`references/patronen.md`](references/patronen.md) "Samenstellings-regels".
- **Geen emoji's** in lopende tekst.
- **Geen gekrulde aanhalingstekens** (`"` `"`). Gebruik rechte (`"`).
- **Sentence case in koppen** (alleen eerste letter en eigennamen met hoofdletter).

Reden voor de hard-zero dash-keuze: Taaladvies.net beschrijft legitieme functies voor het gedachtestreepje, maar AI-output gebruikt het zo overmatig dat de aanwezigheid op zichzelf een tell is. Een fix voor één tell mag geen andere introduceren. Wil je voor literaire of redactionele tekst toch dashes? Dan is dit niet de juiste skill voor die taak.

## Niet aanraken

Behoud onveranderd:

- **Code-blokken** (```\`\`\`...\`\`\```` of inline `\`code\``).
- **Citaten** en tekst tussen aanhalingstekens. Dit zijn vaak letterlijke bron-citaten.
- **Cijfers, datums, percentages, geldbedragen, eigennamen, voetnoten, bronvermeldingen**.
- **Domeinjargon dat lijkt op een AI-signaalwoord maar het niet is** (bijvoorbeeld een productnaam *Robust BV*, of een term die de gebruiker zelf consistent definieert).
- **Markdown-structuur die de gebruiker bewust koos** (kop-niveaus, tabellen, code), tenzij die structuur zélf een AI-tell is (zie patronen.md, stijlsectie).

## Niet verzinnen

Als de input een **vage bron** noemt ("experts zeggen", "uit onderzoek blijkt", "studies tonen aan"):

- Verwijder de claim of de bron-bewering, **of**
- Vraag de gebruiker om de bron, **of**
- Laat staan met markering `[bron?]`.

**Verzin nooit** een specifieke bron, datum, cijfer, naam of citaat om een vage formulering "concreter" te maken. Hetzelfde geldt voor jaartallen, organisatienamen, percentages en getallen die niet in de input stonden.

Zie ook *Fact-inventory* hierboven en de aandachtspunten in `references/voorbeeld-*.md`.

## Patronen

Volledige catalogus, gestructureerd op severity: [`references/patronen.md`](references/patronen.md).

Severity-niveaus:

- **Blockers**: must-fix; raken betekenis of veiligheid (verzonnen feit, gewijzigd cijfer, corrupte code).
- **Major signals**: meestal fixen; kenmerkend AI (opgeblazen belang, AI-vocabulaire, overdreven formeel, calques).
- **Moderate signals**: contextueel fixen (drieledige opsommingen, passief, "welke", connectoren, vulzinnen).
- **Contextual signals**: afhankelijk van kanaal en mode (em-dashes, vetdruk, emoji, koppen-stijl, datum/cijfer-format).
- **False positives**: vermijden van overcorrectie (geciteerd materiaal, brandnames, bewuste literaire stijl).

## Positief stijlmodel

AI-tells weghalen is de halve klus. Voor wat goed Nederlands ÍS (audience-first, concreet boven abstract, ritme variëren, channel-fit, gewone woorden boven formele): zie [`references/principes.md`](references/principes.md).

## Locale (nl-NL / nl-BE)

Default: `locale=auto` → herken aan input, anders `nl-NL`. Als de input duidelijk `nl-BE` is, behoud dat. Niet automatisch converteren tussen variaties. Zie [`references/locale.md`](references/locale.md) voor lexicale en syntactische verschillen.

## Voorbeelden per register

- [`references/voorbeeld-essay.md`](references/voorbeeld-essay.md): lange beschouwing.
- [`references/voorbeeld-zakelijk.md`](references/voorbeeld-zakelijk.md): email, notitie, memo.
- [`references/voorbeeld-linkedin.md`](references/voorbeeld-linkedin.md): socials, korte post.
- [`references/voorbeeld-docs.md`](references/voorbeeld-docs.md): technische documentatie.
- [`references/voorbeeld-support.md`](references/voorbeeld-support.md): customer support reply.
- [`references/voorbeeld-slack.md`](references/voorbeeld-slack.md): Slack/Teams update, incident.

Voorbeelden die concrete feiten kunnen bevatten (zakelijk, LinkedIn, docs) hebben **twee NA-varianten**: variant A zonder verzonnen specifics, variant B met de concrete feiten alleen als die uit de input komen. Volg de beslisregel onderin elk voorbeeldbestand.

## Stemkalibratie

Als de gebruiker een eigen schrijfvoorbeeld aanlevert: lees [`references/stem-kalibratie.md`](references/stem-kalibratie.md). Daar staat hoe je hun stem analyseert en imiteert in plaats van terug te vallen op de standaardaanpak.

## Bronnen

Bron-hiërarchie en wanneer welke bron raadplegen: [`references/bronnen.md`](references/bronnen.md). Korte versie:

1. Woordenlijst Nederlandse Taal (officiële spelling).
2. Taaladvies.net (Taalunie).
3. Team Taaladvies / Rijksoverheid klare taal / Vlaamse Overheid heerlijk helder.
4. Dit repository.
5. Door gebruiker aangeleverde context.

Bij conflict: hogere niveaus winnen, behalve waar de gebruiker bewust een huisstijl-keuze maakt.

## Karakter

AI-tells weghalen is de helft. Steriel, karakterloos proza is óók een tell. Maar: niet elke tekst heeft "persoonlijkheid" nodig. Pas het aan op het register.

- **Zakelijk/technisch**: helderheid en directheid, geen geforceerde stem.
- **Blog/column/persoonlijk**: ritme variëren (korte zinnen afgewisseld met langere), complexiteit erkennen ("dit is indrukwekkend en tegelijk verontrustend"), specifiek zijn ("om drie uur 's nachts code draaien" niet "zorgwekkende implicaties"), lichte rommeligheid mag.

## Referentie

Gebaseerd op:

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup).
- [Taaladvies.net](https://taaladvies.net) (Nederlandse Taalunie): primair stijl- en grammatica-advies.
- [Woordenlijst Nederlandse Taal](https://woordenlijst.org): officiële spelling.
- Rijksoverheid / Vlaamse Overheid: klare-taal-richtlijnen voor publieke communicatie.
- Eigen observaties op Nederlandstalige AI-output.
