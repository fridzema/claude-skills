# Locale: nl-NL en nl-BE

Standaardtaal Nederlands kent twee regionale variëteiten: nl-NL (Nederland) en nl-BE (België, vaak "Vlaams" genoemd, maar bedoeld is *standaardtaal in België*, niet dialect).

Beide zijn standaardtaal. Geen variant is "beter". Maar ze verschillen in lexicon, syntaxis en register-conventies. Een nl-NL-tekst leest in België soms als formeel of vreemd; een nl-BE-tekst leest in Nederland soms als ouderwets of literair.

## Detectie en default

**Default: `locale=auto`.**

Detecteer aan de hand van:

1. **Expliciete instructie** door de gebruiker (`schrijf in Belgisch Nederlands`, `nl-BE`, `nl-NL`, `Vlaamse standaardtaal`).
2. **Eigennamen en organisatie-context** in de input (Belgastraat, KBC, RTBF, Vlaamse overheid → nl-BE; ABN AMRO, NS, gemeente Utrecht → nl-NL).
3. **Lexicale tells** in de input zelf (zie tabel hieronder).
4. **Bij geen signaal: nl-NL** als pragmatische default (grootste publiek), tenzij de gebruiker anders zegt.

Als de input duidelijk `nl-BE` is en de gebruiker geen andere variant vraagt: **behoud nl-BE in de output**. Niet "omzetten" tenzij gevraagd.

## Veelvoorkomende verschillen (kort overzicht)

Niet uitputtend. Bij specifieke twijfel: raadpleeg Taaladvies.net (markeert "standaardtaal in NL", "standaardtaal in BE", of "algemeen").

### Lexicaal

| nl-NL | nl-BE |
|---|---|
| zo'n / dergelijk(e) | dergelijk(e) (formeler in BE) |
| binnenkort | weldra (frequenter in BE) |
| meteen | direct, dadelijk |
| beneden | onder |
| vergaderen | vergaderen, samenkomen |
| salaris | wedde (frequenter in BE) |
| verbruik | verbruik / consumptie |
| boterham | boterham (NL ook "broodje" voor belegde versie); BE "broodje" = belegde versie |
| stoplicht | verkeerslicht |
| pinpas | bankkaart |
| afspraak | afspraak / rendez-vous |
| betaalbaar | betaalbaar / haalbaar |

### Syntactisch

- **"Heb"-vorm in onbepaalde tijd**: nl-BE gebruikt vaker "heb" waar nl-NL "ben" gebruikt bij sommige werkwoorden ("ik ben vergeten" vs "ik heb vergeten"). Beide zijn standaardtaal.
- **Werkwoordvolgorde in eindgroep**: Vlaams kent variatie ("dat hij gegaan is" / "dat hij is gegaan"). Beide zijn standaardtaal.
- **"Aan het + infinitief"**: in nl-BE soms "bezig met". Beide goed.
- **Diminutief-vormen**: "boekje" universeel, maar register-gebruik wisselt.

### Officialese / juridisch

België heeft eigen wetgeving en bestuurskundige termen. Niet vertalen naar nl-NL-equivalent als dat de juridische betekenis verandert:

- "wedde" (BE, ambtelijk) ≠ "salaris" (NL, breed).
- "schepen" (BE, gemeentebestuur) ≠ "wethouder" (NL).
- "OCMW" (BE): geen NL-equivalent met dezelfde rol.
- "burgemeester" werkt in beide.

## Datum, getal, tijd

Beide locales volgen NL-conventies (zie `patronen.md` "Datum- en cijfer-format"):

- Decimaal: komma (`€3,14`).
- Datum: dag-maand-jaar (`15 januari 2026`).
- Tijd: 24-uurs (`14:30`).
- Maandnamen: kleine letter.

Geen wezenlijk verschil tussen nl-NL en nl-BE op deze punten.

## Wanneer locale-switchen wel zinvol is

Als de tekst voor een specifiek publiek is, en het tegengestelde locale onnatuurlijk klinkt:

- **nl-NL → nl-BE conversie**: als de tekst voor Belgisch publiek is en nu Nederlandse begrippen gebruikt die in BE iets anders betekenen.
- **nl-BE → nl-NL conversie**: als de tekst voor Nederlands publiek is en nu Belgische begrippen gebruikt die in NL onbekend zijn.

Bij switching: vraag de gebruiker wat het doel-publiek is, en behoud daarna locale consistent door de hele tekst.

## Wanneer locale-switchen NIET zinvol is

- Als de tekst neutraal-Nederlandse termen gebruikt (geldig in beide). Geen switching nodig.
- Als de gebruiker gewoon "humaniseren" vraagt zonder locale-wens. Behoud bestaande locale.
- Voor citaten en eigennamen: nooit switchen. Een Vlaamse minister wordt niet "wethouder".

## Output-output van skill bij locale

In zelf-audit (zie `SKILL.md` stap 5):

- Heb ik de input-locale herkend en behouden?
- Als ik geconverteerd heb: heb ik dat consistent gedaan?
- Komen er termen uit de andere locale per ongeluk doorheen ("ik heb dat gevraagd aan de wethouder" in een Vlaamse tekst)?

Bij twijfel: behoud is veiliger dan converteren.
