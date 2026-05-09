# Voorbeeld: Slack/Teams update (incident, status, korte mededeling)

Chat-berichten zijn de plek waar AI-tone het meest opvalt. Een formeel incident-bericht in Slack leest direct als gegenereerd. Echte chat is fragmentair, urgent en zonder pleasantries.

## Voor (AI-klinkend)

> Beste team,
>
> Ik wil jullie informeren over een lopend incident dat momenteel onze checkout-functionaliteit beïnvloedt. Sinds 14:07 vandaag observeren wij een toename in time-out errors, met name bij gebruikers die de betaalstap proberen te voltooien.
>
> Ons engineering-team is actief bezig met het onderzoeken van de oorzaak. We hebben de eerste indicaties dat het mogelijk gerelateerd is aan onze betaalprovider, maar dit is op dit moment nog niet definitief bevestigd.
>
> Wij zullen jullie zo spoedig mogelijk een update sturen zodra we meer informatie hebben. In de tussentijd vragen we om jullie geduld en willen we benadrukken dat we de hoogste prioriteit aan deze kwestie geven.
>
> Mocht je in de tussentijd vragen ontvangen van klanten of stakeholders, verwijs ze gerust door naar het support-team voor de meest actuele status.
>
> Bedankt voor jullie begrip!

## Na (gehumaniseerd)

> Incident: checkout time-outs sinds 14:07.
>
> Symptoom: gebruikers krijgen een time-out op de betaalstap.
> Vermoeden: probleem bij de betaalprovider, nog niet bevestigd.
> Onderzoek: engineering kijkt nu.
>
> Volgende update: 14:30, of eerder als we meer weten.
>
> Klantvragen → support.

## Welke patronen zijn hersteld

* **Aanhef in chat**: "Beste team," → weg. Slack heeft geen aanhef nodig.
* **Vulzinnen**: "Ik wil jullie informeren over", "we hebben de eerste indicaties dat het mogelijk", "in de tussentijd vragen we om", "willen we benadrukken" → weg.
* **Officialese**: "lopend incident dat momenteel onze checkout-functionaliteit beïnvloedt" → "checkout time-outs".
* **Hedging-stapeling**: "mogelijk", "nog niet definitief bevestigd", "zo spoedig mogelijk" → één keer noemen ("vermoeden, niet bevestigd").
* **Slijmerige afsluiter**: "Bedankt voor jullie begrip!" → weg.
* **Concrete update-tijd toegevoegd** (14:30): alleen als die in de input-context bekend is. Bij twijfel: "volgende update: zo snel mogelijk" of de tijd uit de input behouden.
* **Format**: chat staat fragmentair toe. Korte zinnen en labels (`Symptoom:`, `Vermoeden:`, `Onderzoek:`) zijn beter dan een lopende alinea.

## Aandachtspunt

Behoud altijd: tijdstempels, getroffen systemen, klantgegevens, ticketnummers, namen.

In incident-updates: **wees expliciet over wat je weet versus wat je vermoedt**. AI mengt deze door elkaar ("we hebben aanwijzingen dat het mogelijk gerelateerd is" leest als wishy-washy zekerheid). Beter: scheiden in `feit` / `vermoeden` / `onbekend`.

Verzin geen tijdstempels of root-causes. Als je niet weet wanneer de volgende update komt, schrijf "volgende update: zo snel mogelijk", niet "14:30".
