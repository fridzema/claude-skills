# Voorbeeld: technische documentatie

Technische tekst wil precies zijn, niet vriendelijk. AI maakt er marketing-met-een-codeblok van.

## Voor (AI-klinkend)

> ## Aan de slag met onze API
>
> Welkom! In deze handleiding nemen we je mee in de wereld van onze krachtige en flexibele API. Of je nu een ervaren ontwikkelaar bent of net begint, deze documentatie biedt jou alles wat je nodig hebt om naadloos aan de slag te gaan.
>
> Onze API is ontworpen om je workflow te optimaliseren en je in staat te stellen om robuuste, schaalbare integraties te bouwen. Met een breed scala aan endpoints en een intuïtieve, ontwikkelaar-vriendelijke ervaring, maakt het bouwen van data-gedreven applicaties eenvoudiger dan ooit.
>
> ### Authenticatie
>
> Authenticatie is essentieel voor het waarborgen van de veiligheid van je integratie. Onze API maakt gebruik van een robuust token-gebaseerd systeem, waarmee je veilig en betrouwbaar requests kunt versturen.
>
> Om te beginnen, dien je een API-token aan te maken in het dashboard. Vervolgens kun je deze token meegeven in de Authorization-header.
>
> ```
> Authorization: Bearer YOUR_TOKEN
> ```
>
> Mocht je problemen ervaren, aarzel dan niet om contact op te nemen met ons toegewijde supportteam. We staan altijd klaar om je te helpen!

## Na, variant A: input bevat geen specifieke product-details

Gebruik deze variant als de input alleen het marketing-proza bevat (geen genoemd dashboard-pad, geen genoemde token-rotatie, geen genoemde response-codes). Houd de tekst feitelijk en algemeen.

> ## API quickstart
>
> Deze handleiding beschrijft hoe je een eerste request stuurt.
>
> ### Authenticatie
>
> De API gebruikt bearer-tokens. Maak een token aan in het dashboard en stuur deze mee in de `Authorization`-header:
>
> ```
> Authorization: Bearer YOUR_TOKEN
> ```
>
> ### Eerste request
>
> ```bash
> curl https://api.example.com/v1/users \
>   -H "Authorization: Bearer YOUR_TOKEN"
> ```
>
> Een ongeldig token wordt geweigerd. Voor andere problemen: open een ticket of mail support@example.com.

## Na, variant B: input of bron-documentatie bevat concrete details

Gebruik deze variant *alleen* als deze details daadwerkelijk uit de productdocumentatie of de input komen: dashboard-pad `Settings → API tokens`, 90-dagen token-lifetime, response-codes `200 OK` / `401 Unauthorized`, support-emailadres.

> ## API quickstart
>
> Deze handleiding beschrijft hoe je een eerste request stuurt.
>
> ### Authenticatie
>
> De API gebruikt bearer-tokens. Maak een token aan in het dashboard onder *Settings → API tokens* en stuur deze mee in de `Authorization`-header:
>
> ```
> Authorization: Bearer YOUR_TOKEN
> ```
>
> Tokens vervallen na 90 dagen. Roteer ze via hetzelfde dashboard.
>
> ### Eerste request
>
> ```bash
> curl https://api.example.com/v1/users \
>   -H "Authorization: Bearer YOUR_TOKEN"
> ```
>
> Een geslaagd request geeft `200 OK` met een JSON-array terug. Bij een ongeldig token krijg je `401 Unauthorized`.
>
> Loopt iets niet? Open een ticket of mail support@example.com.

## Welke patronen zijn hersteld

* **Welkomst-fluff**: "Welkom!", "nemen we je mee in de wereld van", "Of je nu een ervaren ontwikkelaar bent of net begint" → weg.
* **Promotioneel taalgebruik**: "krachtige en flexibele", "naadloos", "robuuste, schaalbare", "intuïtieve, ontwikkelaar-vriendelijke" → weg. Documentatie verkoopt niet.
* **Bijvoeglijk-naamwoord-stapeling** + Engelse koppeltekens ("data-gedreven") → weg/aaneen ("datagedreven").
* **AI-vocabulaire**: "optimaliseren", "in staat stellen", "een breed scala aan", "essentieel voor het waarborgen" → weg.
* **Code-blok ongewijzigd** behouden. Code raak je nooit aan.
* **Slijmerige supportclaim**: "ons toegewijde supportteam staat altijd klaar" → vervangen door concreet kanaal.
* **Concrete details (variant B)** alleen toegevoegd als ze uit de echte productdocumentatie komen.

## Aandachtspunt

In docs is **precies > prettig**. De grootste valkuil is dat een rewrite "completer" wil voelen. Concreet noemen wat je niet zeker weet is een hallucinatie:

- ❌ Verzin geen endpoint-paden ("`POST /v1/users/create`" als je niet weet of dat klopt).
- ❌ Verzin geen parameter-namen, response-velden of foutcodes.
- ❌ Verzin geen lifetimes ("tokens vervallen na 90 dagen") als die niet gedocumenteerd zijn.
- ❌ Verzin geen support-kanalen ("mail support@example.com" als dat niet de echte werkwijze is).

Bij twijfel: variant A. Algemener is veiliger dan onjuist.
