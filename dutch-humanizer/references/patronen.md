# Patronen: gestructureerd overzicht

Catalogus van patronen waar AI-gegenereerd Nederlands op valt. Gestructureerd op **severity** (hoe ernstig de tell is) en voorzien van een **per-pattern template** dat helpt bij de afweging wel/niet aanpakken.

## Hoe deze catalogus te gebruiken

**Niet mechanisch doorlopen.** Een rewrite die alle 50+ patronen tegelijk wegwerkt produceert overcorrectie. Het juiste gebruik:

1. Pak de top-3 dominante tells in de tekst.
2. Pas die aan.
3. Lees het resultaat.
4. Eventueel een tweede pas voor 1-2 secundaire tells.

**Severity-niveaus**:

| Niveau | Aanpak |
|---|---|
| **Blockers** | Always fix. Raken betekenis, veiligheid of feitenjuistheid. |
| **Major signals** | Almost always fix. Sterke AI-tells; menselijk Nederlands gebruikt deze zelden. |
| **Moderate signals** | Contextueel fixen. Kan in sommige registers legitiem zijn. |
| **Contextual signals** | Afhankelijk van kanaal/register/huisstijl. Hard regels uit `SKILL.md` overrulen contextuele afweging. |
| **Communicatie-tics** | Specifiek aan assistant-output; zelden gewenst behalve in literaire imitatie. |
| **Algemene spelcontrole** | Niet AI-specifiek; meenemen in zelf-audit. |

**Per-pattern template**:

- **Symptoom**: hoe herken je het.
- **Waarom AI**: waarom een AI dit produceert of waarom het synthetisch leest.
- **Niet fixen wanneer**: false-positive cases.
- **Vervanging**: wat doe je in plaats daarvan.
- **Voorbeeld**: voor/na.

Zie ook de losse sectie [False positives](#false-positives-vermijden-van-overcorrectie) onderaan.

---

## Blockers: must-fix

Deze raken betekenis, veiligheid of correctheid. Ze zijn niet onderhandelbaar.

### Verzonnen feiten

**Symptoom**: in de output staan namen, datums, cijfers, percentages, organisaties, bronnen of citaten die niet in de input voorkomen.
**Waarom AI**: bij vage input grijpt AI naar plausibel klinkende specifics om "menselijk concreet" te schrijven.
**Niet fixen wanneer**: nooit. Dit is altijd fout.
**Vervanging**: zie [`SKILL.md`](../SKILL.md) "Fact-inventory" en "Niet verzinnen". Drie correcte aanpakken: claim verwijderen, placeholder (`[bron?]`/`[datum?]`/`[percentage?]`), of de gebruiker om de feiten vragen.

**Voor:** "Studies tonen aan dat 73% van de bedrijven dit doet."
**Na (geen bron):** "Veel bedrijven doen dit." *of* "[Bron?] meldt dat 73% van de bedrijven dit doet."

### Gewijzigde harde feiten

**Symptoom**: een cijfer, datum, naam of versie in de input is in de output anders.
**Waarom AI**: paraphrase-bias; soms "round numbers" als de input een odd number had.
**Niet fixen wanneer**: nooit.
**Vervanging**: behoud exacte waarden. Zelfs een synoniem voor "ongeveer 100" mag niet "rond de 100" worden als de input "97" zei.

### Code- of citaat-corruptie

**Symptoom**: code-blok, citaat of voetnoot is gewijzigd: andere syntax, andere quote-marks, gewijzigd commentaar, ingekorte URL.
**Waarom AI**: paraphrase-instinct strekt onbedoeld tot code en citaten.
**Niet fixen wanneer**: nooit. Code en geciteerd materiaal blijven 100% identiek.
**Vervanging**: copy-paste, niet rewrite.

### Locale-mismatch waar locale expliciet was

**Symptoom**: input is duidelijk nl-BE (of de gebruiker vroeg nl-BE), output gebruikt nl-NL-specifieke termen of omgekeerd.
**Waarom AI**: default-bias naar nl-NL.
**Niet fixen wanneer**: locale was niet expliciet en de gebruiker accepteert beide.
**Vervanging**: zie [`locale.md`](locale.md). Behoud bestaande locale; niet automatisch converteren.

---

## Major signals: usually fix

Sterke AI-tells. Menselijk Nederlands gebruikt deze patronen zelden of veel spaarzamer.

### Opgeblazen belang

**Symptoom**: vormt/dient als, is een testament van, cruciale/vitale/essentiële rol, onderstreept het belang, weerspiegelt een bredere, markeert een verschuiving, veranderend landschap.
**Waarom AI**: AI vult kort feit aan met abstracte significantie-claims zonder informatieve waarde.
**Niet fixen wanneer**: in kritiek/opinie waar het belang juist het onderwerp is.
**Vervanging**: vervang door concreet feit, of laat de claim weg.

**Voor:** "Het CBS speelt een cruciale rol in het Nederlandse statistische landschap en vormt een onmisbare schakel in de voortdurende evolutie van datagedreven beleid."
**Na:** "Het CBS verzamelt en publiceert statistieken over de Nederlandse samenleving, economie en bevolking."

### Promotioneel taalgebruik

**Symptoom**: bruisend, adembenemend, betoverend, baanbrekend, gelegen in het hart van, sfeervol, toonaangevend, niet te missen, iconisch, must-see.
**Waarom AI**: training-data uit toeristenfolders en marketing-copy.
**Niet fixen wanneer**: bewust marketing-genre voor doelpubliek dat het verwacht (en zelfs daar: minder is meer).
**Vervanging**: feitelijke beschrijving zonder bijvoeglijke opsmuk.

**Voor:** "Gelegen in het bruisende hart van de Randstad, biedt Gouda een betoverend samenspel van rijke historie en eigentijdse dynamiek."
**Na:** "Gouda is een stad in Zuid-Holland, bekend om de kaasmarkt en de Sint-Janskerk."

### AI-vocabulaire

**Symptoom (hoogfrequent)**: daarnaast, essentieel, cruciaal, aanzienlijk, een breed scala aan, naadloos, robuust, faciliteren, optimaliseren, dynamisch, innovatief, landschap (abstract), alomvattend, breed gedragen, van onschatbare waarde, waarborgen, ontsluiten, hervormen, transformeren.
**Waarom AI**: deze woorden zijn statistisch oververtegenwoordigd in AI-output.
**Niet fixen wanneer**: het woord een specifieke vakterm is met geen goed Nederlands equivalent ("robuuste statistiek" in techniek-context).
**Vervanging**: gewone synoniemen of weglaten.

**Voor:** "Daarnaast biedt het platform een breed scala aan innovatieve tools die naadloos integreren in het bestaande technologische landschap."
**Na:** "Het platform heeft ook tools die je kunt koppelen aan bestaande systemen."

### Vage bronvermeldingen

**Symptoom**: experts zijn van mening, onderzoek wijst uit (zonder bron), studies tonen aan, het is algemeen bekend dat, men gaat ervan uit.
**Waarom AI**: training maakt vage bronnen makkelijker dan echte.
**Niet fixen wanneer**: de claim is zo bekend dat geen bron nodig is ("Nederland heeft koningshuis").
**Vervanging**: zie de drie aanpakken in *Blockers - Verzonnen feiten*. Drie correcte opties: claim verwijderen, placeholder `[bron?]`, of bestaande bron behouden. Verzin nooit een specifieke bron.

**Voor:** "Experts zijn van mening dat de Waddenzee een belangrijk natuurgebied is."
**Na:** "De Waddenzee is een belangrijk natuurgebied."

### Engelse calques

**Symptoom**: adresseren (i.p.v. aanpakken), impactvol, leveren/deliveren, het grotere plaatje, in de driver's seat, key takeaways, alignment, performen, leveragen, scalen, uitrollen (figuurlijk).
**Waarom AI**: directe vertaling uit Engelse training-data.
**Niet fixen wanneer**: de term is in een vaktechnische context standaard ("agile scalen" in software).
**Vervanging**: Nederlandse equivalenten.

**Voor:** "We moeten de uitdagingen adresseren om impactvolle resultaten te deliveren."
**Na:** "We moeten de problemen aanpakken om resultaten te boeken die ertoe doen."

### Overdreven formeel register

**Symptoom**: derhalve, aldus (als bijwoord), desalniettemin, onderhavig, dient opgemerkt te worden, in het kader van, met betrekking tot, alvorens, middels, doch, immer, thans.
**Waarom AI**: AI valt terug op ambtelijke training-data.
**Niet fixen wanneer**: een juridische akte of officieel document waar deze termen vakbetekenis hebben.
**Vervanging**: gewone Nederlandse alternatieven (Taaladvies.net adviseert spaarzaam gebruik van formele woorden).

**Voor:** "Derhalve dient opgemerkt te worden dat de onderhavig beschreven methodologie nadere toelichting behoeft."
**Na:** "De methode moet beter worden uitgelegd."

**Subtieler. Voor:** "Met betrekking tot de planning zijn er enkele aandachtspunten."
**Na:** "Over de planning: er zijn een paar aandachtspunten."

### Verbindingswoord-stapeling

**Symptoom (alinea-openers)**: Daarnaast, Bovendien, Tevens, Eveneens, Voorts, Verder, Hiernaast, opeenvolgend over meerdere alinea's.
**Waarom AI**: AI maakt opsommingen zichtbaar in plaats van impliciet.
**Niet fixen wanneer**: lijst-introductie waar elke alinea inderdaad een aparte bullet is.
**Vervanging**: maximaal één zwaar verbindingswoord per drie alinea's. Wissel af met "ook", "en", of begin gewoon een nieuwe zin.

**Voor:**
> De tool automatiseert rapportages. Daarnaast biedt het integraties met Slack. Bovendien is er een API beschikbaar. Tevens ondersteunt het SSO.

**Na:**
> De tool automatiseert rapportages en integreert met Slack. Er is ook een API, en SSO wordt ondersteund.

### Onnatuurlijke zinsvolgorde (vertaal-Nederlands)

**Symptoom**: woordvolgorde leest als directe vertaling van Engels; voorop-geplaatste bijzin met komma; nominalisaties.
**Waarom AI**: training-bias naar Engelse syntax.
**Niet fixen wanneer**: bewust gekozen ritme in literair register.
**Vervanging**: herschrijven met natuurlijke Nederlandse woordvolgorde, vaak hoofdzin eerst.

**Voor:** "Door het implementeren van deze innovatieve benadering, verwachten de onderzoekers dat significante verbeteringen zullen worden gerealiseerd."
**Na:** "De onderzoekers verwachten dat deze aanpak de efficiëntie flink verbetert."

### Cliché-openers

**Symptoom**: In een wereld waarin..., In tijden van..., In het huidige (digitale/snel veranderende) tijdperk..., Stel je voor dat..., Of het nu gaat om X of Y.
**Waarom AI**: training-data uit Engelstalige content-marketing.
**Niet fixen wanneer**: bewuste retorische opener in literair/opinie-register, en dan hoogstens één keer.
**Vervanging**: begin met de concrete context.

**Voor:** "In een wereld waarin data het nieuwe goud is, kan geen organisatie nog zonder een datastrategie."
**Na:** "Onze klanten vragen sinds dit jaar steeds vaker om datarapportages, daarom hebben we een datastrategie opgesteld."

### Bijvoeglijk-naamwoord-stapeling

**Symptoom**: drie of meer adjectieven achter elkaar.
**Waarom AI**: cumulatief willen-overtuigen.
**Niet fixen wanneer**: bewuste retorische opsomming met expliciet contrast.
**Vervanging**: kies één adjectief, of vervang door concreet zelfstandig naamwoord.

**Voor:** "Een innovatieve, baanbrekende, transformatieve oplossing voor moderne bedrijven."
**Na:** "Een nieuwe aanpak voor logistiek-bedrijven."

### Onterechte nadruk op bekendheid

**Symptoom**: opsomming van media of awards die de claim moet ondersteunen.
**Waarom AI**: AI vult vaag bewijs aan met name-dropping.
**Niet fixen wanneer**: de bekendheid is direct relevant voor het verhaal (bijvoorbeeld: artikel over hoe een bedrijf de pers haalde).
**Vervanging**: noem één concrete bron of gebeurtenis.

**Voor:** "Het bedrijf is veelvuldig besproken in NRC, de Volkskrant, het FD en diverse internationale publicaties."
**Na:** "In een interview met NRC in 2024 legde de CEO uit dat het bedrijf overstapt op een abonnementsmodel."

### Oppervlakkige deelwoord-analyses

**Symptoom**: daarmee benadrukkend..., bijdragend aan..., resulterend in..., waarmee wordt aangetoond...
**Waarom AI**: AI plakt extra significantie-clausules aan zinnen die al af zijn.
**Niet fixen wanneer**: in academisch register waar de logische schakel daadwerkelijk wordt onderbouwd.
**Vervanging**: knip de zin af na de hoofdclaim, of maak van de deelwoord-clausule een eigen zin met evidence.

**Voor:** "Het beleid combineert groei met duurzaamheid, daarmee de balans benadrukkend tussen welvaart en milieu, bijdragend aan een bredere transitie."
**Na:** "Het beleid koppelt subsidies voor zonnepanelen aan strengere uitstootnormen."

### Formulaire uitdagingen-en-toekomst-secties

**Symptoom**: "Ondanks uitdagingen op het gebied van X, blijft de Y zich gestaag ontwikkelen en kijkt vol vertrouwen naar de toekomst."
**Waarom AI**: ingebakken framing voor "afsluiten met optimisme".
**Niet fixen wanneer**: jaarverslag waar dit register expliciet wordt verwacht (en dan nog: minder is meer).
**Vervanging**: concreet feit dat de huidige stand laat zien.

**Voor:** "Ondanks uitdagingen op het gebied van vergrijzing, blijft de gemeente zich gestaag ontwikkelen en kijkt zij vol vertrouwen naar de toekomst."
**Na:** "Door de sluiting van het streekziekenhuis in 2021 moeten bewoners nu 40 minuten rijden voor spoedeisende hulp."

---

## Moderate signals: contextual fix

Patronen die in sommige registers legitiem kunnen zijn. Beoordeel per geval.

### Negatieve parallellismen

**Symptoom**: "Het gaat niet alleen om X; het gaat om Y." / "Het draait niet om X, maar om Y."
**Waarom AI**: ingebakken retorisch contrast.
**Niet fixen wanneer**: bewust contrast waarbij beide kanten relevant zijn.
**Vervanging**: positieve formulering of weglaten.

**Voor:** "Het gaat niet alleen om technologie, het gaat om mensen."
**Na:** "De tool automatiseert rapportages, waardoor het team meer tijd heeft voor analyse."

**Subtieler. Voor:** "Het draait niet zozeer om snelheid, maar om betrouwbaarheid."
**Na:** "Betrouwbaarheid is belangrijker dan snelheid."

### Drieledige opsommingen

**Symptoom**: drie elementen achter elkaar, vaak met dezelfde lengte/syntax.
**Waarom AI**: ritmisch aantrekkelijk; verbergt vage onderbouwing.
**Niet fixen wanneer**: er zijn echt drie concrete punten.
**Vervanging**: twee elementen, of een lopende zin.

**Voor:** "Het evenement biedt inspiratie, innovatie en interactie."
**Na:** "Het evenement bestaat uit lezingen en workshops. Tussendoor is er ruimte om te netwerken."

**Subtieler. Voor:** "We focussen op kwaliteit, efficiëntie en klanttevredenheid."
**Na:** "We focussen op kwaliteit en efficiëntie." *(Als klanttevredenheid niet apart onderbouwd wordt, laat het weg.)*

### Synoniemroulette

**Symptoom**: drie verschillende woorden voor hetzelfde concept binnen één korte alinea.
**Waarom AI**: AI vermijdt herhaling, ook waar herhaling juist helder is.
**Niet fixen wanneer**: bewust nuance-verschil tussen de termen.
**Vervanging**: één term consistent aanhouden.

**Voor:** "De hoofdpersoon staat voor uitdagingen. De protagonist moet obstakels overwinnen. Het centrale karakter triomfeert."
**Na:** "De hoofdpersoon staat voor grote uitdagingen, maar triomfeert uiteindelijk."

### Onechte reeksen

**Symptoom**: "Van X tot Y, van A tot B"; vier of meer elementen in parallel-structuur.
**Waarom AI**: vult diversiteits-claim met willekeurige paren.
**Niet fixen wanneer**: bewust literair effect met echt diverse voorbeelden.
**Vervanging**: één concrete, specifieke opsomming.

**Voor:** "Van de kleigronden in Zeeland tot de heidvelden op de Veluwe, van de grachtenpanden in Amsterdam tot de boerderijen in Drenthe."
**Na:** "Nederland heeft uiteenlopende landschappen: kleigronden langs de kust, heidevelden op de Veluwe en veengebieden in het noorden."

### Passief en subjectloze zinnen

**Symptoom**: "er wordt", "er kan worden gesteld", "het wordt verwacht".
**Waarom AI**: AI vermijdt actor-claim wanneer onbekend.
**Niet fixen wanneer**: actor onbekend, irrelevant of bewust verborgen (bijvoorbeeld in incident-rapport waar wie-precies-wat-deed niet helpt).
**Vervanging**: actief met concrete actor.

**Voor:** "Er wordt verwacht dat de transitie voordelen oplevert."
**Na:** "Het projectteam verwacht dat de transitie voordelen oplevert."

**Subtieler. Voor:** "Er kan worden gesteld dat de resultaten positief zijn."
**Na:** "De resultaten zijn positief."

### Koppelwerkwoord-vermijding

**Symptoom**: fungeert als, dient als, vormt een, kenmerkt zich door, beschikt over, manifesteert zich als.
**Waarom AI**: vermijdt eenvoudige `is`/`heeft`-zinnen.
**Niet fixen wanneer**: het werkwoord drukt iets specifieks uit ("dient als reservelocatie"; drukt rol uit, niet identiteit).
**Vervanging**: `is`/`heeft` waar mogelijk.

**Voor:** "De bibliotheek fungeert als een bruisend kenniscentrum en beschikt over een moderne architectuur."
**Na:** "De bibliotheek is een kenniscentrum. Het gebouw is modern en heeft vergaderzalen, een café en een mediatheek."

### "Welke" als betrekkelijk voornaamwoord

**Symptoom**: "het rapport welke is gepubliceerd", "de medewerkers welke deelnemen".
**Waarom AI**: training-bias naar formeel register.
**Niet fixen wanneer**: juridische akte of bewust formele/literaire stijl.
**Vervanging**: "die" (de-woord/meervoud) of "dat" (het-woord).

**Voor:** "Het rapport welke gepubliceerd is..."
**Na:** "Het rapport dat gepubliceerd is..."

### "Men" waar je/we hoort

**Symptoom**: "men kan stellen", "men gaat ervan uit", "men verwacht".
**Waarom AI**: training-bias naar afstandelijk register.
**Niet fixen wanneer**: academisch register waar afstandelijkheid gewenst is.
**Vervanging**: "je" (algemeen-modern), "we" (groep), of concrete actor.

**Voor:** "Men kan stellen dat dit beleid effectief is."
**Na:** "Je kunt zeggen dat dit beleid werkt." *of* "Het beleid werkt."

### "Echter" mid-zin

**Symptoom**: "X werkt, echter, niet altijd." / "X is goed, echter er zijn risico's."
**Waarom AI**: trainings-tic.
**Niet fixen wanneer**: aan begin van zin als bewust contrast-marker (zelfs daar: zelden).
**Vervanging**: "maar", punt + nieuwe zin, of weglaten.

**Voor:** "Dit werkt, echter, niet altijd."
**Na:** "Dit werkt niet altijd."

### Onnatuurlijk "er"-gebruik

**Symptoom**: vermijding van "er" waar het natuurlijk hoort, of stapeling: "er is het zo dat er X er Y".
**Waarom AI**: "er" is moeilijk te plaatsen voor niet-moedertaalsprekers; AI imiteert dat.
**Niet fixen wanneer**: zelden van toepassing.
**Vervanging**: natuurlijk Nederlandstalig "er" toevoegen of dubbelen verwijderen.

**Voor (vermijding):** "In de organisatie zijn veel veranderingen doorgevoerd."
**Na:** "Er zijn veel veranderingen doorgevoerd in de organisatie."

**Voor (misbruik):** "Er is het zo dat er meerdere factoren er een rol in spelen."
**Na:** "Meerdere factoren spelen een rol."

### Meta-verwijzingen

**Symptoom**: zoals eerder genoemd, zoals hierboven beschreven, in voorgaande sectie, zoals we hebben gezien.
**Waarom AI**: vult tekst met zelf-verwijzing.
**Niet fixen wanneer**: lange tekst waar de lezer écht terug moet bladeren.
**Vervanging**: weglaten.

**Voor:** "Zoals eerder genoemd is de planning krap."
**Na:** "De planning is krap."

### Aankondigingen en wegwijzers

**Symptoom**: laten we eens kijken naar, laten we erin duiken, dit is wat je moet weten, in deze blog gaan we, in dit artikel bespreek ik.
**Waarom AI**: training-data uit YouTube/blog-intro's.
**Niet fixen wanneer**: zelden; soms in didactisch materiaal.
**Vervanging**: begin direct met de inhoud.

**Voor:** "Laten we eens dieper duiken in hoe caching werkt in Next.js."
**Na:** "Next.js cachet data op meerdere lagen: request-memoization, datacache en routercache."

### "Het is vermeldenswaard dat..."

**Symptoom**: het is vermeldenswaard, het is opmerkelijk dat, het is interessant om op te merken dat, het mag niet onvermeld blijven.
**Waarom AI**: meta-laag boven de inhoud.
**Niet fixen wanneer**: zelden.
**Vervanging**: gewoon vermelden.

**Voor:** "Het is vermeldenswaard dat Nederland meer fietsen dan inwoners heeft."
**Na:** "Nederland heeft meer fietsen dan inwoners."

### Retorische autoriteitsfrases

**Symptoom**: de kern is, waar het werkelijk om gaat, fundamenteel gezien, in werkelijkheid, in essentie.
**Waarom AI**: simuleert wijsheid zonder onderbouwing.
**Niet fixen wanneer**: zelden.
**Vervanging**: noem direct wat je bedoelt.

**Voor:** "Waar het werkelijk om gaat is of teams zich kunnen aanpassen. In de kern draait het om bereidheid."
**Na:** "De vraag is of teams zich kunnen aanpassen. Dat hangt af van of de organisatie bereid is te veranderen."

### Vulzinnen

**Symptoom**:

- "Teneinde dit doel te bereiken" → "Om dit te bereiken"
- "Vanwege het feit dat" → "Omdat"
- "Op dit moment in de tijd" → "Nu"
- "Het systeem beschikt over de mogelijkheid om" → "Het systeem kan"
- "Het is belangrijk om op te merken dat" → (weglaten)
- "Het verdient aanbeveling om" → "Het is slim om" of weglaten
- "In de huidige context" → weglaten
- "Een en ander" → weglaten of vervangen door wat je echt bedoelt

**Niet fixen wanneer**: juridisch document waar de exacte formulering vakbetekenis heeft.

### Overmatige hedging

**Symptoom**: "wellicht", "mogelijk", "eventueel", "naar verluidt", "men neemt aan", gestapeld.
**Waarom AI**: trainings-bias naar onzekerheid.
**Niet fixen wanneer**: échte onzekerheid; één hedge per claim is fine.
**Vervanging**: één hedge maximaal, en alleen waar terecht.

**Voor:** "Het zou eventueel mogelijk kunnen zijn dat het beleid wellicht enig effect heeft."
**Na:** "Het beleid heeft waarschijnlijk effect."

### Generieke positieve conclusies

**Symptoom**: "De toekomst ziet er veelbelovend uit. Spannende tijden liggen voor de deur."
**Waarom AI**: ingebakken "afsluit op optimisme"-framing.
**Niet fixen wanneer**: zelden.
**Vervanging**: concrete next step of feit, of geen conclusie.

**Voor:** "De toekomst ziet er veelbelovend uit. Spannende tijden liggen voor de deur."
**Na:** "Het bedrijf opent volgend jaar twee nieuwe vestigingen."

### Onnodige Engelse termen

**Symptoom**: stakeholders, deliverables, alignment, bandwidth (figuurlijk), ownership (figuurlijk), commitment, leverage (werkwoord).
**Waarom AI**: training-data uit gemixte managementtaal.
**Niet fixen wanneer**: vakterm met eigen betekenis ("OKRs", "sprint", "container" in IT).
**Vervanging**:

- stakeholders → belanghebbenden, betrokkenen
- deliverables → opleverpunten, resultaten
- alignment → afstemming
- bandwidth → ruimte, capaciteit
- ownership → eigenaarschap, verantwoordelijkheid
- commitment → toezegging, betrokkenheid
- leverage → benutten, inzetten

### Vage opsomming-terminators

**Symptoom**: "en meer", "et cetera" (als afsluiting van vage opsomming), "onder andere... en meer", "...en zo".
**Waarom AI**: vermijdt specifiek-eindigen.
**Niet fixen wanneer**: zelden; soms gepast als de opsomming inderdaad open is en dat duidelijk moet zijn.
**Vervanging**: maak de opsomming compleet of laat hem eindigen.

**Voor:** "De tool ondersteunt rapportages, dashboards, integraties en meer."
**Na:** "De tool maakt rapportages, dashboards en integraties met Slack en HubSpot."

---

## Contextual signals

Patronen die afhankelijk zijn van kanaal, register of huisstijl. **Hard regels uit `SKILL.md` overrulen contextuele afweging.**

### Em-dashes en en-dashes

**Symptoom**: `—` of `–` in lopende tekst.
**Waarom AI**: AI-modellen produceren em-dashes als visuele tic.
**Niet fixen wanneer**: in een citaat of bron-tekst die letterlijk behouden moet blijven; in de skill-eigen patronencatalogus als VOOR-voorbeeld.
**Vervanging**: komma, punt of dubbele punt.

**Huisstijl-keuze (zie `SKILL.md` "Hard regels"): hard zero in alle output.** Dit is bewust restrictiever dan Taaladvies.net (dat legitieme functies voor de gedachtestreepje beschrijft), maar de overmatige aanwezigheid in AI-output maakt elk gebruik tot tell.

**Voorbeeld 1 (dramatic pause / parenthetical):**

**Voor:** "De term wordt gepromoot door instellingen—niet door bewoners. Je zegt niet 'Europa' als adres—toch blijft dit—zelfs in documenten."
**Na:** "De term wordt gepromoot door instellingen, niet door bewoners. Toch blijft dit voorkomen in officiële documenten."

**Voorbeeld 2 (parenthetical achteraf):**

**Voor:** "Dit werkt — meestal."
**Na:** "Dit werkt meestal." *of* "Dit werkt. Meestal."

**Voorbeeld 3 (list-intro):**

**Voor:** "Drie redenen — snelheid, prijs, support."
**Na:** "Drie redenen: snelheid, prijs, support."

### Spatie-hyphen-spatie als gedachtestreepje

**Symptoom**: ` - ` met spaties als em-dash-substituut.
**Niet fixen wanneer**: nooit als gedachtestreepje. Wel toegestaan als hyphen in samenstellingen.
**Vervanging**: zelfde als em-dash: komma/punt/dubbele punt.

### Overmatig vetdruk

**Symptoom**: meerdere niet-koptekst-termen vetgedrukt in één alinea, vooral als onderdeel van inline koppen-stijl.
**Waarom AI**: visuele opsmuk.
**Niet fixen wanneer**: vakterm-introductie waar vet nuttig is voor lezerservaring.
**Vervanging**: hoogstens één vetgedrukt element per alinea.

**Voor:** "Het combineert **OKR's**, **KPI's** en **Business Model Canvas**."
**Na:** "Het combineert OKR's, KPI's en het Business Model Canvas."

### Verticale lijsten met inline koppen

**Symptoom**: bullets met vetgedrukte korte koppen gevolgd door uitleg op dezelfde regel.
**Waarom AI**: training-data uit feature-lijsten.
**Niet fixen wanneer**: documentatie waar een echte feature-tabel hoort.
**Vervanging**: lopende zin of echte tabel.

**Voor:**
* **Gebruikservaring:** De gebruikservaring is verbeterd.
* **Prestaties:** De prestaties zijn geoptimaliseerd.

**Na:** "De update verbetert de interface en versnelt het laden."

### Title Case in koppen

**Symptoom**: "## Strategische Onderhandelingen En Mondiale Partnerschappen".
**Waarom AI**: bias naar Engelse conventie.
**Niet fixen wanneer**: officiële NL-titel die in Title Case staat (zelden) of een merknaam.
**Vervanging**: sentence case (alleen eerste letter en eigennamen).

**Voor:** `## Strategische Onderhandelingen En Mondiale Partnerschappen`
**Na:** `## Strategische onderhandelingen en mondiale partnerschappen`

### Emoji's in lopende tekst

**Symptoom**: 🚀, ✅, 👇, 💡 als visuele opsmuk in prose, koppen of bullet-points.
**Niet fixen wanneer**: nooit in zakelijk/docs/academisch register. Casual chat van een individuele schrijver mag, mits beperkt en functioneel.
**Vervanging**: weghalen. Huisstijl-keuze: hard zero (zie `SKILL.md`).

### Gekrulde aanhalingstekens

**Symptoom**: `"..."` (curly).
**Waarom AI**: smart-quote conversie in training-data.
**Niet fixen wanneer**: bewust typografisch design buiten skill-scope.
**Vervanging**: rechte (`"..."`). Huisstijl-keuze: hard zero (zie `SKILL.md`).

### Datum- en cijfer-format

NL-conventie:

- **Decimaal**: komma → "€3,14" niet "€3.14".
- **Duizendtallen**: punt of spatie → "1.000" of "1 000".
- **Datum**: dag-maand-jaar → "15 januari 2026" niet "January 15, 2026" of "1/15/2026".
- **Tijden**: 24-uurs of "uur"-notatie → "14:30" of "half drie 's middags".
- **Maandnamen**: kleine letter → "januari" niet "Januari".

**Niet fixen wanneer**: bron-document waar het format intentioneel is (internationale context, brand-stijl).
**Vervanging**: NL-format toepassen.

### Samenstellings-regels (hyphen wel/niet)

Twee inverse problemen, één regel: Nederlandse samenstellingen worden **aaneengeschreven**.

**Probleem A. Gesplitst (Engelse spatie-stijl):**

* "werk gever" → "werkgever"
* "klant ervaring" → "klantervaring"
* "project manager" → "projectmanager"
* "content strategie" → "contentstrategie"

**Probleem B. Engelse koppeltekens waar geen botsing is:**

* "data-gedreven" → "datagedreven"
* "klant-gericht" → "klantgericht"
* "cross-functioneel" → "crossfunctioneel"

**Wel een koppelteken** in de volgende gevallen:

* **Klinkerbotsing** die leesbaarheid hindert: "data-analyse", "auto-ongeluk", "zee-eend", "na-apen".
* **Drie gelijke medeklinkers**: "stress-situatie".
* **Voor-/achtervoegsels die anders verwarren**: "niet-roker", "ex-werkgever", "Nederlands-Duits", "anti-Amerikaans".
* **Ingeburgerde leenwoorden waar het woordenboek dat voorschrijft**: "e-mail", "online-cursus" (variabel; kies consistent).

Bij twijfel: Woordenlijst Nederlandse Taal raadplegen.

---

## Communicatie-tics

### Assistent-tics (chatbot-artefacten + slijmerige toon)

**Symptoom**: "Goede vraag!", "Uitstekende vraag!", "Zeker!", "Natuurlijk!", "Ik hoop dat dit helpt!", "Laat me weten als...", "Je hebt helemaal gelijk dat...", "Wat een interessant onderwerp!", "Voel je vrij om...".
**Waarom AI**: training op chatbot-RLHF.
**Niet fixen wanneer**: nooit in zakelijke output.
**Vervanging**: verwijder volledig; begin direct met de inhoud.

**Voor:** "Uitstekende vraag! Je hebt helemaal gelijk dat dit complex is. Hier is wat ik denk..."
**Na:** "De economische factoren die je noemt zijn hier relevant."

### Kennisgrens-disclaimers

**Symptoom**: "Hoewel specifieke details beperkt zijn in beschikbare bronnen, lijkt het bedrijf ergens in de jaren 90 te zijn opgericht."
**Waarom AI**: hedge over eigen kennis-onzekerheid.
**Niet fixen wanneer**: als de info echt niet in input/bronnen staat: vermeld dat en stop.
**Vervanging**: óf het feit (als beschikbaar), óf "dat staat niet in de aangeleverde bronnen". Niet gokken.

**Voor:** "Hoewel specifieke details beperkt zijn in beschikbare bronnen, lijkt het bedrijf ergens in de jaren 90 te zijn opgericht."
**Na (info beschikbaar):** "Het bedrijf is opgericht in 1994."
**Na (info niet beschikbaar):** "Het oprichtingsjaar staat niet in de aangeleverde bronnen."

### Gefragmenteerde inleidingen onder koppen

**Symptoom**: een kop direct gevolgd door een nietszeggende eerste zin.
**Waarom AI**: ingebakken kop-introduceert-onderwerp-pattern.
**Niet fixen wanneer**: zelden.
**Vervanging**: schrap de fragmentaire openingszin, begin met de eerste betekenisvolle zin.

**Voor:**
> ## Prestaties
> Snelheid is belangrijk.
> Wanneer gebruikers een trage pagina tegenkomen, haken ze af.

**Na:**
> ## Prestaties
> Wanneer gebruikers een trage pagina tegenkomen, haken ze af.

---

## Algemene spelcontrole (niet AI-specifiek)

### D/t-fouten en werkwoordspelling

Niet specifiek een AI-tell. Mensen maken deze ook, en moderne modellen zijn er meestal goed in. Wel meenemen in de zelf-audit, omdat een dt-fout de hele tekst onverzorgd laat ogen.

* "hij word" → "hij wordt"
* "het gebeurd" → "het gebeurt" (tegenw. tijd) / "het is gebeurd" (volt. deelw.)
* Voltooid deelwoord: gebruik 't kofschip voor d/t.

---

## False positives: vermijden van overcorrectie

De skill is in de eerste plaats subtractief. Maar overcorrectie maakt tekst slechter, niet beter. Vermijd deze valkuilen:

| Valkuil | Hoe te herkennen | Wat dan |
|---|---|---|
| **Brandnames die op signaalwoorden lijken** | "Robust BV", "Innovatie Lab", "Naadloos Software" | Behoud naam exact |
| **Citaten die letterlijk gequoteerd zijn** | tekst tussen "..." of '...' die iemand zegt | Niet rewriten, ook al bevat het AI-tells |
| **Domeinjargon** | juridische akte-termen, medische vakwoorden, technisch jargon | Behouden binnen specialistisch register |
| **Bewuste literaire stijl** | gebruiker geeft eigen schrijfvoorbeeld; voorbeeld toont consistente "tic" | Imiteer (zie `stem-kalibratie.md`) |
| **Bron-tekst met AI-tells** | de gebruiker citeert een bestaand AI-stuk | Behoud als citaat; eventueel commentaar erbij, niet de quote zelf rewriten |
| **Tekst voor een formeel publiek** | gebruiker schrijft voor advocaten, ambtenaren, academici | Sommige formele patronen zijn dan correct |
| **Numerieke of technische precisie** | API-paden, statuscodes, dosering, percentages | Nooit aanpassen of "verbeteren" |

**Vuistregel**: in twijfelgeval: niet aanraken. Een rewrite die te weinig doet is fixbaar; een rewrite die te veel doet kan onbedoelde betekenisverschuiving introduceren.

**Locale-specifieke false positives**:

- "wedde" in nl-BE-tekst is geen archaïsch synoniem voor "salaris"; het is correct nl-BE voor ambtelijk loon.
- "schepen" in nl-BE is geen vreemde gemeentebestuurs-functie; het is correct.
- "gij" in zuid-Nederlandse dialecttekst kan bewuste keuze zijn.

Zie [`locale.md`](locale.md) voor meer.
