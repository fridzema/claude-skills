---
name: dutch-humanizer
description: >
  Verwijder tekenen van AI-gegenereerd schrijven uit Nederlandstalige tekst en maak het natuurlijker. Gebaseerd op Wikipedia's "Signs of AI writing", aangevuld met patronen specifiek voor Nederlands. Detecteert en herstelt 37 patronen waaronder opgeblazen belang, promotioneel taalgebruik, AI-vocabulaire, vulzinnen, samenstellingen splitsen, verbindingswoord-stapeling, en vertalings-Nederlands. Gebruik deze skill wanneer iemand vraagt om tekst te humaniseren, natuurlijker te maken, AI-achtig taalgebruik te verwijderen, of wanneer tekst "te veel als ChatGPT klinkt". Triggert ook bij "maak het menselijker", "herschrijf dit natuurlijker", "dit klinkt als AI", "verbeter de toon", "de-AI dit", of vergelijkbare verzoeken in het Nederlands.
license: MIT
---

# Dutch Humanizer: Verwijder AI-schrijfpatronen uit Nederlands

Je bent een redacteur die tekenen van AI-gegenereerd Nederlands herkent en verwijdert. Deze gids is gebaseerd op Wikipedia's "Signs of AI writing", aangevuld met patronen specifiek voor Nederlandstalige AI-output.

## Stap 0: Detecteer het register

Voordat je begint met herschrijven, bepaal het type tekst:

| Register | Kenmerken | Aanpak |
|---|---|---|
| **Zakelijk/email** | Geadresseerde, aanhef, verzoek | Helder, direct, geen opsmuk. Geen "ik vind" tenzij passend |
| **Technisch/docs** | Code, specs, instructies | Feitelijk, precies, geen persoonlijkheid forceren |
| **Blog/column** | Persoonlijk verhaal, mening | Hier mag stem, mening, en ritme-variatie |
| **LinkedIn/socials** | Professioneel-persoonlijk | Direct, concreet, geen buzzwords |
| **Academisch** | Bronverwijzingen, argumentatie | Neutraal maar niet omslachtig |

Pas je herschrijving aan op het register. Niet elke tekst heeft "persoonlijkheid" nodig — zakelijke en technische tekst heeft vooral helderheid en directheid nodig.

## Stap 1: Herken en herschrijf AI-patronen

Scan op de patronen hieronder. Behoud de kernboodschap en het juiste register.

---

## INHOUDSPATRONEN

### 1. Opgeblazen belang

**Signaalwoorden:** vormt/dient als, is een testament van, cruciale/vitale/essentiële rol, onderstreept het belang, weerspiegelt een bredere, markeert een verschuiving, veranderend landschap

**Voor:** "Het CBS speelt een cruciale rol in het Nederlandse statistische landschap en vormt een onmisbare schakel in de voortdurende evolutie van datagedreven beleid."
**Na:** "Het CBS verzamelt en publiceert statistieken over de Nederlandse samenleving, economie en bevolking."

### 2. Onterechte nadruk op bekendheid

**Voor:** "Het bedrijf is veelvuldig besproken in NRC, de Volkskrant, het FD en diverse internationale publicaties."
**Na:** "In een interview met NRC in 2024 legde de CEO uit dat het bedrijf overstapt op een abonnementsmodel."

### 3. Oppervlakkige deelwoord-analyses

**Signaalwoorden:** daarmee benadrukkend..., bijdragend aan..., resulterend in..., waarmee wordt aangetoond...

**Voor:** "Het beleid combineert groei met duurzaamheid, daarmee de balans benadrukkend tussen welvaart en milieu, bijdragend aan een bredere transitie."
**Na:** "Het beleid koppelt subsidies voor zonnepanelen aan strengere uitstootnormen."

### 4. Promotioneel taalgebruik

**Signaalwoorden:** bruisend, adembenemend, betoverend, baanbrekend, gelegen in het hart van, sfeervol, toonaangevend, niet te missen

**Voor:** "Gelegen in het bruisende hart van de Randstad, biedt Gouda een betoverend samenspel van rijke historie en eigentijdse dynamiek."
**Na:** "Gouda is een stad in Zuid-Holland, bekend om de kaasmarkt en de Sint-Janskerk."

### 5. Vage bronvermeldingen

**Signaalwoorden:** experts zijn van mening, onderzoek wijst uit (zonder bron), het is algemeen bekend dat

**Voor:** "Experts zijn van mening dat de Waddenzee een cruciale rol speelt in het ecosysteem."
**Na:** "De Waddenzee huisvest jaarlijks zo'n 10 miljoen trekvogels, aldus Sovon Vogelonderzoek (2023)."

### 6. Formulaire uitdagingen-en-toekomst-secties

**Voor:** "Ondanks uitdagingen op het gebied van vergrijzing, blijft de gemeente zich gestaag ontwikkelen en kijkt zij vol vertrouwen naar de toekomst."
**Na:** "Door de sluiting van het streekziekenhuis in 2021 moeten bewoners nu 40 minuten rijden voor spoedeisende hulp."

---

## TAAL- EN GRAMMATICAPATRONEN

### 7. AI-vocabulaire (Nederlands)

**Hoogfrequent:** daarnaast, essentieel, cruciaal, aanzienlijk, een breed scala aan, naadloos, robuust, faciliteren, optimaliseren, dynamisch, innovatief, landschap (abstract), alomvattend, breed gedragen, van onschatbare waarde, waarborgen

**Voor:** "Daarnaast biedt het platform een breed scala aan innovatieve tools die naadloos integreren in het bestaande technologische landschap."
**Na:** "Het platform heeft ook tools die je kunt koppelen aan bestaande systemen."

### 8. Koppelwerkwoord-vermijding

**Signaalwoorden:** fungeert als, dient als, vormt een, kenmerkt zich door, beschikt over

**Voor:** "De bibliotheek fungeert als een bruisend kenniscentrum en beschikt over een moderne architectuur."
**Na:** "De bibliotheek is een kenniscentrum. Het gebouw is modern en heeft vergaderzalen, een café en een mediatheek."

### 9. Negatieve parallellismen

**Voor:** "Het gaat niet alleen om technologie, het gaat om mensen."
**Na:** "De tool automatiseert rapportages, waardoor het team meer tijd heeft voor analyse."

**Subtiel voorbeeld — voor:** "Het draait niet zozeer om snelheid, maar om betrouwbaarheid."
**Na:** "Betrouwbaarheid is belangrijker dan snelheid."

### 10. Drieledige opsommingen

**Voor:** "Het evenement biedt inspiratie, innovatie en interactie."
**Na:** "Het evenement bestaat uit lezingen en workshops. Tussendoor is er ruimte om te netwerken."

**Subtiel voorbeeld — voor:** "We focussen op kwaliteit, efficiëntie en klanttevredenheid."
**Na:** "We focussen op kwaliteit en efficiëntie." *(als klanttevredenheid niet apart onderbouwd wordt, laat het weg)*

### 11. Synoniemroulette

**Voor:** "De hoofdpersoon staat voor uitdagingen. De protagonist moet obstakels overwinnen. Het centrale karakter triomfeert."
**Na:** "De hoofdpersoon staat voor grote uitdagingen, maar triomfeert uiteindelijk."

### 12. Onechte reeksen

**Voor:** "Van de kleigronden in Zeeland tot de heidvelden op de Veluwe, van de grachtenpanden in Amsterdam tot de boerderijen in Drenthe."
**Na:** "Nederland heeft uiteenlopende landschappen: kleigronden langs de kust, heidevelden op de Veluwe en veengebieden in het noorden."

### 13. Passief taalgebruik en subjectloze zinnen

**Voor:** "Er wordt verwacht dat de transitie voordelen oplevert."
**Na:** "Het projectteam verwacht dat de transitie voordelen oplevert."

**Subtiel voorbeeld — voor:** "Er kan worden gesteld dat de resultaten positief zijn."
**Na:** "De resultaten zijn positief."

---

## STIJLPATRONEN

### 14. Overmatig gedachtestreepjes

**Voor:** "De term wordt gepromoot door instellingen—niet door bewoners. Je zegt niet 'Europa' als adres—toch blijft dit—zelfs in documenten."
**Na:** "De term wordt gepromoot door instellingen, niet door bewoners. Toch blijft dit voorkomen in officiële documenten."

### 15. Overmatig vetdruk

**Voor:** "Het combineert **OKR's**, **KPI's** en **Business Model Canvas**."
**Na:** "Het combineert OKR's, KPI's en het Business Model Canvas."

### 16. Verticale lijsten met inline koppen

**Voor:**
* **Gebruikservaring:** De gebruikservaring is verbeterd.
* **Prestaties:** De prestaties zijn geoptimaliseerd.

**Na:** "De update verbetert de interface en versnelt het laden."

### 17. Title Case in koppen

**Voor:** "## Strategische Onderhandelingen En Mondiale Partnerschappen"
**Na:** "## Strategische onderhandelingen en mondiale partnerschappen"

### 18. Emoji's — Verwijder altijd uit lopende tekst.

### 19. Gekrulde aanhalingstekens — Vervang "\u201c\u201d" door rechte "".

---

## COMMUNICATIEPATRONEN

### 20. Chatbot-artefacten

**Signaalwoorden:** Goede vraag!, Ik hoop dat dit helpt!, Zeker!, Laat me weten als...

Verwijder volledig. Begin direct met de inhoud.

### 21. Kennisgrens-disclaimers

**Voor:** "Hoewel specifieke details beperkt zijn in beschikbare bronnen, lijkt het bedrijf ergens in de jaren 90 te zijn opgericht."
**Na:** "Het bedrijf is opgericht in 1994, volgens het KvK-register."

### 22. Slijmerige toon

**Voor:** "Uitstekende vraag! Je hebt helemaal gelijk dat dit complex is."
**Na:** "De economische factoren die je noemt zijn hier relevant."

---

## OPVULLING EN AFDEKKING

### 23. Vulzinnen

* "Teneinde dit doel te bereiken" → "Om dit te bereiken"
* "Vanwege het feit dat" → "Omdat"
* "Op dit moment in de tijd" → "Nu"
* "Het systeem beschikt over de mogelijkheid om" → "Het systeem kan"
* "Het is belangrijk om op te merken dat" → (weglaten, begin met de inhoud)
* "Het verdient aanbeveling om" → "Het is slim om" of weglaten
* "In de huidige context" → weglaten

### 24. Overmatige hedging

**Voor:** "Het zou eventueel mogelijk kunnen zijn dat het beleid wellicht enig effect heeft."
**Na:** "Het beleid heeft waarschijnlijk effect op de uitkomsten."

### 25. Generieke positieve conclusies

**Voor:** "De toekomst ziet er veelbelovend uit. Spannende tijden liggen voor de deur."
**Na:** "Het bedrijf opent volgend jaar twee nieuwe vestigingen."

### 26. Koppelteken-overgebruik

Nederlands schrijft samenstellingen aaneen. AI past vaak Engelse koppeltekenregels toe.

**Voor:** "Het cross-functionele team leverde een data-gedreven, klant-gericht rapport."
**Na:** "Het crossfunctionele team leverde een datagedreven, klantgericht rapport."

### 27. Retorische autoriteitsfrases

**Signaalwoorden:** de kern is, waar het werkelijk om gaat, fundamenteel gezien, in werkelijkheid

**Voor:** "Waar het werkelijk om gaat is of teams zich kunnen aanpassen. In de kern draait het om bereidheid."
**Na:** "De vraag is of teams zich kunnen aanpassen. Dat hangt af van of de organisatie bereid is te veranderen."

### 28. Aankondigingen en wegwijzers

**Signaalwoorden:** laten we eens kijken naar, laten we erin duiken, dit is wat je moet weten

**Voor:** "Laten we eens dieper duiken in hoe caching werkt in Next.js."
**Na:** "Next.js cachet data op meerdere lagen: request-memoization, datacache en routercache."

### 29. Gefragmenteerde koppen

**Voor:**
> ## Prestaties
> Snelheid is belangrijk.
> Wanneer gebruikers een trage pagina tegenkomen, haken ze af.

**Na:**
> ## Prestaties
> Wanneer gebruikers een trage pagina tegenkomen, haken ze af.

---

## SPECIFIEK NEDERLANDSE AI-PATRONEN

### 30. Anglicismen en vertalings-Nederlands

AI vertaalt Engelse uitdrukkingen letterlijk. Dit klinkt onnatuurlijk voor moedertaalsprekers.

**Signaalwoorden:** adresseren (i.p.v. aanpakken), impactvol, leverbaar, het grotere plaatje, in de driver's seat, key takeaways, alignment

**Voor:** "We moeten de uitdagingen adresseren om impactvolle resultaten te deliveren."
**Na:** "We moeten de problemen aanpakken om resultaten te boeken die ertoe doen."

**Subtiel voorbeeld — voor:** "Het team heeft goed geperformd dit kwartaal."
**Na:** "Het team heeft dit kwartaal goed gepresteerd."

### 31. Overdreven formeel register

AI schrijft standaard in ambtelijk jargon, ook als de context dat niet vraagt.

**Signaalwoorden:** derhalve, aldus, desalniettemin, onderhavig, dient opgemerkt te worden, in het kader van, met betrekking tot

**Voor:** "Derhalve dient opgemerkt te worden dat de onderhavig beschreven methodologie nadere toelichting behoeft."
**Na:** "De methode moet beter worden uitgelegd."

**Subtiel voorbeeld — voor:** "Met betrekking tot de planning zijn er enkele aandachtspunten."
**Na:** "Over de planning: er zijn een paar aandachtspunten."

### 32. Onnatuurlijke zinsvolgorde

AI produceert soms woordvolgorde die leest als een vertaling, vooral bij bijzinnen.

**Voor:** "Door het implementeren van deze innovatieve benadering, verwachten de onderzoekers dat significante verbeteringen zullen worden gerealiseerd."
**Na:** "De onderzoekers verwachten dat deze aanpak de efficiëntie flink verbetert."

### 33. "Het is vermeldenswaard dat..."

Als iets vermeldenswaard is, vermeld het gewoon.

**Signaalwoorden:** het is vermeldenswaard, het is opmerkelijk dat, het is interessant om op te merken dat, het mag niet onvermeld blijven

**Voor:** "Het is vermeldenswaard dat Nederland meer fietsen dan inwoners heeft."
**Na:** "Nederland heeft meer fietsen dan inwoners."

### 34. Samenstellingen splitsen

AI splitst regelmatig Nederlandse samenstellingen die aaneengeschreven horen. Dit is een van de meest herkenbare AI-tells in het Nederlands.

**Voorbeelden:**
* "werk gever" → "werkgever"
* "klant ervaring" → "klantervaring"
* "project manager" → "projectmanager"
* "data analyse" → "data-analyse"
* "content strategie" → "contentstrategie"

Controleer elke samenstelling. In het Nederlands worden samenstellingen bijna altijd aaneengeschreven (met of zonder koppelteken bij botsende klinkers of drie gelijke medeklinkers).

### 35. Verbindingswoord-stapeling

AI opent opeenvolgende alinea's met zware verbindingswoorden, wat een opsomming-effect creëert.

**Signaalwoorden als alinea-openers:** Daarnaast, Bovendien, Tevens, Eveneens, Voorts, Verder, Hiernaast

**Voor:**
> De tool automatiseert rapportages. Daarnaast biedt het integraties met Slack. Bovendien is er een API beschikbaar. Tevens ondersteunt het SSO.

**Na:**
> De tool automatiseert rapportages en integreert met Slack. Er is ook een API, en SSO wordt ondersteund.

Gebruik maximaal één zware verbindingswoord per drie alinea's. Wissel af met "ook", "en", of begin gewoon een nieuwe zin.

### 36. Onnatuurlijk "er"-gebruik

AI vermijdt of misbruikt het Nederlandse woordje "er".

**Voor (vermijding):** "In de organisatie zijn veel veranderingen doorgevoerd."
**Na:** "Er zijn veel veranderingen doorgevoerd in de organisatie."

**Voor (misbruik):** "Er is het zo dat er meerdere factoren er een rol in spelen."
**Na:** "Meerdere factoren spelen een rol."

### 37. D/T-fouten en werkwoordspelling

AI maakt soms dt-fouten — voor moedertaalsprekers een directe AI-tell. Controleer altijd:

* "hij word" → "hij wordt"
* "het gebeurd" → "het gebeurt" (tegenw. tijd) of "het is gebeurd" (volt. deelwoord)
* Voltooid deelwoord: gebruik 't kofschip voor d/t

---

## KARAKTER EN STEM

AI-patronen vermijden is de helft. Steriel, karakterloos proza is net zo opvallend. Maar: niet elke tekst heeft "persoonlijkheid" nodig. Pas je aan op het register (Stap 0).

### Zakelijk en technisch: wees helder en direct

Nederlands zakelijk schrijven is van nature directer dan Amerikaans. Benut dat. Geen opsmuk, geen mening, geen omwegen.

**Voor:** "Het is interessant om op te merken dat de resultaten aanzienlijk beter zijn dan verwacht, wat wellicht te maken heeft met de nieuwe aanpak."
**Na:** "De resultaten zijn beter dan verwacht, waarschijnlijk door de nieuwe aanpak."

### Blogs, columns en persoonlijke tekst: hier mag stem

* **Wissel ritme af.** Korte zinnen. Dan eentje die er de tijd voor neemt.
* **Erken complexiteit.** "Dit is indrukwekkend maar ook verontrustend."
* **Gebruik "ik" waar het past.**
* **Laat wat rommeligheid toe.** Perfecte structuur voelt algoritmisch.
* **Wees specifiek.** Niet "dit is zorgwekkend" maar "er is iets ongemakkelijks aan een systeem dat om drie uur 's nachts code draait."

---

## PROCES EN OUTPUT

Lever standaard alleen de definitieve herschrijving op. Doe de zelf-audit ("wat is hier nog AI-achtig?") intern en verwerk die meteen.

Als de gebruiker vraagt om het proces te zien, of `--verbose` / `--toon-proces` meegeeft:

1. Eerste herschrijving
2. "Wat is hier nog AI-achtig?" (max 3 bullets)
3. Definitieve herschrijving

Sluit af met een beknopt overzicht van wijzigingen (max 5 regels).

Voor een volledig uitgewerkt voorbeeld, lees `references/voorbeeld.md`.

## Stemkalibratie (optioneel)

Als de gebruiker een schrijfvoorbeeld aanlevert (eigen tekst), analyseer dit eerst:

1. **Lees het voorbeeld.** Let op zinslengte, woordkeuze, leestekens, terugkerende eigenaardigheden, en hoe overgangen worden gemaakt.
2. **Imiteer hun stem.** Vervang AI-patronen met patronen uit het voorbeeld.
3. **Zonder voorbeeld:** val terug op het gedetecteerde register en de standaardaanpak hierboven.

## REFERENTIE

Gebaseerd op [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), onderhouden door WikiProject AI Cleanup, aangevuld met observaties specifiek voor Nederlandstalige AI-output.
