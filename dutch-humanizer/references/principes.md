# Principes: positief model van menselijk Nederlands

AI-tells weghalen is de halve klus. Wat blijft als je AI-patronen wegstreept, is vaak nog steriel of plat. Deze principes geven het positieve model: wat maakt Nederlandstalige tekst werkelijk goed?

Gebaseerd op richtlijnen van Team Taaladvies, Taaladvies.net (Taalunie), Rijksoverheid en Vlaamse Overheid (klare taal). Zie [`bronnen.md`](bronnen.md) voor de bron-hiërarchie.

## 1. Lezer eerst

> Voor wie schrijf je? Wat weet die lezer al? Wat moet die lezer doen, weten of voelen na het lezen?

Native-feeling Nederlands begint niet bij de schrijver maar bij de lezer. AI schrijft vaak "in het algemeen" voor "iemand". Een mens schrijft voor iemand specifiek met een specifieke situatie.

**Voor:** "Deze tool kan organisaties helpen om hun processen te optimaliseren."
**Na:** "Als je weekrapportages handmatig in elkaar zet, scheelt deze tool je een halve dag per week."

## 2. Doel boven onderwerp

Iedere zin moet bijdragen aan het lezersdoel. Een tekst is geen verzameling waarheden over een onderwerp; het is gereedschap waarmee de lezer iets kan.

Een email die om beslissing vraagt, eindigt met de keuze. Een handleiding die werkend wil maken, eindigt met de werkende output. Een blog die een mening verkondigt, eindigt met de mening, niet met "spannende tijden liggen voor de deur".

## 3. Concreet boven abstract

Als je iets abstract kunt opschrijven, kun je het bijna altijd ook concreet. Concreet is bijna altijd beter, behalve waar abstractie expliciet doel is (filosofische tekst, juridische definities).

| Abstract (vaak AI) | Concreet (vaak menselijk) |
|---|---|
| "verbeterde gebruikservaring" | "drie klikken minder bij het inloggen" |
| "uitdagingen op het gebied van resourcing" | "twee mensen ziek, één ouderschapsverlof" |
| "operationele excellentie" | "facturatie binnen 5 dagen, foutpercentage onder 1%" |
| "transformatieve impact" | "we zijn van vier dagen naar één dag doorlooptijd gegaan" |

Belangrijke regel: **wees concreet over wat je weet, niet over wat je verzint**. Zie [`SKILL.md`](../SKILL.md) "Niet verzinnen".

## 4. Belangrijkste eerst

Nederlands schrijven (en lezen) volgt vaker dan Amerikaans-Engels het patroon van *belangrijkste eerst*. Geen lange aanloop, geen build-up, geen "let me set the scene". Ten minste in zakelijk, journalistiek en ambtelijk register.

**Voor:** "Naar aanleiding van de afgelopen kwartaalrapportage en de daaruit voortvloeiende inzichten met betrekking tot onze pipeline, zou ik graag voorstellen dat we ..."
**Na:** "Ik wil het offertetraject inkorten van 11 naar 5 dagen. Hieronder waarom en hoe."

In blog/column mag je een aanloop nemen, maar dan bewust voor effect.

## 5. Ritme: variëren, niet uniformeren

AI produceert vaak zinnen van vergelijkbare lengte (allemaal middellang) of vergelijkbaar complex (allemaal hoofdzin + bijzin). Dat leest als een metronoom.

Goed Nederlands wisselt af. Korte zin. Dan eentje die er de tijd voor neemt om iets uit te leggen waarvan de lezer mag merken dat het complex is. Korte zin terug.

In zakelijk/technisch is "korter is bijna altijd beter". In blog/column is "ritme variëren" belangrijker.

## 6. Channel-fit

Geen tekst leest in vacuüm. Een Slack-bericht in beleidstaal valt op (te formeel). Een memo in chat-stijl valt op (te informeel). Match het kanaal.

| Kanaal | Korte kenmerken |
|---|---|
| Email zakelijk | Aanhef, directe vraag of mededeling, korte alinea's, ondertekening |
| Slack/chat | Geen aanhef, korte zin, soms incompleet, urgentie eerst |
| Blog/column | Eerste persoon mag, aanloop mag, ritme-variatie mag |
| Productdocs | Imperatief ("Maak een token aan"), code-blokken, geen marketing |
| Beleids-/overheidstekst | Klare taal: korte zinnen, actief, gewone woorden |
| Vacaturetekst | Beschrijf de baan, niet de organisatie. Concreet over taken |
| LinkedIn-post | Eén punt per post, concreet, geen drieslag-cliché |
| Academische tekst | Neutraal, voorzichtig met claims, duidelijk over bron |

## 7. Actief boven passief, behalve waar het verbergt

Standaard: actief. "Het rapport beschrijft X" leest beter dan "X wordt beschreven in het rapport".

Uitzondering 1: als de actor onbekend, irrelevant of bewust verborgen is. "De server is herstart"; wie dat heeft gedaan is meestal niet relevant.

Uitzondering 2: in instructies waar de lezer de actor is, gebruik gebiedende wijs of "je"-vorm. "Maak een token aan" / "Je maakt een token aan" zijn beide goed; passief "Een token wordt aangemaakt" is steriel.

## 8. Gewone woorden boven formele

Taaladvies: gebruik formele woorden spaarzaam. Liever "ook" dan "tevens". Liever "om" dan "teneinde". Liever "via" dan "middels". Liever "die" dan "welke".

Behoud een formele term alleen als die specifiek juridische, technische of vakbetekenis heeft. "De akte" in een notariële tekst is niet "het document"; het *is* een akte.

## 9. Eerlijk over wat je niet weet

Mensen schrijven "ik weet niet zeker, maar". AI schrijft "het is duidelijk dat" of "het is algemeen bekend dat", vaak zonder dat dat klopt.

Drie opties bij onzekerheid:

1. Markeer expliciet ("volgens de planning, maar nog niet bevestigd").
2. Laat de claim weg.
3. Vraag de gebruiker om de bron of het cijfer (zie fact-inventory in `SKILL.md`).

Dit is geen stijl-vraag maar een veiligheidsvraag. Verzonnen specifics zijn schadelijk.

## 10. Stem boven stijl-regels (waar het past)

Voor blog/column/persoonlijke tekst: een specifieke stem van een bekende schrijver beats elke generieke "humanisering". Vraag (of gebruik, als de gebruiker een stuk eigen werk geeft) een schrijfvoorbeeld; zie [`stem-kalibratie.md`](stem-kalibratie.md).

Voor zakelijk/technisch/overheid: stem-vraag is minder relevant. Daar zijn helderheid, snelheid en juistheid de "stem".

## Hoe deze principes gebruiken

Niet als checklist. Eerder als kalibratie-bril:

1. Lees je rewrite hardop.
2. Vraag jezelf per principe: ben ik hier in de buurt?
3. Sluit voornaamste mismatches op (bijvoorbeeld: te abstract, te formeel, lezer onduidelijk).

Twee verbeteringen per pas zijn meer waard dan tien gelijktijdige.
