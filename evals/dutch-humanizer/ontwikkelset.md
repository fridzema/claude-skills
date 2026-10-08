# Semantische regressiecases

Elke case heeft een verzoek, een input, de invarianten die moeten blijven, en wat de output wel en niet mag. Geef een agent die de skill test alleen **Verzoek** en **Input**; de rest is voor de beoordeling. Beoordeel volgens `tests/evaluation.md`.

Soort: **R** = herschrijven moet, **N** = negatief voorbeeld (niet of nauwelijks ingrijpen), **T** = vertalen, **C** = nieuwe tekst.

---

## 01 Al natuurlijke mail (N)

**Verzoek:** Kun je dit menselijker maken?
**Input:**
Hoi Mark,

Ik heb de offerte van Bakker Bouw doorgelezen. De prijs valt mee, maar ze rekenen de fundering apart en dat stond niet in hun eerste mail. Kun jij morgen bellen om te vragen wat dat kost? Ik ben zelf de hele dag op de bouwplaats in Zwolle.

Groet,
Ilse

**Invarianten:** alles.
**Wel:** (vrijwel) ongewijzigd.
**Niet:** woorden vervangen om iets te veranderen; nieuwe feiten.

## 02 Onzekerheid, voorwaarde, toezegging, bron (R)

**Verzoek:** Herschrijf dit natuurlijker, het klinkt te veel als ChatGPT.
**Input:**
Beste collega's,

Het is belangrijk om op te merken dat de migratie naar het nieuwe CRM mogelijk vertraging oploopt. Echter, als de leverancier de koppeling vóór 14 november oplevert, kunnen we de oorspronkelijke planning wellicht alsnog halen. Het datateam heeft toegezegd de testdata uiterlijk 7 november klaar te hebben. De exportfunctie wordt in deze fase nadrukkelijk niet meegenomen. Daarnaast is de nieuwe versie volgens Joost de enige optie die aan de AVG-eisen voldoet.

Met vriendelijke groet,
Priya

**Invarianten:** "mogelijk" en "wellicht" (onzekerheid), voorwaarde vóór 14 november, toezegging datateam uiterlijk 7 november, export niet mee, "volgens Joost", "de enige optie", aanhef en afsluiting.
**Niet:** stelliger worden; "Hoi" of "Groet".

## 03 Formele support-reply met u (R)

**Verzoek:** Maak dit antwoord minder AI.
**Input:**
Geachte heer De Vries,

Hartelijk dank voor uw bericht en uw geduld. Wij begrijpen volkomen dat dit een frustrerende situatie voor u is. Het lijkt erop dat uw factuur van september dubbel is verwerkt. Wij zullen het te veel betaalde bedrag binnen 10 werkdagen terugstorten op uw rekening. Mocht u nog vragen hebben, aarzel dan vooral niet om contact met ons op te nemen. Wij staan altijd voor u klaar!

Met vriendelijke groet,
Klantenservice WarmteNet

**Invarianten:** u, "lijkt", september, binnen 10 werkdagen, afzender, uitnodiging voor vragen.
**Niet:** een naam als afzender; je.

## 04 Belgisch-Nederlandse schoolbrief (R)

**Verzoek:** Kan je dit wat vlotter maken?
**Input:**
Beste ouders,

Graag willen wij u informeren over een belangrijke wijziging die een aanzienlijke impact heeft op het schoolleven van uw kind. Vanaf maandag 6 januari wordt de speelplaats heraangelegd. Gedurende deze periode dienen de leerlingen via de achteringang aan de Kerkstraat binnen te komen. Gelieve uw kind tijdig af te zetten. Schepen Van den Broeck zal de werken officieel openen. Voor vragen kan u terecht op het secretariaat of via gsm op 0471 23 45 67.

Met vriendelijke groeten,
Directie basisschool De Linde

**Invarianten:** nl-BE (gelieve, schepen, gsm, speelplaats, werken, kan u, groeten), datum, straat, nummer, verplichting ("dienen" wordt "moeten").
**Niet:** wethouder, schoolplein, mobiel.

## 05 Citaat, code, URL, bereik, dubbelzinnige datum (R)

**Verzoek:** Herschrijf dit natuurlijker: "Deze release vormt een cruciale mijlpaal in de evolutie van onze tool. De nieuwe vlag `--dry-run` stelt gebruikers in staat om naadloos wijzigingen te bekijken voordat ze worden toegepast. Zoals onze CTO het zei: "Dit is de release waar we op wachtten — eindelijk." Support is bereikbaar van 9-17 uur. De release staat gepland voor 03/04/2026. Documentatie: https://docs.example.org/cli#dry-run"
**Input:** zie verzoek.
**Invarianten:** de buitenste aanhalingstekens bakenen alleen de tekst af (de tekst zelf wordt herschreven); citaat letterlijk met gedachtestreepje, `--dry-run`, URL, 9-17 uur, 03/04/2026 ongewijzigd, "voordat ze worden toegepast".
**Niet:** de datum omzetten naar een maandnaam.

## 06 Stemvoorbeeld met eigen feiten (R)

**Verzoek:** Schrijf dit in mijn stijl. Voorbeeld van mij: "Vanochtend weer met Bobbie naar het strand bij Wijk aan Zee. Koud. Maar de koffie bij de strandtent maakt veel goed, en Bobbie vond een dode krab, dus die dag was ook geslaagd." Te herschrijven: "Thuiswerken biedt talloze voordelen voor zowel werknemers als werkgevers. Het stelt medewerkers in staat om een optimale balans te vinden tussen werk en privé. Bovendien draagt het bij aan een aanzienlijke reductie van reistijd."
**Invarianten:** veel voordelen, voor werknemers en werkgevers, balans werk en privé, minder reistijd.
**Niet:** Bobbie, strand, koffie, krab; verzonnen ervaring.

## 07 Vage LinkedIn-post blijft vaag (R)

**Verzoek:** Maak deze LinkedIn-post minder AI.
**Input:** 🚀 Trots! Ons team heeft het afgelopen jaar een ongelooflijke groei doorgemaakt. Het gaat niet om de cijfers, het gaat om de mensen. Dankzij hard werken, doorzettingsvermogen en teamgeest hebben we mijlpalen bereikt die we nooit voor mogelijk hielden. Wat is jouw grootste succes van dit jaar? 👇 #groei #teamwork
**Invarianten:** trots, grote groei, mensen boven cijfers, drie oorzaken, onverwachte mijlpalen, vraag aan de lezer (doel van de post).
**Niet:** cijfers, namen of voorbeelden verzinnen.

## 08 Vertaling met valse vrienden (T)

**Verzoek:** Translate this to natural Dutch, don't translate literally.
**Input:** It makes sense to start small. Eventually, we want every team to own their dashboards. In terms of budget, we have €12,500 for Q1. At the end of the day, this is not just about tooling — it's about culture. Let's dive in at the kickoff on Thursday, March 5.
**Invarianten:** klein beginnen, uiteindelijk eigen dashboards per team, €12.500, Q1, tooling én cultuur (cultuur weegt zwaarder), kickoff donderdag 5 maart.
**Niet:** "maakt zin", "eventueel", "in termen van", "aan het eind van de dag".

## 09 Korte Slack-update (R)

**Verzoek:** Klinkt als AI, fix even.
**Input:** Hallo allemaal! 👋 Ik wilde jullie even laten weten dat de deployment van vanmiddag helaas is uitgesteld vanwege een onverwacht probleem met de database-migratie. We zijn er druk mee bezig en houden jullie op de hoogte! Bedankt voor jullie geduld! 🙏
**Invarianten:** deployment vanmiddag uitgesteld, oorzaak database-migratie, onverwacht, we houden jullie op de hoogte.
**Niet:** tijdstip of oorzaak verzinnen.

## 10 Bericht aan manager met "tenzij" (R)

**Verzoek:** Maak dit minder stijf.
**Input:**
Beste Karin,

Graag maak ik van de gelegenheid gebruik om u te informeren dat wij het project naar verwachting op 1 december kunnen afronden, tenzij de leverancier de hardware later levert dan toegezegd. In dat geval schuift de oplevering minimaal twee weken op.

Met vriendelijke groet,
Tom

**Invarianten:** u, "naar verwachting", 1 december, "tenzij" met de voorwaarde, "minimaal twee weken".
**Niet:** "uiterlijk" of "zeker"; de voorwaarde weglaten.

## 11 Jira-ticket met acceptatiecriteria (R)

**Verzoek:** Herschrijf dit ticket in normaal Nederlands.
**Input:**
Als beheerder wil ik op een naadloze en efficiënte wijze een export van klantgegevens kunnen genereren, teneinde rapportages te faciliteren.

Acceptatiecriteria:
- De export bevat geen BSN.
- De export is alleen beschikbaar voor de rol Beheerder.
- Het bestandsformaat is CSV (UTF-8).
- Lege velden worden als lege string geëxporteerd, niet als NULL.

**Invarianten:** vier criteria, "geen BSN", "alleen" Beheerder, CSV (UTF-8), lege string niet NULL.
**Niet:** een criterium samenvoegen tot iets vagers; "BSN" weglaten.

## 12 Technische afweging (R)

**Verzoek:** Maak dit natuurlijker.
**Input:** Sessietokens worden elke 24 uur vernieuwd. Een mogelijke oplossing is de authenticatiedienst via een cronjob te herstarten, maar dan vallen alle actieve sessies weg. De vernieuwing gebeurt daarom zonder herstart en clients verversen automatisch.
**Invarianten:** 24 uur, de afgewezen optie (cronjob-herstart), het gevolg (actieve sessies weg), daarom zonder herstart, clients verversen automatisch.
**Niet:** de afweging schrappen.

## 13 Incidentrapport (R)

**Verzoek:** Herschrijf dit incidentverslag zodat het minder als AI leest.
**Input:** Op dinsdag 4 maart om 09:12 werd een significante verstoring van de betaalomgeving gedetecteerd. Om 09:40 werd vastgesteld dat de oorzaak vermoedelijk gelegen was in een verlopen TLS-certificaat. Na vervanging van het certificaat was de dienstverlening om 10:05 volledig hersteld. Er is geen klantdata gelekt. Team Platform zal uiterlijk 14 maart monitoring op certificaatverloop inrichten.
**Invarianten:** alle tijden en datums, "vermoedelijk", geen klantdata gelekt, Team Platform, uiterlijk 14 maart, volgorde.
**Niet:** "de oorzaak was" zonder voorbehoud; een andere eigenaar.

## 14 Informele klantreactie met voorwaarde en toezegging (R)

**Verzoek:** Maak dit antwoord natuurlijker.
**Input:** Hoi Sem, Wat ontzettend vervelend dat je pakket nog niet is aangekomen! We begrijpen helemaal hoe frustrerend dat is. Volgens de vervoerder wordt het uiterlijk donderdag bezorgd. Is het donderdag nog niet binnen, dan sturen we kosteloos een nieuw exemplaar. Groetjes, Team Fietsplek
**Invarianten:** je, "volgens de vervoerder", uiterlijk donderdag, voorwaarde en toezegging (kosteloos nieuw exemplaar), afzender.
**Niet:** "het wordt donderdag bezorgd" zonder bron.

## 15 Formele brief overheid (N/R)

**Verzoek:** Kun je dit natuurlijker maken?
**Input:** Indien u het niet eens bent met dit besluit, kunt u binnen zes weken na de dagtekening van dit besluit een bezwaarschrift indienen. Het bezwaarschrift dient te zijn ondertekend en moet ten minste uw naam, adres, de datum en de gronden van het bezwaar bevatten.
**Invarianten:** u, "indien", binnen zes weken na de dagtekening, ondertekening, vier verplichte onderdelen, "ten minste".
**Niet:** je; "na zes weken"; een onderdeel weglaten; informele toon.

## 16 Informeel bericht met "mits" (R)

**Verzoek:** Maak dit wat natuurlijker.
**Input:** Hey! Ik wilde je even laten weten dat ik zaterdag helaas niet kan komen, omdat mijn zus dan verhuist. Zondag zou wel kunnen, mits jij dan nog tijd hebt!
**Invarianten:** zaterdag niet, reden, zondag kan, voorwaarde "mits jij tijd hebt", informele toon.
**Niet:** formeler worden; "zondag kom ik".

## 17 Percentage en bron (R)

**Verzoek:** Herschrijf natuurlijker.
**Input:** Studies tonen aan dat 73% van de bedrijven dit doet.
**Invarianten:** 73%, toeschrijving aan studies.
**Wel:** eventueel een `Let op:` dat de bron ontbreekt.
**Niet:** "veel bedrijven"; een verzonnen studie.

## 18 Voorwaardelijke levering (R)

**Verzoek:** Maak deze mail minder stijf.
**Input:** Beste Anouk, Hierbij wil ik u graag informeren dat de klant de drukklare bestanden zal ontvangen zodra de goedkeuring van de afdeling Compliance binnen is. Wij verwachten deze goedkeuring in week 42. Met vriendelijke groet, Ruben
**Invarianten:** u, "zodra" plus Compliance-goedkeuring, "verwachten", week 42.
**Niet:** "de klant ontvangt de bestanden in week 42".

## 19 Onzekerheid (R)

**Verzoek:** Natuurlijker graag.
**Input:** Het lijkt erop dat de synchronisatie met het ERP-systeem vannacht is mislukt. Wij onderzoeken dit momenteel.
**Invarianten:** "lijkt", ERP-systeem, vannacht, onderzoek loopt.
**Niet:** "is mislukt" als feit.

## 20 Exacte deadline (R)

**Verzoek:** Maak dit minder formeel.
**Input:** Wij verzoeken u vriendelijk de gewijzigde artwork uiterlijk vrijdag om 17.00 uur aan te leveren.
**Invarianten:** uiterlijk, vrijdag, 17.00 uur, u.
**Niet:** "vrijdag"; "voor het weekend".

## 21 Termijn binnen (R)

**Verzoek:** Herschrijf dit in gewone taal.
**Input:** De aanvraag tot terugbetaling dient binnen 30 dagen na ontvangst van de factuur te worden ingediend.
**Invarianten:** binnen 30 dagen, na ontvangst van de factuur, verplichting.
**Niet:** "na 30 dagen".

## 22 Verantwoordelijkheden (R)

**Verzoek:** Kun je dit natuurlijker formuleren?
**Input:** Het is van essentieel belang dat de export wordt aangeleverd door het datateam, waarna de cijfers vóór verzending gecontroleerd dienen te worden door Finance.
**Invarianten:** datateam levert, Finance controleert, vóór verzending, volgorde.
**Niet:** "het datateam controleert"; de controle weglaten.

## 23 Ontkenning met uitzondering (R)

**Verzoek:** Maak dit klantvriendelijker.
**Input:** Deze prijswijziging heeft geen invloed op bestaande abonnementen, behalve op jaarabonnementen die na 1 maart zijn afgesloten.
**Invarianten:** geen invloed, uitzondering, jaarabonnementen, na 1 maart.
**Niet:** de uitzondering weglaten; "voor 1 maart".

## 24 Vakjargon (R)

**Verzoek:** Haal de AI-toon eruit.
**Input:** In het kader van onze robuuste releasestrategie zullen wij de hotfix via de CI-pipeline naar staging deployen; na een succesvolle smoke test wordt de pull request naar main gemerged.
**Invarianten:** hotfix, CI-pipeline, staging, smoke test, pull request, main, volgorde, voorwaarde "na een succesvolle".
**Niet:** "uitrollen naar de testomgeving"; "samenvoegen met de hoofdtak".

## 25 Lijst met vier aparte punten (R)

**Verzoek:** Maak dit minder AI.
**Input:**
Onze nieuwe werkwijze:
- **Snelheid:** Offertes gaan binnen 24 uur de deur uit.
- **Kwaliteit:** Elke offerte wordt door een tweede collega gecontroleerd.
- **Transparantie:** Klanten zien de status in het klantportaal.
- **Eigenaarschap:** Elke accountmanager is eindverantwoordelijk voor zijn eigen offertes.
**Invarianten:** vier punten met elk hun inhoud, binnen 24 uur, tweede collega, klantportaal, eindverantwoordelijk.
**Niet:** een punt laten vallen of samenvoegen tot iets anders.

## 26 Twee bronnen (R)

**Verzoek:** Natuurlijker graag.
**Input:** Volgens het RIVM is het risico op besmetting laag. De GGD adviseert desondanks om bij klachten thuis te blijven.
**Invarianten:** RIVM over risico, GGD over advies, "desondanks", "bij klachten".
**Niet:** de toeschrijving verwisselen of samenvoegen.

## 27 Technische vertaling (T)

**Verzoek:** Translate to natural Dutch.
**Input:** Do not delete the volume unless the backup has completed. The cleanup job runs at 2 AM UTC and retries up to three times.
**Invarianten:** verbod, "tenzij" of gelijkwaardig, back-up voltooid, 02:00 UTC, maximaal drie keer, "volume", "job".
**Niet:** "na de back-up mag je het volume verwijderen" als opdracht; "drie keer" zonder "maximaal".

## 28 Idiomatische vertaling (T)

**Verzoek:** Make this sound like natural Dutch.
**Input:** At the end of the day, it's a judgment call. Eventually we'll need a policy, but for now it's case by case.
**Invarianten:** uiteindelijk een afweging, later een beleid nodig, nu per geval.
**Niet:** "aan het eind van de dag", "eventueel".

## 29 Lange tekst met verwijzing tussen alinea's (R)

**Verzoek:** Herschrijf dit natuurlijker.
**Input:**
Alle medewerkers werken vanaf 1 april volgens het nieuwe roosterbeleid. Een uitzondering geldt voor medewerkers in de nachtdienst; zij blijven tot 1 juli in het oude rooster.

Het nieuwe beleid houdt in dat diensten uiterlijk vier weken van tevoren worden gepubliceerd. Ruilen is toegestaan, mits de teamleider vooraf akkoord geeft.

Voor de groep die onder de genoemde uitzondering valt, gelden de nieuwe ruilregels wel al vanaf 1 april.

**Invarianten:** 1 april, uitzondering nachtdienst tot 1 juli, uiterlijk vier weken, ruilen mits akkoord vooraf, de verwijzing in alinea 3 naar de nachtdienst, ruilregels voor hen al vanaf 1 april.
**Niet:** de verwijzing verliezen ("voor iedereen geldt...").

## 30 Al natuurlijke documentatie (N)

**Verzoek:** Humaniseer deze tekst.
**Input:** Maak een API-token aan onder Instellingen > Tokens. Stuur het token mee in de `Authorization`-header. Tokens zijn 90 dagen geldig.
**Invarianten:** alles.
**Wel:** ongewijzigd of nagenoeg.
**Niet:** de pijl of het menupad aanpassen.

## 31 Al natuurlijke Belgische mail (N)

**Verzoek:** Maak dit natuurlijker.
**Input:** Dag Lies, bedankt voor de nota. Ik betaal ze deze week nog. Gelieve het rekeningnummer nog eens te bevestigen, want ik vind het niet terug. Groetjes, Bart
**Invarianten:** alles, inclusief nl-BE-woorden.
**Niet:** "rekening" voor "nota", "Wil je" voor "Gelieve".

## 32 Zware AI-tekst met één feit (R, volledig)

**Verzoek:** Herschrijf dit volledig, het is echt te veel.
**Input:** In het huidige, snel veranderende digitale landschap is het van cruciaal belang om naadloos in te spelen op de behoeften van onze diverse klantenkring. Daarom zijn wij verheugd aan te kondigen dat onze webshop vanaf 1 januari ook in het Frans beschikbaar is. Dit markeert een belangrijke mijlpaal in onze internationale groeireis.
**Invarianten:** webshop, vanaf 1 januari, Frans, inspelen op klanten, het belang (belangrijke stap, internationale groei).
**Niet:** nieuwe talen, landen of cijfers.

## 33 Nuttig contrast (N/R)

**Verzoek:** Maak dit natuurlijker.
**Input:** De vertraging komt niet door de leverancier, maar door onze eigen goedkeuringsronde.
**Invarianten:** beide helften.
**Niet:** "De vertraging komt door onze goedkeuringsronde." zonder de correctie.

## 34 Citaat met AI-woorden (R)

**Verzoek:** Maak dit minder AI.
**Input:** De directeur zei bij de opening: "Dit is een cruciale mijlpaal in onze reis naar duurzaamheid." Daarnaast is het nieuwe pand voorzien van een breed scala aan duurzame innovaties, waaronder zonnepanelen en een warmtepomp.
**Invarianten:** citaat letterlijk, zonnepanelen, warmtepomp, "waaronder" (lijst niet volledig).
**Niet:** het citaat herschrijven.

## 35 Persoonlijker zonder verzonnen ervaring (R)

**Verzoek:** Maak dit persoonlijker.
**Input:** Thuiswerken vraagt om discipline. Een vaste werkplek en vaste werktijden helpen om werk en privé gescheiden te houden.
**Invarianten:** discipline, vaste werkplek, vaste werktijden, scheiding werk en privé.
**Wel:** ik- of je-vorm, een mening.
**Niet:** "Toen ik begon met thuiswerken..." of andere verzonnen ervaring.

## 36 Concreter zonder verzonnen bron (R)

**Verzoek:** Maak dit concreter.
**Input:** Uit onderzoek blijkt dat thuiswerkers productiever zijn.
**Invarianten:** toeschrijving aan onderzoek, de bewering.
**Wel:** een `Let op:` of vraag om de bron of cijfers.
**Niet:** een studie, jaar, instituut of percentage verzinnen.

## 37 Formeel blijft formeel (R)

**Verzoek:** Haal de AI-toon eruit.
**Input:** Geachte leden van de Raad van Bestuur, Hierbij doe ik u, conform uw verzoek, het geactualiseerde investeringsvoorstel toekomen. Het voorstel omvat een investering van € 2,4 miljoen, verdeeld over drie jaar. Graag licht ik het voorstel toe tijdens uw vergadering van 18 november. Hoogachtend, M. Jansen, CFO
**Invarianten:** formeel register, u, conform verzoek, € 2,4 miljoen, drie jaar, 18 november, ondertekening.
**Niet:** "Hoi", "je", "Groet".

## 38 Cijfers en eenheden (R)

**Verzoek:** Klinkt als AI, maak het gewoner.
**Input:** Wij zijn verheugd te kunnen melden dat de uptime in Q3 maar liefst 99,95% bedroeg (doelstelling: 99,9%). De gemiddelde responstijd bedroeg 180 ms.
**Invarianten:** 99,95%, Q3, doel 99,9%, 180 ms.
**Niet:** afronden; "boven het doel" zonder cijfers.

## 39 Waarschijnlijk en verplicht (R)

**Verzoek:** Maak dit Teams-bericht natuurlijker.
**Input:** Het is waarschijnlijk dat de audit in week 12 zal plaatsvinden. Deelname is verplicht voor alle teamleads.
**Invarianten:** waarschijnlijk, week 12, verplicht, alle teamleads.
**Niet:** "de audit is in week 12"; "deelname wordt verwacht".

## 40 Nieuwe mail uit bullets (C)

**Verzoek:** Schrijf hier een korte, natuurlijke mail van aan de klant.
**Input:**
- offerte verstuurd op 3 oktober
- klant wil eerst intern overleggen
- wij bellen maandag 14 oktober na
- contactpersoon: mevrouw Bos

**Invarianten:** 3 oktober, intern overleg, maandag 14 oktober nabellen, mevrouw Bos (u-vorm ligt voor de hand).
**Niet:** prijs, product, kortingen of andere verzonnen details.

## 41 Meerdere schrijfvoorbeelden, ander kanaal (C)

**Verzoek:** Schrijf in mijn stijl een Teams-bericht aan mijn team dat de retro van vrijdag verschuift naar maandag 10:00. Twee voorbeelden van mij: (1) mail aan mijn manager: "Hoi Ellen, korte update: de migratie loopt. Twee issues open, niks spannends. Vrijdag weet ik meer." (2) LinkedIn: "Drie jaar bij Kodo vandaag. Nog steeds geen spijt van de overstap. Wel van het koffieapparaat."
**Invarianten:** retro, van vrijdag naar maandag 10:00.
**Wel:** kort, droog, direct.
**Niet:** Ellen, migratie, Kodo, koffieapparaat; verzonnen reden voor de verschuiving.

## 42 Emoji in de stem van de schrijver (N)

**Verzoek:** Maak dit iets natuurlijker, maar het is gewoon een appje aan mijn team.
**Input:** Top gedaan vandaag allemaal 🎉 Morgen om 9 uur starten we met de oplevering, neem je laptop mee 💻
**Invarianten:** compliment, morgen 9 uur, oplevering, laptop meenemen, informele toon.
**Wel:** emoji mogen blijven.
**Niet:** formeel worden; emoji verplicht weghalen.


## 43 Inkorten met termijn (C), uit validatieset V20

**Verzoek:** Maak dit korter.
**Input:** Wij willen u er graag op wijzen dat het voor de goede orde van belang is dat u uw parkeervergunning uiterlijk 30 november verlengt. Indien u dit niet doet, vervalt uw vergunning per 1 december en kunt u niet meer in de wijk parkeren.
**Invarianten:** uiterlijk 30 november verlengen; gevolg: vervalt per 1 december; niet meer in de wijk parkeren; u-vorm
**Niet:** termijn weg; gevolg weg; toelichting als alleen opvulling wegviel.
**Herkomst:** validatieset V20, verplaatst op 2026-10-08 na gebruik voor reparatie.
