# Voorbeeld: zakelijk (email/notitie)

Zakelijk Nederlands is van nature direct. AI maakt er vaak een verzameling beleefdheidsformules en hedging van.

## Voor (AI-klinkend)

> Beste team,
>
> Ik hoop dat deze e-mail jullie in goede gezondheid bereikt. Ik wil graag van de gelegenheid gebruikmaken om jullie te informeren over enkele belangrijke ontwikkelingen met betrekking tot het Q2-project.
>
> Zoals jullie wellicht weten, hebben we de afgelopen periode aanzienlijke vooruitgang geboekt op diverse fronten. Het is vermeldenswaard dat het projectteam, ondanks uitdagingen op het gebied van resourcing, erin geslaagd is om de belangrijkste mijlpalen te realiseren. Daarnaast hebben we waardevolle inzichten opgedaan die zullen bijdragen aan toekomstige initiatieven.
>
> Echter, er zijn nog enkele aandachtspunten die nadere bespreking behoeven. Met betrekking tot de planning zou ik graag een aantal scenario's met jullie willen verkennen, teneinde tot een breed gedragen besluit te komen. Ik stel voor dat we hiervoor een meeting inplannen.
>
> Mochten jullie nog vragen of opmerkingen hebben, aarzel dan niet om contact met mij op te nemen. Ik kijk uit naar onze samenwerking en heb er alle vertrouwen in dat we samen tot mooie resultaten zullen komen.
>
> Met vriendelijke groet,
> Marieke

## Na, variant A: input bevat geen specifieke feiten

Gebruik deze variant als de input alleen vage formuleringen bevat ("vooruitgang", "uitdagingen", "aandachtspunten"). De rewrite blijft op hetzelfde abstractie-niveau, maar zonder AI-toon.

> Hoi team,
>
> Korte update over Q2 en een vraag over Q3.
>
> De belangrijkste mijlpalen staan. Een paar dingen liepen niet volgens plan; daar willen we volgende sprint op terugkomen.
>
> Voor Q3 wil ik twee opties met jullie doornemen:
>
> 1. Doorgaan met huidige scope.
> 2. Scope inkrimpen.
>
> Donderdag een halfuurtje plannen?
>
> Groet,
> Marieke

## Na, variant B: input bevat wel concrete feiten

Gebruik deze variant *alleen* als de gebruiker (in de input of als context) deze specifieke feiten heeft aangedragen: bijvoorbeeld dat de migratie twee weken eerder klaar was, dat de testfase is ingekort, en dat een meeting op donderdag 14:00 wordt voorgesteld.

> Hoi team,
>
> Korte update over Q2 en een vraag.
>
> De belangrijkste mijlpalen staan, ondanks de krappe bezetting. Wat goed liep: de migratie was twee weken eerder klaar dan gepland. Wat minder liep: we hebben de testfase ingekort, en daar moeten we volgende sprint nog op terugkomen.
>
> Voor de planning van Q3 wil ik twee opties met jullie doornemen:
>
> 1. Doorgaan met huidige scope, einde Q3 livegang.
> 2. Scope inkrimpen, livegang half augustus.
>
> Donderdag 14:00 een halfuur plannen?
>
> Groet,
> Marieke

## Welke patronen zijn hersteld

* **Assistent-tics / pleasantries**: "Ik hoop dat deze e-mail jullie in goede gezondheid bereikt", "aarzel dan niet contact op te nemen", "heb er alle vertrouwen in".
* **Vulzinnen**: "wil graag van de gelegenheid gebruikmaken", "met betrekking tot", "teneinde", "het is vermeldenswaard dat".
* **Hedging**: "wellicht", "enkele aandachtspunten die nadere bespreking behoeven".
* **Officialese**: "echter, ...", "breed gedragen besluit", "diverse fronten".
* **Vaag → concreet (alleen variant B)**: "aanzienlijke vooruitgang", "waardevolle inzichten" → vervangen door concrete feiten alleen als die feiten in de input stonden.
* **Geen call to action** → vervangen door specifiek voorstel (variant A: "donderdag een halfuurtje"; variant B: "donderdag 14:00 een halfuur").
* **Generieke positieve afsluiter**: "kijk uit naar onze samenwerking ... mooie resultaten" → weg.

## Aandachtspunt

Beslisregel **wanneer welke variant**:

- Input is vaag → variant A. Maak het direct, behoud abstractie-niveau.
- Input bevat concrete feiten of de gebruiker geeft die als context → variant B. Gebruik die feiten.
- Input is vaag, maar gebruiker vraagt om concreet te maken → vraag de gebruiker om de feiten. Verzin ze niet.

Behoud altijd: namen, datums, projectnamen, deadlines en concrete cijfers die in de input stonden.

**Dit is de belangrijkste regel van de skill**: een rewrite mag specifieker maken alleen waar de input dat toelaat. "Twee weken eerder", "donderdag 14:00", "einde Q3 livegang" zijn hallucinaties zodra ze niet uit de input komen, hoe goed ze ook leesbaar maken.
