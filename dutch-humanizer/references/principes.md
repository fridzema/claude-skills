# Principes

## Inhoud

- Deel 1: betekenis behouden (wat nooit mag, gevallen A-H, controle in twee richtingen, per taak)
- Deel 2: wat goed Nederlands is (principes 1-11)

Twee delen. Deel 1 bepaalt wat een herschrijving nooit mag veranderen. Deel 2 beschrijft wat goed Nederlands is. Deel 1 gaat altijd voor.

Gebaseerd op Taaladvies.net (Taalunie), Team Taaladvies, Rijksoverheid en Vlaamse overheid (klare taal). Zie [`bronnen.md`](bronnen.md).

# Deel 1: betekenis behouden

Semantische gelijkwaardigheid gaat voor stilistische verbetering. Een redacteur verandert hoe iets gezegd wordt, niet wat er gezegd wordt.

## Wat bij een gewone herschrijving nooit mag

- Een relevante bewering schrappen om de tekst korter te maken.
- De mate van zekerheid veranderen, in welke richting ook.
- Een ontkenning weghalen of toevoegen.
- De betekenis van een voorwaarde veranderen of een uitzondering schrappen.
- Veranderen wie iets doet of waarvoor verantwoordelijk is.
- Een toezegging of termijn wijzigen of laten vallen.
- Een oorzakelijk verband toevoegen dat de bron niet legt.
- Een mening als feit brengen, of een feit als mening.
- De bron van een uitspraak veranderen.
- Exacte hoeveelheden vager maken ("73%" wordt geen "veel").
- Technische informatie vereenvoudigen tot iets wat minder klopt.
- Ervaringen, emoties, feiten of citaten verzinnen.
- De communicatieve handeling veranderen: een voorstel wordt geen besluit, een vraag geen opdracht, een verwachting geen garantie, een verontschuldiging geen nieuwe toezegging.
- Een waarde aan een andere zaak koppelen, of een eenheid impliciet maken ("in 3 dagen" wordt niet "in 3" naast "11 werkdagen").
- Een onbewezen of vermoedelijk onjuiste bewering uit de bron als feit bevestigen of stilzwijgend corrigeren. Laat haar als bewering staan en meld een vermoedelijke fout in een `Let op:`.

Vraagt de gebruiker uitdrukkelijk om een samenvatting of om iets te schrappen, dan is dat een inhoudelijke bewerking. Doe dan wat gevraagd is en meld in één regel wat wegviel. Inkorten (`shorten`) is dat niet: daar verdwijnen alleen woorden en herhaling.

## Gevallen

**A. Technische afweging**
Bron: "Sessietokens worden elke 24 uur vernieuwd. Een mogelijke oplossing is de authenticatiedienst via een cronjob te herstarten, maar dan vallen alle actieve sessies weg. De vernieuwing gebeurt daarom zonder herstart en clients verversen automatisch."
Fout: "Sessietokens worden elke 24 uur vernieuwd en clients verversen automatisch."
Goed: "Sessietokens worden elke 24 uur vernieuwd. De authenticatiedienst via een cronjob herstarten kan ook, maar dan vallen alle actieve sessies weg. Daarom gebeurt de vernieuwing zonder herstart en verversen clients automatisch."
De afgewezen optie, het gevolg en het "daarom" zijn de reden voor het ontwerp. Ze blijven; alleen de formulering wordt gewoner.

**B. Hoeveelheden en bronnen**
Bron: "Studies tonen aan dat 73% van de bedrijven dit doet."
Fout: "Veel bedrijven doen dit." Het percentage en de toeschrijving zijn weg.
Goed: "Studies laten zien dat 73% van de bedrijven dit doet." Plus, als de bron ertoe doet: `Let op: welke studies? De bron ontbreekt.`
Verzin geen specifieke studie. Verander ook niet stilzwijgend de bewering; een aparte opmerking is beter.

**C. Voorwaarden**
Bron: "De klant ontvangt de bestanden zodra de goedkeuring binnen is."
Fout: "De klant ontvangt de bestanden."
Goed: "Zodra de goedkeuring binnen is, krijgt de klant de bestanden."
"Na goedkeuring" is te zwak: "zodra" zegt ook dat de levering direct volgt.

**D. Zekerheid**
Bron: "Het lijkt erop dat de synchronisatie is mislukt."
Fout: "De synchronisatie is mislukt."
Goed: "De synchronisatie lijkt mislukt."
Niet "waarschijnlijk mislukt": "het lijkt erop" gaat over aanwijzingen, "waarschijnlijk" is een inschatting van de kans. Dat zijn verschillende beweringen.

**E. Termijnen**
Bron: "Lever de wijziging uiterlijk vrijdag om 17.00 uur op."
Fout: "Lever de wijziging vrijdag op."
Goed: de bron zelf, ongewijzigd. Ze is al helder; "opleveren" is ook niet hetzelfde als "inleveren".

**F. Volgorde in de tijd**
Bron: "De aanvraag moet binnen 30 dagen worden ingediend."
Fout: "De aanvraag moet na 30 dagen worden ingediend."
Goed: de bron zelf, ongewijzigd. "Dien de aanvraag binnen 30 dagen in" maakt van een regel een opdracht aan de lezer; dat kan alleen als de lezer de aanvrager is.

**G. Communicatieve handeling**
Bron: "Zullen we donderdag om 14:00 overleggen?"
Fout: "We overleggen donderdag om 14:00." Een voorstel is een besluit geworden.
Goed: de vraag laten staan. "Kunnen we ..." is niet gelijkwaardig: dat vraagt eerder of het mogelijk is.

**H. Bewering uit de bron**
Bron: "Volgens de leverancier is de nieuwe versie volledig veilig."
Fout: "De nieuwe versie is volledig veilig." De bron is weg en de bewering is een feit geworden.
Goed: "Volgens de leverancier is de nieuwe versie volledig veilig."

## Controle in twee richtingen

1. **Output naar bron**: volgt elke bewering in de output uit de bron of de opdracht? Is niets stelliger, specifieker of verplichtender geworden?
2. **Bron naar output**: staat alle vereiste inhoud er nog, inclusief verbanden tussen alinea's, verwijzingen ("die uitzondering"), lijstonderdelen, de reikwijdte van ontkenningen en welke waarde bij welke zaak hoort?

## Per taak

- **rewrite**: alle bovenstaande regels.
- **shorten**: minder woorden en herhaling; feiten, voorwaarden en termijnen blijven. Inkorten is geen toestemming om inhoud te schrappen.
- **summarize**: alleen als de gebruiker uitdrukkelijk om een samenvatting vraagt. Je kiest wat blijft; wat je opneemt, klopt precies.
- **create**: elke feitelijke bewering moet herleidbaar zijn tot de aangeleverde context. Een mening of reactie mag als de stem erom vraagt; een feit, ervaring of citaat niet.
- **translate**: idiomatisch Nederlands met dezelfde beweringen en dezelfde verbanden ertussen. Zinsbouw en volgorde mogen veranderen. Een idioom vervang je door een Nederlands idioom met dezelfde betekenis, niet door een letterlijke vertaling.

## Aanpassing of inhoudelijke wijziging?

Geen inhoudelijke wijziging: zinsbouw, woordvolgorde, gewone synoniemen, samenvoegen of splitsen van zinnen, een lijst als lopende zin, een ambtelijk woord vervangen door een gewoon woord, een herhaling die niets toevoegt schrappen.

Wel een inhoudelijke wijziging: elk van de punten onder *Wat nooit mag*. Twijfel je, behandel het dan als inhoudelijk en houd het oorspronkelijke vast.

Je hoeft niet zin voor zin of woord voor woord gelijk te blijven. Het doel is dezelfde betekenis, niet dezelfde vorm.

# Deel 2: wat goed Nederlands is

Formulematige constructies weghalen is de helft van het werk. Wat overblijft is vaak nog steriel of plat. Deze principes geven het positieve model.

## 1. Lezer eerst

> Voor wie schrijf je? Wat weet die lezer al? Wat moet die lezer doen, weten of voelen na het lezen?

Natuurlijk Nederlands begint bij de lezer, niet bij de schrijver. Generieke tekst is geschreven voor "iemand in het algemeen". Goede tekst is geschreven voor een specifieke lezer in een specifieke situatie.

**Voor:** "Deze tool kan organisaties helpen om hun processen te optimaliseren, doordat hij de weekrapportage automatisch opstelt."
**Na:** "Deze tool stelt de weekrapportage automatisch op en kan organisaties zo helpen hun processen te verbeteren."

Het concrete voordeel staat nu vooraan; de bewering over processen blijft, met dezelfde voorzichtigheid ("kan").

## 2. Doel boven onderwerp

Iedere zin moet bijdragen aan het lezersdoel. Een tekst is geen verzameling waarheden over een onderwerp; het is gereedschap waarmee de lezer iets kan.

Een mail die om een beslissing vraagt, maakt de keuze vindbaar. Een handleiding laat zien wat de lezer moet doen. Een blog die een mening verkondigt, eindigt met de mening, niet met "spannende tijden liggen voor de deur".

Maakt de bron duidelijk wat de lezer moet doen, zet dat dan op een plek waar de lezer het vindt. Voeg zelf geen actie, uitleg of conclusie toe die niet uit de bron volgt.

## 3. Concreet boven abstract

Als je iets abstract kunt opschrijven, kun je het bijna altijd ook concreet. Concreet is bijna altijd beter, behalve waar abstractie expliciet doel is (filosofische tekst, juridische definities).

| Abstract | Concreet |
|---|---|
| "verbeterde gebruikservaring" | "drie klikken minder bij het inloggen" |
| "uitdagingen op het gebied van resourcing" | "twee mensen ziek, één ouderschapsverlof" |
| "operationele excellentie" | "facturatie binnen 5 dagen, foutpercentage onder 1%" |
| "transformatieve impact" | "we zijn van vier dagen naar één dag doorlooptijd gegaan" |

Belangrijke regel: **wees concreet over wat je weet, niet over wat je verzint**. De rechterkolom hierboven werkt alleen als de input die feiten bevat. Staan ze er niet, dan blijft de bewering zo algemeen als ze was (deel 1).

## 4. Belangrijkste eerst

In zakelijke, journalistieke en ambtelijke tekst helpt het de lezer als de kern vooraan staat (zie de checklist duidelijke tekst van Onze Taal). Dat is een leesadvies, geen kenmerk van "het" Nederlands.

**Voor:** "Naar aanleiding van de afgelopen kwartaalrapportage en de daaruit voortvloeiende inzichten met betrekking tot onze verkoopcijfers, zou ik graag voorstellen dat we het offertetraject inkorten van 11 naar 5 dagen."
**Na:** "Ik stel voor het offertetraject in te korten van 11 naar 5 dagen. Aanleiding is wat de laatste kwartaalrapportage over onze verkoopcijfers liet zien."

Het blijft een voorstel ("ik stel voor"), geen besluit ("ik wil" of "we korten in").

In blog/column mag je een aanloop nemen, maar dan bewust voor effect.

## 5. Ritme: variëren, niet uniformeren

Formulematige tekst heeft vaak zinnen van vergelijkbare lengte (allemaal middellang) of vergelijkbaar complex (allemaal hoofdzin + bijzin). Dat leest als een metronoom.

Goed lopende tekst wisselt af: een korte zin, dan een langere die de tijd neemt om iets ingewikkelds uit te leggen, dan weer een kortere. Afwisselen is iets anders dan fragmenten stapelen. Een rij zinnetjes van twee woorden is ook een patroon (zie `patronen.md`, patroon 2).

In zakelijke en technische tekst helpen korte zinnen; korter betekent wel nooit minder inhoud. In een blog of column is afwisseling in ritme belangrijker.

## 6. Past bij het kanaal

Geen tekst leest in vacuüm. Een Slack-bericht in beleidstaal valt op (te formeel). Een memo in chat-stijl valt op (te informeel). Match het kanaal.

| Kanaal | Korte kenmerken |
|---|---|
| Zakelijke e-mail | Aanhef, directe vraag of mededeling, korte alinea's, ondertekening |
| Slack/chat | Geen aanhef, korte zin, soms incompleet, urgentie eerst |
| Blog/column | Eerste persoon mag, aanloop mag, ritme-variatie mag |
| Productdocs | Imperatief ("Maak een token aan"), code-blokken, geen marketing |
| Beleids-/overheidstekst | Klare taal: korte zinnen, actief, gewone woorden |
| Vacaturetekst | Beschrijf de baan, niet de organisatie. Concreet over taken |
| LinkedIn-post | Eén punt per post, concreet, geen drieslag-cliché |
| Academische tekst | Neutraal, voorzichtig met claims, duidelijk over bron |

## 7. Actief boven passief, behalve waar het verbergt

Actief leest vaak directer: "Het rapport beschrijft X" tegenover "X wordt beschreven in het rapport". Het is geen doel op zich.

Uitzondering 1: als de actor onbekend, irrelevant of bewust verborgen is. "De server is herstart"; wie dat heeft gedaan is meestal niet relevant.

Uitzondering 2: in instructies waar de lezer de actor is, gebruik gebiedende wijs of "je"-vorm. "Maak een token aan" / "Je maakt een token aan" zijn beide goed; passief "Een token wordt aangemaakt" is steriel.

## 8. Samenhang en verwijzingen

Na herschikken moeten verwijzingen nog naar het juiste ding wijzen: "die uitzondering", "het genoemde bedrag", "zij". Verschuift een zin naar een andere alinea, controleer dan of "dit" en "deze" nog kloppen. Overgangswoorden ("daarom", "toch", "daarna") drukken een verband uit; voeg er geen toe dat de bron niet legt, en laat er geen weg die de bron wel legt.

## 9. Gewone woorden boven formele

Taaladvies: gebruik formele woorden spaarzaam. Liever "ook" dan "tevens". Liever "om" dan "teneinde". Liever "via" dan "middels". Liever "die" dan "welke".

Behoud een formele term alleen als die specifiek juridische, technische of vakbetekenis heeft. "De akte" in een notariële tekst is niet "het document"; het *is* een akte.

## 10. Eerlijk over wat je niet weet

Goede tekst zegt "ik weet het niet zeker, maar" waar dat zo is. Formulematige tekst schrijft "het is duidelijk dat" of "het is algemeen bekend dat", vaak zonder dat dat klopt.

Drie opties bij onzekerheid:

1. Behoud de onzekerheid die de bron uitdrukt ("volgens de planning, maar nog niet bevestigd").
2. Ontbreekt een bron of cijfer dat ertoe doet, meld dat in een `Let op:` of vraag erom.
3. Schrap een bewering alleen als de gebruiker dat vraagt (deel 1).

Dit is geen stijl-vraag maar een veiligheidsvraag. Verzonnen specifics zijn schadelijk.

## 11. Stem boven stijl-regels (waar het past)

Voor blog/column/persoonlijke tekst: de stem van de schrijver zelf werkt beter dan elke algemene "humanisering". Vraag (of gebruik, als de gebruiker een stuk eigen werk geeft) een schrijfvoorbeeld; zie [`stem-kalibratie.md`](stem-kalibratie.md).

Voor zakelijk/technisch/overheid: stem-vraag is minder relevant. Daar zijn helderheid, snelheid en juistheid de "stem".

## Hoe deze principes gebruiken

Niet als checklist. Eerder als kalibratie-bril:

1. Lees je rewrite hardop.
2. Vraag jezelf per principe: ben ik hier in de buurt?
3. Herstel de grootste afwijkingen (bijvoorbeeld: te abstract, te formeel, lezer onduidelijk).

Twee verbeteringen per pas zijn meer waard dan tien gelijktijdige. Een zin die al goed is, laat je staan.
