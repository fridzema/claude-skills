# Bronnen: hiërarchie van Nederlandstalige taaladvies

Bij twijfel over een spelling, woordkeuze of stijlvraag: gebruik deze hiërarchie. Hogere bronnen winnen van lagere.

## Niveau 1: officiële norm

**Woordenlijst Nederlandse Taal** ("Het Groene Boekje").
- Officiële spelling van de Nederlandse Taalunie.
- Bron voor: spelling, samenstellingen, koppeltekens bij klinkerbotsing en gelijke medeklinkers, voltooide deelwoorden.
- [woordenlijst.org](https://woordenlijst.org)

**Taaladvies.net** (Taalunie).
- Online vraagbaak voor de officiële standaardtaal.
- Bron voor: stijl, woordkeuze, leestekens, formulering. Markeert zaken als "standaardtaal in NL/BE/algemeen".
- [taaladvies.net](https://taaladvies.net)

## Niveau 2: register-specifieke gezaghebbende stijlbronnen

**Team Taaladvies** (Taalunie blog/redactie).
- Stijl- en advies-content; toelichting bij Taaladvies.net-beslissingen.
- Vooral nuttig bij contextuele vragen ("wanneer wel/geen leesteken?").

**Rijksoverheid: Klare taal richtlijnen**.
- Voor publieke communicatie en overheidstekst.
- Korte zinnen, actief, gewone woorden, lezer-eerst.
- [rijksoverheid.nl/onderwerpen/klare-taal](https://www.rijksoverheid.nl) (zoek op "klare taal").

**Vlaamse Overheid: Heerlijk helder**.
- Vlaams equivalent van klare taal.
- Vergelijkbare principes; bron bij Belgisch-Nederlandse overheidstekst.

## Niveau 3: vaktechnische woordenboeken en gidsen

- **Van Dale** voor moderne woordbetekenis en register-labels.
- **Onze Taal** (vereniging) voor stijlvragen, idioom en frequente twijfelgevallen.
- **Genootschap Onze Taal**: blog en advies-content.

Deze bronnen volgen Taalunie maar vullen aan op nuance, gebruik en context.

## Niveau 4: dit repository

**`patronen.md`**: gestructureerde catalogus van AI-tells in Nederlandstalige output.
**`principes.md`**: positief stijlmodel.
**`locale.md`**: nl-NL/nl-BE-conventies.
**`stem-kalibratie.md`**: voice-matching workflow.
**`voorbeeld-*.md`**: register-specifieke voor/na-voorbeelden.

Deze leggen geen norm op die in conflict komt met niveaus 1-3. Ze codificeren toepassing op AI-output en huisstijl-keuzes (bijvoorbeeld: hard zero em-dashes; zie `SKILL.md` "Hard regels").

## Niveau 5: door gebruiker aangeleverde context

Schrijfvoorbeeld of style-guide door de gebruiker aangeleverd, voor stem-imitatie of huisstijl-naleving. Wint binnen de scope die de gebruiker definieert (een specifieke tekst of doelgroep), maar niet over niveaus 1-3 heen wanneer die direct conflicteren met taalnorm.

Voorbeeld: gebruiker zegt "schrijf zoals dit voorbeeld". Voorbeeld gebruikt consequent "welke" als betrekkelijk vnw. Vraag jezelf:
- Is dit bewuste stijl van de schrijver? Imiteer.
- Is dit een tic die de schrijver zelf zou willen verwijderen? Niet imiteren.

Bij twijfel: imiteer en noteer; niet ongevraagd corrigeren.

## Conflict-resolutie

Als bronnen verschillen:

1. **nl-NL of nl-BE expliciet?** Volg de regionale variant (Taalunie labelt expliciet wat "standaardtaal in BE" of "standaardtaal in NL" is).
2. **Officiële norm vs. moderne praktijk?** Voor neutrale tekst: officieel. Voor casual/blog: vraag jezelf wat de doelgroep verwacht.
3. **Dit repository vs. Taalunie?** Taalunie wint. Pas dit repo aan bij conflict.

## Cite-praktijk in skill-output

De skill levert herschreven tekst, geen bronvermeldingen. Cite uitsluitend als:
- De gebruiker er expliciet om vraagt.
- De skill een specifieke regel-keuze moet uitleggen ("ik heb 'welke' vervangen door 'die' omdat Taaladvies dit voorschrijft voor neutraal register").

In andere gevallen: pas de regel toe, zonder bron-vermelding in de output.
