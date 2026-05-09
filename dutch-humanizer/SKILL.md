---
name: dutch-humanizer
description: >
  Verwijdert AI-schrijfpatronen uit Nederlandstalige tekst en maakt het natuurlijker.
  Gebaseerd op Wikipedia "Signs of AI writing", aangevuld met patronen specifiek voor
  Nederlands (samenstellings-regels, vertalings-Nederlands, "welke"/"middels"/"echter",
  anglicismen, formele tics). Bevat register-detectie, behoud-regels (code, citaten,
  cijfers, namen blijven onaangetast) en een anti-fabricatie-regel (verzin nooit
  bronnen of feiten).
  Triggert bij: "humaniseer", "maak menselijker", "klinkt als ChatGPT", "klinkt
  als AI", "de-AI dit", "herschrijf natuurlijker", "verbeter de toon", "minder AI"
  en vergelijkbare verzoeken in het Nederlands.
license: MIT
---

# Dutch Humanizer

Je herschrijft Nederlandstalige tekst om AI-schrijfpatronen te verwijderen zonder de kernboodschap aan te tasten.

## Werkwijze

1. **Lees de input volledig** — inclusief context, register en eventuele expliciete instructies van de gebruiker.
2. **Detecteer het register** (zie tabel hieronder). Bij echte twijfel: vraag het kort.
3. **Identificeer de drie dominante AI-tells** in deze tekst — niet alle patronen mechanisch doorlopen.
4. **Herschrijf** — feiten, cijfers, datums, eigennamen, citaten en code blijven onveranderd (zie *Niet aanraken*).
5. **Zelf-audit** intern: "wat is hier nog AI-achtig?" — corrigeer voor je oplevert.
6. **Lever op**: alleen de herschrijving. Geen toelichting, geen samenvatting, tenzij gevraagd.

**Verbose-modus** — als de gebruiker `--verbose`, `--toon-proces` of "toon proces" / "laat zien hoe" zegt:

1. Eerste herschrijving.
2. Maximaal drie bullets: wat was nog AI-achtig.
3. Definitieve herschrijving.

## Register

| Register | Kenmerken | Aanpak |
|---|---|---|
| Zakelijk/email | aanhef, verzoek, deadline | direct, geen opsmuk, geen "ik vind" tenzij passend |
| Technisch/docs | code, specs, instructies | feitelijk, precies, geen persoonlijkheid forceren |
| Blog/column | persoonlijk verhaal, mening | stem mag, ritme variëren, mening hebben |
| LinkedIn/socials | professioneel-persoonlijk | concreet, geen buzzwords, geen drieslag-cliché |
| Academisch | bronverwijzingen, argumentatie | neutraal, maar niet omslachtig |

Niet elke tekst heeft "persoonlijkheid" nodig. Zakelijke en technische tekst wil vooral helderheid en directheid.

## Niet aanraken

Behoud onveranderd:

- **Code-blokken** (```\`\`\`...\`\`\```` of inline `\`code\``).
- **Citaten** en tekst tussen aanhalingstekens — kunnen letterlijke bron-citaten zijn.
- **Cijfers, datums, percentages, geldbedragen, eigennamen, voetnoten, bronvermeldingen.**
- **Domeinjargon dat lijkt op een AI-signaalwoord maar het niet is** (bijvoorbeeld een productnaam *Robust BV*, of een term die de gebruiker zelf consistent definieert).
- **Markdown-structuur die de gebruiker bewust koos** (kop-niveaus, tabellen, code) — *tenzij* die structuur zélf een AI-tell is (zie patronen.md, stijlsectie).

## Niet verzinnen

Als de input een **vage bron** noemt ("experts zeggen", "uit onderzoek blijkt", "studies tonen aan"):

- Verwijder de claim of de bron-bewering, **of**
- Vraag de gebruiker om de bron, **of**
- Laat staan met markering `[bron?]`.

**Verzin nooit** een specifieke bron, datum, cijfer, naam of citaat om een vage formulering "concreter" te maken. Hetzelfde geldt voor jaartallen, organisatienamen en getallen die niet in de input stonden.

## Patronen

Volledige lijst met voor/na-voorbeelden: [`references/patronen.md`](references/patronen.md). Categorieën:

- **Inhoud** — opgeblazen belang, promotioneel taalgebruik, vage bronnen, formulaire conclusies, oppervlakkige deelwoord-analyses.
- **Taal en grammatica** — AI-vocabulaire, koppelwerkwoord-vermijding, negatieve parallellismen, drieledige opsommingen, synoniemroulette, passief.
- **Stijl** — gedachtestreepjes, vetdruk, Title Case, emoji's, gekrulde aanhalingstekens, verticale lijsten met inline koppen.
- **Communicatie** — assistent-tics (chatbot-artefacten + slijmerige toon), kennisgrens-disclaimers.
- **Opvulling** — vulzinnen, hedging, wegwijzers, "het is vermeldenswaard", retorische autoriteitsfrases, generieke positieve conclusies.
- **NL-specifiek** — samenstellings-regels, vertalings-Nederlands ("welke", "middels", "echter", "men"), anglicismen, datum/cijfer-format, onnodige Engelse termen, formele tics ("derhalve", "aldus"), verbindingswoord-stapeling, "er"-gebruik, cliché-openers, bijvoeglijk-naamwoord-stapeling.

Lees `patronen.md` als je een patroon niet zeker herkent of een nuance nodig hebt (bijvoorbeeld: wanneer wel/geen koppelteken in samenstellingen).

## Voorbeelden per register

- [`references/voorbeeld-essay.md`](references/voorbeeld-essay.md) — lange beschouwing.
- [`references/voorbeeld-zakelijk.md`](references/voorbeeld-zakelijk.md) — email, notitie, memo.
- [`references/voorbeeld-linkedin.md`](references/voorbeeld-linkedin.md) — socials, korte post.
- [`references/voorbeeld-docs.md`](references/voorbeeld-docs.md) — technische documentatie.

## Stemkalibratie

Als de gebruiker een eigen schrijfvoorbeeld aanlevert: lees [`references/stem-kalibratie.md`](references/stem-kalibratie.md). Daar staat hoe je hun stem analyseert en imiteert in plaats van terug te vallen op de standaardaanpak.

## Karakter

AI-tells weghalen is de helft. Steriel, karakterloos proza is óók een tell. Maar: niet elke tekst heeft "persoonlijkheid" nodig — pas het aan op het register.

- **Zakelijk/technisch**: helderheid en directheid, geen geforceerde stem.
- **Blog/column/persoonlijk**: ritme variëren (korte zinnen afgewisseld met langere), complexiteit erkennen ("dit is indrukwekkend en tegelijk verontrustend"), specifiek zijn ("om drie uur 's nachts code draaien" niet "zorgwekkende implicaties"), lichte rommeligheid mag.

## Referentie

Gebaseerd op [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup), aangevuld met observaties specifiek voor Nederlandstalige AI-output.
