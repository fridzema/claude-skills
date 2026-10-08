# Voorbeeld: technische documentatie

Documentatie moet precies zijn. Formulematige documentatie leest als marketing met een codeblok. Een herschrijving haalt de verkoopzinnen weg en houdt elke technische bewering, elk pad en elke code letterlijk.

## Voor

> ## Aan De Slag Met Onze API
>
> Welkom! In deze handleiding nemen we je mee in de wereld van onze krachtige en flexibele API. Of je nu een ervaren ontwikkelaar bent of net begint, deze documentatie biedt jou alles wat je nodig hebt om naadloos aan de slag te gaan.
>
> ### Authenticatie
>
> Authenticatie is essentieel voor het waarborgen van de veiligheid van je integratie. Onze API maakt gebruik van een robuust token-gebaseerd systeem. Om te beginnen, dien je een API-token aan te maken in het dashboard onder Settings > API tokens. Vervolgens kun je deze token meegeven in de Authorization-header. Let op: Tokens vervallen na 90 dagen, dus vergeet niet om ze tijdig te roteren!
>
> ```
> Authorization: Bearer YOUR_TOKEN
> ```
>
> Een succesvol request retourneert `200 OK` met een JSON-array. Bij een ongeldig token ontvang je `401 Unauthorized`.
>
> Mocht je problemen ervaren, aarzel dan niet om contact op te nemen met ons toegewijde supportteam via support@example.com. We staan altijd klaar om je te helpen!

## Na (volledige herschrijving)

> ## Aan de slag met de API
>
> Deze handleiding is bedoeld voor zowel ervaren als beginnende ontwikkelaars en bevat alles om zonder moeite te beginnen.
>
> ### Authenticatie
>
> Authenticatie is nodig om je integratie te beveiligen. De API werkt met tokens: maak een API-token aan in het dashboard onder *Settings > API tokens* en stuur het mee in de `Authorization`-header:
>
> ```
> Authorization: Bearer YOUR_TOKEN
> ```
>
> Let op: tokens vervallen na 90 dagen, dus roteer ze op tijd.
>
> Een geslaagd request geeft `200 OK` met een JSON-array terug. Bij een ongeldig token krijg je `401 Unauthorized`.
>
> Problemen? Mail het supportteam via support@example.com.

## Wat is aangepakt

- Welkomstpraat en promotietaal: "Welkom!", "nemen we je mee in de wereld van", "krachtige en flexibele", "robuust", "We staan altijd klaar". "Naadloos aan de slag" wordt "zonder moeite beginnen": de bewering blijft, het modewoord gaat.
- Title Case in de kop, hoofdletter na "Let op:", uitroeptekens.
- "dien je ... aan te maken" wordt de gebiedende wijs.

## Bewust behouden

- Het codeblok, het menupad (met `>`, een functionele pijl), 90 dagen, de statuscodes, het e-mailadres en de inline code.
- De doelgroep, de belofte dat de handleiding alles bevat om te beginnen, en dat authenticatie nodig is voor beveiliging: dat zijn beweringen, geen opsmuk. Ze worden gewoner gezegd, niet geschrapt.
- "Roteren" blijft staan. Het is een vakterm en zegt iets anders dan "vervangen" of "herstarten"; verzin er ook geen uitleg bij die niet in de bron staat.

## Let op

Verzin geen endpoints, parameters, responsvelden, foutcodes, geldigheidsduur of supportkanalen. Een voorbeeldrequest met een verzonnen URL is ook een verzonnen feit.

## Bewust laten staan

**Input:** "Maak een API-token aan onder *Instellingen > Tokens*. Stuur het token mee in de `Authorization`-header. Tokens zijn 90 dagen geldig."
**Output:** dezelfde tekst, ongewijzigd.

Precies, kort en in de gebiedende wijs. De pijl in het menupad is functioneel, geen versiering.
