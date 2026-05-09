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

## Na (gehumaniseerd)

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
* **Tokencode-blok ongewijzigd** behouden. Code raak je nooit aan.
* **Slijmerige supportclaim**: "ons toegewijde supportteam staat altijd klaar" → vervangen door concreet kanaal.
* **Concrete details toegevoegd waar de input ze impliceerde** (90-dagen rotatie, response-codes), alleen als die feiten daadwerkelijk uit de productdocumentatie komen. Anders blijven generiek.

## Aandachtspunt

In docs is **precies > prettig**. Als je niet weet welke statuscode het systeem teruggeeft, schrijf dat niet op. Verzin geen endpoint-paden, parameter-namen of foutcodes om de tekst "completer" te maken.
