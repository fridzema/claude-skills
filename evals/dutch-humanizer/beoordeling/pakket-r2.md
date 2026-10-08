# Beoordelingspakket run 2

## V01 (mail, taak: rewrite)

**Verzoek:** Kun je deze mail natuurlijker maken?

**Input:**
Beste Johan,

Graag zou ik willen informeren of het wellicht mogelijk zou zijn om de evaluatie van het project te verplaatsen naar dinsdag 12 november. Mijn voorstel zou zijn om hiervoor 45 minuten te reserveren. Zou u kunnen aangeven of dit voor u schikt?

Met vriendelijke groet,
Anouk
**Invarianten:** vraag/voorstel blijft vraag of voorstel, geen besluit; dinsdag 12 november; 45 minuten; u-vorm; aanhef en afsluiting

**Niet:** 'We verplaatsen de evaluatie' als besluit; je-vorm

### Output X

````text
Beste Johan,

Zou het mogelijk zijn om de projectevaluatie te verplaatsen naar dinsdag 12 november? Ik stel voor om er 45 minuten voor te reserveren. Kunt u laten weten of dat schikt?

Met vriendelijke groet,
Anouk
````

### Output Y

````text
Beste Johan,

Is het mogelijk om de projectevaluatie te verplaatsen naar dinsdag 12 november? Ik stel voor om er 45 minuten voor te reserveren. Komt dat u uit?

Met vriendelijke groet,
Anouk
````

### Output Z

````text
Beste Johan,

Zou het mogelijk zijn om de projectevaluatie te verplaatsen naar dinsdag 12 november? Ik stel voor om daar 45 minuten voor te reserveren. Kunt u laten weten of dat u schikt?

Met vriendelijke groet,
Anouk
````

## V02 (klantreactie, taak: rewrite)

**Verzoek:** Maak dit antwoord minder stijf.

**Input:**
Beste meneer Visser,

Onze oprechte excuses voor de vertraging van uw bestelling. Op dit moment kunnen wij helaas nog niet aangeven wanneer het pakket bij u zal worden bezorgd. Zodra wij meer informatie van de vervoerder ontvangen, zullen wij u hiervan per e-mail op de hoogte stellen.

Met vriendelijke groet,
Klantenservice Tuinwereld
**Invarianten:** excuses blijft excuses, geen nieuwe toezegging; bezorgmoment onbekend; zodra informatie van vervoerder komt: bericht per e-mail; u-vorm; afzender

**Niet:** een verzonnen bezorgdatum of termijn; 'we zorgen dat het snel komt' als nieuwe belofte

### Output X

````text
Beste meneer Visser,

Excuses voor de vertraging van uw bestelling. We kunnen helaas nog niet zeggen wanneer het pakket bij u wordt bezorgd. Zodra we meer horen van de vervoerder, laten we het u per e-mail weten.

Met vriendelijke groet,
Klantenservice Tuinwereld
````

### Output Y

````text
Beste meneer Visser,

Het spijt ons dat uw bestelling vertraging heeft. We kunnen op dit moment helaas nog niet zeggen wanneer het pakket bij u wordt bezorgd. Zodra we meer horen van de vervoerder, laten we het u per e-mail weten.

Met vriendelijke groet,
Klantenservice Tuinwereld
````

### Output Z

````text
Beste meneer Visser,

Sorry dat uw bestelling vertraging heeft. We weten helaas nog niet wanneer het pakket bij u wordt bezorgd. Zodra we meer horen van de vervoerder, laten we het u per e-mail weten.

Met vriendelijke groet,
Klantenservice Tuinwereld
````

## V03 (chat, taak: rewrite)

**Verzoek:** Klinkt stijf, maak er een normaal Teams-bericht van.

**Input:**
Hallo allemaal, ik wil jullie graag informeren dat het erop lijkt dat de nightly build faalt op de integratietests. Ik zal hier vanmiddag naar kijken en jullie op de hoogte houden.
**Invarianten:** 'lijkt' (aanwijzing, niet zeker en niet 'waarschijnlijk'); nightly build; integratietests; vanmiddag kijken; op de hoogte houden

**Niet:** 'de build faalt' als zekerheid; 'waarschijnlijk'

### Output X

````text
Hoi allemaal, de nightly build lijkt te falen op de integratietests. Ik kijk er vanmiddag naar en hou jullie op de hoogte.
````

### Output Y

````text
Hoi allemaal, de nightly build lijkt te falen op de integratietests. Ik kijk er vanmiddag naar en hou jullie op de hoogte.
````

### Output Z

````text
Hoi allemaal, de nightly build lijkt te falen op de integratietests. Ik kijk er vanmiddag naar en hou jullie op de hoogte.
````

## V04 (technische instructie, taak: rewrite)

**Verzoek:** Herschrijf deze instructie natuurlijker.

**Input:**
Om de stabiliteit te waarborgen, dient de waarde van `MAX_RETRIES` in het bestand `config/app.yaml` te worden ingesteld op 3. Het is van belang om op te merken dat deze waarde niet hoger dan 5 mag zijn, aangezien de upstream-API anders requests gaat blokkeren. Herstart daarna de service met:

```bash
systemctl restart orders-api
```
**Invarianten:** MAX_RETRIES op 3; config/app.yaml; niet hoger dan 5; reden: upstream-API blokkeert anders; codeblok letterlijk; herstart na de wijziging

**Niet:** code of pad gewijzigd; reden weggelaten; 'maximaal 3'

### Output X

````text
Zet voor de stabiliteit `MAX_RETRIES` in `config/app.yaml` op 3. Hoger dan 5 mag niet, want dan gaat de upstream-API requests blokkeren. Herstart daarna de service met:

```bash
systemctl restart orders-api
```
````

### Output Y

````text
Zet `MAX_RETRIES` in `config/app.yaml` op 3, zodat de service stabiel blijft. Ga niet hoger dan 5, want dan gaat de upstream-API requests blokkeren. Herstart daarna de service:

```bash
systemctl restart orders-api
```
````

### Output Z

````text
Zet voor de stabiliteit `MAX_RETRIES` in `config/app.yaml` op 3. Ga niet hoger dan 5, want anders gaat de upstream-API requests blokkeren. Herstart daarna de service:

```bash
systemctl restart orders-api
```
````

## V05 (Jira-ticket, taak: rewrite)

**Verzoek:** Maak dit ticket leesbaarder.

**Input:**
Als beheerder wil ik op een efficiënte wijze gebruikers kunnen deactiveren, teneinde de beveiliging te waarborgen.

Acceptatiecriteria:
- Gedeactiveerde gebruikers kunnen niet meer inloggen.
- Deactiveren is alleen mogelijk voor de rol Beheerder.
- Een gebruiker wordt niet verwijderd, tenzij de beheerder dit expliciet bevestigt.
- Er kunnen maximaal 50 gebruikers tegelijk worden gedeactiveerd.
**Invarianten:** vier criteria; niet meer inloggen; alleen Beheerder; niet verwijderd tenzij expliciete bevestiging; maximaal 50 tegelijk

**Niet:** 'tenzij' omgezet in een andere voorwaarde; een criterium samengevoegd of weg

### Output X

````text
Als beheerder wil ik gebruikers efficiënt kunnen deactiveren, zodat de beveiliging op orde blijft.

Acceptatiecriteria:
- Gedeactiveerde gebruikers kunnen niet meer inloggen.
- Alleen gebruikers met de rol Beheerder kunnen deactiveren.
- Een gebruiker wordt pas verwijderd als de beheerder dat expliciet bevestigt.
- Je kunt maximaal 50 gebruikers tegelijk deactiveren.
````

### Output Y

````text
Als beheerder wil ik gebruikers efficiënt kunnen deactiveren, om de beveiliging te waarborgen.

Acceptatiecriteria:
- Gedeactiveerde gebruikers kunnen niet meer inloggen.
- Alleen de rol Beheerder kan gebruikers deactiveren.
- Een gebruiker wordt alleen verwijderd als de beheerder dat expliciet bevestigt.
- Er kunnen maximaal 50 gebruikers tegelijk worden gedeactiveerd.
````

### Output Z

````text
Als beheerder wil ik gebruikers efficiënt kunnen deactiveren, om de beveiliging te waarborgen.

Acceptatiecriteria:
- Gedeactiveerde gebruikers kunnen niet meer inloggen.
- Alleen de rol Beheerder kan gebruikers deactiveren.
- Een gebruiker wordt alleen verwijderd als de beheerder dat expliciet bevestigt.
- Er kunnen maximaal 50 gebruikers tegelijk worden gedeactiveerd.
````

## V06 (vertaling, taak: translate)

**Verzoek:** Translate this into natural Dutch, not literally.

**Input:**
Refunds are processed within 14 days, unless the item was damaged by the customer. The maximum refund is $1,250.00 per order. Please keep your receipt.
**Invarianten:** binnen 14 dagen; tenzij door klant beschadigd; maximaal $1.250,00 (of $1250) per bestelling; bon bewaren als verzoek

**Niet:** 'na 14 dagen'; bedrag veranderd; 'mits'

### Output X

````text
Terugbetalingen worden binnen 14 dagen verwerkt, tenzij het artikel door de klant is beschadigd. Per bestelling wordt maximaal $ 1.250,00 terugbetaald. Bewaar uw kassabon.
````

### Output Y

````text
Terugbetalingen verwerken we binnen 14 dagen, behalve als de klant het artikel zelf heeft beschadigd. Per bestelling betalen we maximaal $ 1.250,00 terug. Bewaar uw aankoopbon goed.
````

### Output Z

````text
Terugbetalingen worden binnen 14 dagen verwerkt, behalve als het artikel door de klant is beschadigd. Per bestelling krijgt u maximaal $ 1.250,00 terug. Bewaar uw aankoopbewijs.
````

## V07 (formele brief, taak: rewrite)

**Verzoek:** Kun je dit iets vriendelijker formuleren?

**Input:**
Geachte heer, mevrouw,

Indien u het niet eens bent met dit besluit, kunt u binnen zes weken na de dagtekening van deze brief schriftelijk bezwaar maken. Uw bezwaarschrift dient ten minste uw naam, adres, handtekening en de reden van uw bezwaar te bevatten.

Hoogachtend,
Gemeente Zwolle
**Invarianten:** u-vorm, formeel; voorwaarde (indien/als u het niet eens bent); binnen zes weken na dagtekening; schriftelijk; vier verplichte onderdelen, ten minste; afsluiting en afzender

**Niet:** je-vorm; 'na zes weken'; onderdeel weg

### Output X

````text
Geachte heer, mevrouw,

Bent u het niet eens met dit besluit? Dan kunt u binnen zes weken na de datum van deze brief schriftelijk bezwaar maken. Vermeld in uw bezwaarschrift in ieder geval uw naam, uw adres en de reden van uw bezwaar, en zet er uw handtekening onder.

Hoogachtend,
Gemeente Zwolle
````

### Output Y

````text
Geachte heer, mevrouw,

Bent u het niet eens met dit besluit? Dan kunt u binnen zes weken na de datum van deze brief schriftelijk bezwaar maken. Zet in uw bezwaarschrift in elk geval uw naam, adres, handtekening en de reden van uw bezwaar.

Hoogachtend,
Gemeente Zwolle
````

### Output Z

````text
Geachte heer, mevrouw,

Bent u het niet eens met dit besluit? Dan kunt u binnen zes weken na de datum van deze brief schriftelijk bezwaar maken. Zet in uw bezwaarschrift in elk geval uw naam, uw adres en de reden van uw bezwaar, en onderteken het.

Met vriendelijke groet,
Gemeente Zwolle
````

## V08 (stemvoorbeeld, taak: rewrite)

**Verzoek:** Herschrijf dit in mijn stijl. Twee voorbeelden van mij: (1) "Kort update: migratie draait. Nog twee issues open, niks engs. Morgen meer." (2) "Vandaag mijn laatste dag bij Fietsplek. Fijne club, slechte koffie." Tekst: "Graag informeer ik u dat de nieuwe versie van het klantportaal per maandag beschikbaar zal zijn. Gebruikers dienen opnieuw in te loggen. Bij vragen kunt u contact opnemen met de servicedesk."

**Input:**
zie verzoek
**Invarianten:** nieuwe versie klantportaal; per maandag; opnieuw inloggen (verplichting); vragen naar servicedesk; korte droge stijl

**Niet:** Fietsplek, koffie, migratie, issues; verzonnen details

### Output X

````text
Nieuwe versie klantportaal staat maandag live. Iedereen moet opnieuw inloggen. Vragen? Servicedesk.
````

### Output Y

````text
Per maandag staat de nieuwe versie van het klantportaal klaar. Gebruikers moeten wel opnieuw inloggen. Vragen? Neem contact op met de servicedesk.
````

### Output Z

````text
Vanaf maandag staat de nieuwe versie van het klantportaal klaar. Gebruikers moeten wel opnieuw inloggen. Vragen? Neem contact op met de servicedesk.
````

## V09 (al goed nl-BE, taak: rewrite)

**Verzoek:** Maak dit natuurlijker.

**Input:**
Dag Inge, bedankt voor je mail. Ik bezorg je de documenten morgen voor de middag. Laat gerust iets weten als er nog iets ontbreekt. Groetjes, Wim
**Invarianten:** ongewijzigd of vrijwel ongewijzigd; nl-BE 'bezorg' blijft

**Niet:** 'bezorg' naar 'stuur' of 'lever'; toelichting dat er niets veranderde

### Output X

````text
Dag Inge, bedankt voor je mail. Ik bezorg je de documenten morgen voor de middag. Laat gerust iets weten als er nog iets ontbreekt. Groetjes, Wim
````

### Output Y

````text
Dag Inge, bedankt voor je mail. Ik bezorg je de documenten morgen voor de middag. Laat gerust iets weten als er nog iets ontbreekt. Groetjes, Wim
````

### Output Z

````text
Dag Inge, bedankt voor je mail. Ik bezorg je de documenten morgen voor de middag. Laat gerust iets weten als er nog iets ontbreekt. Groetjes, Wim

Deze tekst leest al natuurlijk; er viel niets te verbeteren.
````

## V10 (al goed technisch, taak: rewrite)

**Verzoek:** Humaniseer deze tekst.

**Input:**
Draai `make migrate` voordat je de app start. De migratie duurt ongeveer twee minuten en is niet terug te draaien.
**Invarianten:** ongewijzigd of vrijwel ongewijzigd; make migrate voor start; ongeveer twee minuten; niet terug te draaien

**Niet:** 'ongeveer' weg; onomkeerbaarheid weg

### Output X

````text
Draai `make migrate` voordat je de app start. De migratie duurt ongeveer twee minuten en is niet terug te draaien.
````

### Output Y

````text
Draai `make migrate` voordat je de app start. De migratie duurt ongeveer twee minuten en is niet terug te draaien.

Deze tekst leest al natuurlijk; er viel niets te verbeteren.
````

### Output Z

````text
Draai `make migrate` voordat je de app start. De migratie duurt ongeveer twee minuten en is niet terug te draaien.
````

## V11 (nl-BE, taak: rewrite)

**Verzoek:** Kan je dit wat vlotter maken?

**Input:**
Geachte klant, gelieve het ingevulde formulier ons te bezorgen vóór 15 maart. Indien u vragen heeft, kan u ons bereiken op het nummer 03 123 45 67 tijdens de kantooruren.
**Invarianten:** gelieve of gelijkwaardig verzoek; bezorgen (nl-BE); vóór 15 maart; kan u (nl-BE); nummer letterlijk; tijdens kantooruren

**Niet:** omzetting naar nl-NL ('kunt u', 'sturen' is toegestaan maar niet nodig); datum veranderd

### Output X

````text
Beste klant, bezorg ons het ingevulde formulier graag vóór 15 maart. Hebt u vragen? Bel ons dan tijdens de kantooruren op 03 123 45 67.
````

### Output Y

````text
Geachte klant, gelieve ons het ingevulde formulier vóór 15 maart te bezorgen. Hebt u vragen? Bel ons dan tijdens de kantooruren op 03 123 45 67.
````

### Output Z

````text
Geachte klant, gelieve ons het ingevulde formulier te bezorgen vóór 15 maart. Heeft u vragen? Dan kan u ons tijdens de kantooruren bereiken op het nummer 03 123 45 67.
````

## V12 (nl-BE school, taak: rewrite)

**Verzoek:** Maak dit minder stijf.

**Input:**
Beste ouders, graag delen wij u mee dat de leerlingen hun rapport ontvangen op vrijdag 20 december. Proficiat aan alle leerlingen voor hun inzet dit trimester. Wij wensen u alvast een fijne kerstvakantie.
**Invarianten:** vrijdag 20 december; rapport; proficiat (nl-BE); trimester; u-vorm naar ouders; kerstwens

**Niet:** 'gefeliciteerd' afgedwongen; 'je'

### Output X

````text
Beste ouders, op vrijdag 20 december krijgen de leerlingen hun rapport. Proficiat aan alle leerlingen voor hun inzet dit trimester. Wij wensen u alvast een fijne kerstvakantie.
````

### Output Y

````text
Beste ouders,

Op vrijdag 20 december krijgen de leerlingen hun rapport. Proficiat aan alle leerlingen voor hun inzet dit trimester. Wij wensen u alvast een fijne kerstvakantie.
````

### Output Z

````text
Beste ouders, op vrijdag 20 december krijgen de leerlingen hun rapport. Proficiat aan alle leerlingen voor hun inzet dit trimester. We wensen u alvast een fijne kerstvakantie.
````

## V13 (nl-BE gemeente, taak: rewrite)

**Verzoek:** Herschrijf dit natuurlijker.

**Input:**
Het college van burgemeester en schepenen nodigt u uit op de nieuwjaarsreceptie in het gemeentehuis op zondag 12 januari om 11 uur. Schepen De Smet zal er een toespraak houden.
**Invarianten:** burgemeester en schepenen; schepen De Smet; zondag 12 januari 11 uur; gemeentehuis; uitnodiging

**Niet:** 'wethouder'

### Output X

````text
Het college van burgemeester en schepenen nodigt u uit op de nieuwjaarsreceptie op zondag 12 januari om 11 uur in het gemeentehuis. Schepen De Smet houdt er een toespraak.
````

### Output Y

````text
Het college van burgemeester en schepenen nodigt u graag uit op de nieuwjaarsreceptie op zondag 12 januari om 11 uur in het gemeentehuis. Schepen De Smet houdt er een toespraak.
````

### Output Z

````text
Het college van burgemeester en schepenen nodigt u uit op de nieuwjaarsreceptie op zondag 12 januari om 11 uur in het gemeentehuis. Schepen De Smet houdt er een toespraak.
````

## V14 (je/u, taak: rewrite)

**Verzoek:** Maak dit consistenter en natuurlijker.

**Input:**
Bedankt voor uw aanvraag. Je ontvangt binnen twee werkdagen een bevestiging per e-mail. Als jouw gegevens niet kloppen, kunt u ons bellen.
**Invarianten:** één aanspreekvorm (u ligt voor de hand); binnen twee werkdagen; bevestiging per e-mail; voorwaarde gegevens kloppen niet: bellen

**Niet:** mix van je en u; 'twee dagen'

### Output X

````text
Bedankt voor uw aanvraag. U ontvangt binnen twee werkdagen een bevestiging per e-mail. Kloppen uw gegevens niet? Bel ons dan.
````

### Output Y

````text
Bedankt voor uw aanvraag. U ontvangt binnen twee werkdagen een bevestiging per e-mail. Kloppen uw gegevens niet? Bel ons dan.
````

### Output Z

````text
Bedankt voor uw aanvraag. U ontvangt binnen twee werkdagen een bevestiging per e-mail. Kloppen uw gegevens niet? Dan kunt u ons bellen.
````

## V15 (anglicismen, taak: rewrite)

**Verzoek:** Haal het Engels-Nederlands eruit.

**Input:**
We moeten de openstaande issues adresseren en de deliverables alignen met de stakeholders, zodat we de deadline van 1 juni kunnen halen.
**Invarianten:** openstaande problemen aanpakken; resultaten afstemmen met betrokkenen; doel: deadline 1 juni halen

**Niet:** 1 juni weg; nieuwe acties

### Output X

````text
We moeten de openstaande punten aanpakken en met de belanghebbenden afstemmen wat we opleveren, zodat we de deadline van 1 juni kunnen halen.
````

### Output Y

````text
We moeten de openstaande punten aanpakken en met de betrokkenen afstemmen wat we opleveren, zodat we de deadline van 1 juni halen.
````

### Output Z

````text
We moeten de openstaande punten aanpakken en met de betrokkenen afstemmen wat we opleveren, zodat we de deadline van 1 juni kunnen halen.
````

## V16 (dubbele punt, taak: rewrite)

**Verzoek:** Corrigeer en verbeter dit.

**Input:**
Let op: De wijziging geldt alleen voor nieuwe klanten. Bestaande klanten: Zij behouden hun huidige tarief tot 31 december.
**Invarianten:** kleine letter na dubbele punt bij verklaring; alleen nieuwe klanten; bestaande klanten behouden tarief tot 31 december

**Niet:** 'alleen' weg; datum veranderd

### Output X

````text
Let op: de wijziging geldt alleen voor nieuwe klanten. Bestaande klanten behouden hun huidige tarief tot 31 december.
````

### Output Y

````text
Let op: de wijziging geldt alleen voor nieuwe klanten. Bestaande klanten behouden hun huidige tarief tot 31 december.
````

### Output Z

````text
Let op: de wijziging geldt alleen voor nieuwe klanten. Bestaande klanten behouden hun huidige tarief tot 31 december.
````

## V17 (mits, taak: rewrite)

**Verzoek:** Formuleer dit natuurlijker.

**Input:**
U ontvangt 10% korting, mits u de factuur voor 1 mei betaalt.
**Invarianten:** 10% korting; voorwaarde: alleen als u voor 1 mei betaalt

**Niet:** 'tenzij'; voorwaarde zwakker ('als' is acceptabel, 'en' niet); percentage veranderd

### Output X

````text
Betaalt u de factuur vóór 1 mei, dan krijgt u 10% korting.
````

### Output Y

````text
U krijgt 10% korting als u de factuur voor 1 mei betaalt.
````

### Output Z

````text
U ontvangt 10% korting, mits u de factuur voor 1 mei betaalt.
````

## V18 (samenstellingen, taak: rewrite)

**Verzoek:** Maak hier correct en vlot Nederlands van.

**Input:**
De project manager heeft de klant ervaring onderzocht. Uit de data analyse blijkt dat 62 procent van de klanten tevreden is.
**Invarianten:** projectmanager; klantervaring; data-analyse; 62 procent; onderzocht

**Niet:** percentage veranderd; 'meer dan de helft'

### Output X

````text
De projectmanager heeft de klantervaring onderzocht. Uit de data-analyse blijkt dat 62 procent van de klanten tevreden is.
````

### Output Y

````text
De projectmanager heeft de klantervaring onderzocht. Uit de data-analyse blijkt dat 62 procent van de klanten tevreden is.
````

### Output Z

````text
De projectmanager heeft de klantervaring onderzocht. Uit de data-analyse blijkt dat 62 procent van de klanten tevreden is.
````

## V19 (samenvatting, taak: summarize)

**Verzoek:** Vat dit samen in twee zinnen.

**Input:**
In het derde kwartaal steeg de omzet met 8% tot € 4,2 miljoen. De kosten stegen met 3%, vooral door hogere energieprijzen. Het aantal klanten groeide van 1.200 naar 1.350. Voor het vierde kwartaal verwacht de directie een vergelijkbare groei, mits de energieprijzen stabiel blijven.
**Invarianten:** hooguit twee zinnen; wat erin staat klopt precies; geen nieuwe feiten; verwachting blijft verwachting

**Niet:** onjuiste cijfers; verwachting als zekerheid; voorwaarde omgedraaid

### Output X

````text
In het derde kwartaal steeg de omzet met 8% tot € 4,2 miljoen, de kosten stegen met 3% (vooral door hogere energieprijzen) en het aantal klanten groeide van 1.200 naar 1.350. Voor het vierde kwartaal verwacht de directie een vergelijkbare groei, mits de energieprijzen stabiel blijven.
````

### Output Y

````text
In het derde kwartaal steeg de omzet met 8% tot € 4,2 miljoen, terwijl de kosten met 3% stegen, vooral door hogere energieprijzen, en het aantal klanten groeide van 1.200 naar 1.350. Voor het vierde kwartaal verwacht de directie een vergelijkbare groei, mits de energieprijzen stabiel blijven.

Inhoudelijk is niets weggevallen.
````

### Output Z

````text
In het derde kwartaal steeg de omzet met 8% tot € 4,2 miljoen en groeide het aantal klanten van 1.200 naar 1.350; de kosten stegen met 3%, vooral door hogere energieprijzen. Voor het vierde kwartaal verwacht de directie een vergelijkbare groei, mits de energieprijzen stabiel blijven.
````

## V20 (inkorten, taak: shorten)

**Verzoek:** Maak dit korter.

**Input:**
Wij willen u er graag op wijzen dat het voor de goede orde van belang is dat u uw parkeervergunning uiterlijk 30 november verlengt. Indien u dit niet doet, vervalt uw vergunning per 1 december en kunt u niet meer in de wijk parkeren.
**Invarianten:** uiterlijk 30 november verlengen; gevolg: vervalt per 1 december; niet meer in de wijk parkeren; u-vorm

**Niet:** termijn weg; gevolg weg

### Output X

````text
Verleng uw parkeervergunning uiterlijk 30 november. Anders vervalt uw vergunning per 1 december en kunt u niet meer in de wijk parkeren.

Weggevallen: alleen de inleidende beleefdheidsformule, inhoudelijk niets.
````

### Output Y

````text
Verleng uw parkeervergunning uiterlijk 30 november. Doet u dat niet, dan vervalt uw vergunning per 1 december en kunt u niet meer in de wijk parkeren.

Weggevallen: alleen de inleidende formule; alle termijnen en gevolgen staan er nog.
````

### Output Z

````text
Verleng uw parkeervergunning uiterlijk 30 november. Anders vervalt de vergunning per 1 december en kunt u niet meer in de wijk parkeren.
````

## V21 (verwachting, taak: rewrite)

**Verzoek:** Maak dit bericht aan mijn manager directer.

**Input:**
Hoi Lisa, we verwachten de release in week 48, maar dat is afhankelijk van de uitkomst van de pentest. Als daar kritieke bevindingen uitkomen, schuift de release minimaal een week op.
**Invarianten:** verwachting, geen garantie; week 48; afhankelijk van pentest; bij kritieke bevindingen minimaal een week later

**Niet:** 'de release is in week 48'; 'minimaal' weg

### Output X

````text
Hoi Lisa, we verwachten de release in week 48, maar dat hangt af van de uitkomst van de pentest. Komen daar kritieke bevindingen uit, dan schuift de release minimaal een week op.
````

### Output Y

````text
Hoi Lisa, we verwachten de release in week 48, afhankelijk van de pentest. Levert die kritieke bevindingen op, dan schuift de release minimaal een week op.
````

### Output Z

````text
Hoi Lisa, we verwachten de release in week 48, afhankelijk van de pentest. Levert die kritieke bevindingen op, dan schuift de release minimaal een week op.
````

## V22 (precisie, taak: rewrite)

**Verzoek:** Haal de AI-toon eruit.

**Input:**
Het is van cruciaal belang om te benadrukken dat de tolerantie van het onderdeel 0,050 mm bedraagt. Daarnaast mag de bedrijfstemperatuur in geen geval hoger zijn dan 85 °C.
**Invarianten:** 0,050 mm (precisie); niet hoger dan 85 °C; verbod blijft verbod

**Niet:** 0,05 mm; 'maximaal ongeveer'

### Output X

````text
De tolerantie van het onderdeel is 0,050 mm. De bedrijfstemperatuur mag in geen geval hoger zijn dan 85 °C.
````

### Output Y

````text
De tolerantie van het onderdeel is 0,050 mm. De bedrijfstemperatuur mag nooit hoger worden dan 85 °C.
````

### Output Z

````text
De tolerantie van het onderdeel is 0,050 mm. De bedrijfstemperatuur mag in geen geval hoger zijn dan 85 °C.
````

## V23 (waarde bij zaak, taak: rewrite)

**Verzoek:** Maak deze update natuurlijker.

**Input:**
Graag informeer ik jullie over de stand van zaken: server A registreerde gisteren 12 fouten, terwijl server B slechts 3 fouten registreerde. Server A wordt vanavond om 22:00 herstart.
**Invarianten:** A=12, B=3; gisteren; A herstart vanavond 22:00

**Niet:** waarden verwisseld; verkeerde server herstart

### Output X

````text
Korte update: server A registreerde gisteren 12 fouten, server B maar 3. Server A wordt vanavond om 22:00 herstart.
````

### Output Y

````text
Stand van zaken: server A registreerde gisteren 12 fouten, server B maar 3. Server A wordt vanavond om 22:00 herstart.
````

### Output Z

````text
Stand van zaken: server A registreerde gisteren 12 fouten, server B maar 3. Server A wordt vanavond om 22:00 herstart.
````

## V24 (briefing, taak: create)

**Verzoek:** Schrijf hier een korte mail van aan de klant.

**Input:**
- afspraak verzet: van dinsdag 4 november naar donderdag 6 november 10:00
- locatie blijft hetzelfde
- graag bevestigen
- contactpersoon: meneer Jansen
**Invarianten:** dinsdag 4 november naar donderdag 6 november 10:00; locatie hetzelfde; verzoek om bevestiging; meneer Jansen

**Niet:** verzonnen reden, locatie of tijd; bevestiging als besluit

### Output X

````text
Beste meneer Jansen,

Onze afspraak van dinsdag 4 november is verzet naar donderdag 6 november om 10:00. De locatie blijft hetzelfde.

Wilt u de nieuwe afspraak bevestigen?

Met vriendelijke groet,
[naam?]

Let op: ik ben ervan uitgegaan dat meneer Jansen de klant is aan wie de mail gericht is. Is hij jullie eigen contactpersoon, pas dan aanhef en tekst aan.
````

### Output Y

````text
Onderwerp: Afspraak verzet naar donderdag 6 november

Beste meneer Jansen,

Onze afspraak van dinsdag 4 november is verzet naar donderdag 6 november om 10:00 uur. De locatie blijft hetzelfde.

Wilt u de nieuwe afspraak bevestigen?

Met vriendelijke groet,
[naam]
````

### Output Z

````text
Beste meneer Jansen,

De afspraak van dinsdag 4 november is verzet naar donderdag 6 november om 10:00. De locatie blijft hetzelfde.

Wilt u de nieuwe datum en tijd bevestigen?

Met vriendelijke groet,
[naam?]

Let op: ik ben ervan uitgegaan dat meneer Jansen de ontvanger is. Is hij juist het aanspreekpunt aan jullie kant, dan moet de aanhef anders en hoort zijn naam onderaan als contactpersoon.
````

## V25 (informeel met emoji, taak: rewrite)

**Verzoek:** Maak dit iets vlotter, het is een appje aan vrienden.

**Input:**
Hey allemaal! Zaterdag om 8 uur vertrekken we naar de Veluwe 🚴 Neem allemaal je eigen lunch mee, want er is onderweg niks open.
**Invarianten:** zaterdag 8 uur; Veluwe; eigen lunch meenemen; reden: onderweg niks open; informele toon

**Niet:** formeel worden; reden weg

### Output X

````text
Hey allemaal! Zaterdag 8 uur vertrekken we naar de Veluwe 🚴 Neem je eigen lunch mee, onderweg is niks open.
````

### Output Y

````text
Hey allemaal! Zaterdag om 8 uur vertrekken we naar de Veluwe 🚴 Neem zelf lunch mee, onderweg is niks open.
````

### Output Z

````text
Hey allemaal! Zaterdag om 8 uur vertrekken we naar de Veluwe 🚴 Neem je eigen lunch mee, onderweg is er niks open.
````

## V26 (onbewezen bronclaim, taak: rewrite)

**Verzoek:** Herschrijf dit natuurlijker.

**Input:**
Volgens onze leverancier zorgt de nieuwe software ervoor dat de verwerkingstijd met 40% afneemt. Dit is echter nog niet door ons zelf getest.
**Invarianten:** toeschrijving aan leverancier; 40%; nog niet zelf getest

**Niet:** 40% als vaststaand feit; 'getest' weggelaten

### Output X

````text
Volgens onze leverancier daalt de verwerkingstijd met de nieuwe software met 40%. Zelf hebben we dat nog niet getest.
````

### Output Y

````text
Volgens onze leverancier verkort de nieuwe software de verwerkingstijd met 40%. Zelf hebben we dat nog niet getest.
````

### Output Z

````text
Volgens onze leverancier verkort de nieuwe software de verwerkingstijd met 40%. Zelf hebben we dat nog niet getest.
````
