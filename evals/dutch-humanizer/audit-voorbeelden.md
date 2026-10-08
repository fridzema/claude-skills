# Auditlog voorbeelden v0.7.0

Controle in twee richtingen (output naar bron, bron naar output) van alle voor/na-paren in `references/`. Eerste ronde door de ontwikkelaar (opdracht v0.7.0, sectie 5), tweede ronde door een onafhankelijke auditagent (66 paren, 9 kritiek, ongeveer 37 klein). Kritieke bevindingen zijn allemaal verwerkt; kleine bevindingen grotendeels. "Regressie" verwijst naar een test of evaluatiecase die het onderliggende risico afdekt.

| Bron | Was | Wijziging | Rationale | Regressie |
|---|---|---|---|---|
| voorbeeld-linkedin | "Dat kwam door een andere manier van werken" | "Het gaat niet om de tools, maar om de mindset." | Geen nieuw causaal verband; ook geen motief in het verleden ("Het ging ons niet om") | ontwikkelset 07 |
| voorbeeld-linkedin | "Concurrenten deden het in 3." | "in 3 dagen" | Eenheid niet impliciet naast "11 werkdagen" | `test_compound_units`; R01 |
| voorbeeld-linkedin | "Het resultaat?" weg; "We veranderden drie dingen" | "Het resultaat:"; "Drie inzichten veranderden onze aanpak"; labels behouden | Oorzakelijk verband en framing als inzichten blijven | validatie V23 (koppeling) |
| principes, geval C | "Na goedkeuring krijgt de klant..." | "Zodra de goedkeuring binnen is, ..." | "Zodra" bevat een timingeis | probe-signaal TIMING |
| principes, geval D; slack; patronen 9, 34 | "waarschijnlijk", "vermoeden", "vermoedelijk" voor "lijkt" | "lijkt", "aanwijzingen", "mogelijk" | Aanwijzing is geen kansinschatting | signaalfamilie EVIDENTIAL; validatie V03 |
| principes, geval E en F | Goed-versie herschreef "opleveren" en maakte van een regel een opdracht | Bron ongewijzigd als goede uitkomst | Communicatieve handeling en actor blijven | `test_..._prose_vs_code` n.v.t.; validatie V07, V10 |
| principes, geval G (nieuw) | - | Voorstel blijft voorstel | Communicatieve handeling | validatie V01, V24 |
| principes 1, 4 | Vraag toegevoegd; "zou graag voorstellen" werd "Ik wil" | Bewering blijft met "kan"; "Ik stel voor" | Geen sterkere claim, voorstel blijft voorstel | validatie V01 |
| voorbeeld-docs | "Vervang ze op tijd" | "dus roteer ze op tijd" | Roteren is een vakterm; "dus" blijft | validatie V04 |
| patronen 5 | Afgewezen optie werd "kan ook" | "De voor de hand liggende aanpak is ..." | Afweging en waardering blijven | ontwikkelset 12 |
| patronen 6 | Mogelijkheden werden gebeurtenissen in de verleden tijd | "kan ... toch eindigen" | Modaliteit blijft | n.v.t. |
| patronen 11 | "De update brengt ..." (verzonnen onderwerp) | Drie beweringen met hun eigen effect | Niets toevoegen, niets weglaten | validatie V05 |
| patronen 16 | "daarmee onmisbaar" (nieuw verband) | Bewering zonder "daarmee" | Geen causaal verband toevoegen | n.v.t. |
| patronen 23 | "Daarom" gold voor beide redenen | "Omdat klanten ..." | Alleen de bron-reden is reden | n.v.t. |
| patronen 27 | "bijzin voorop met komma is Engels" | Voorzetselgroep met komma vóór de persoonsvorm | Bewering over Nederlandse zinsbouw was onjuist | n.v.t. |
| patronen 31; SKILL.md | "bij een zelfstandige zin komen beide voor" | Kleine letter na verklaring, ook bij volledige zin | Taaladvies, "Hoofdletter na dubbele punt" (gecontroleerd 2026-10-08) | `test_capital_after_colon_is_info_only`; validatie V16 |
| voorbeeld-zakelijk | "krappe bezetting" voor "resourcing"; "we" ingevoegd; "zie ik twee opties" | "capaciteit en middelen"; onpersoonlijk; "scenario's bekijken"; uitkijken naar samenwerking terug | Geen concretisering zonder bron; geen nieuwe actor | ontwikkelset 02 |
| voorbeeld-support | "Ik heb uw situatie zorgvuldig bekeken" weggelaten | "Ik heb uw situatie bekeken:" | Feitelijke bewering en bron van de aanwijzing | validatie V02 |
| voorbeeld-essay | Beweringen weggelaten, mogelijkheid werd feit, vergelijking verzonnen | Volledig herschreven; elke bewering terug | Uitleg "elke bewering blijft" was onwaar | ontwikkelset 32 |
| voorbeelden, intro's | "AI-tekst maakt er ... van"; "Zakelijk Nederlands is van nature direct" | "Formulematige tekst ..."; leesadvies | Geen claim over AI-auteurschap of culturele generalisatie | n.v.t. |
| principes 4 | "Nederlands volgt vaker dan Amerikaans-Engels ..." | Leesadvies met bron (Onze Taal) | Onbewezen culturele generalisatie | n.v.t. |
| alle voorbeeldbestanden | Alleen herschrijfvoorbeelden | "Bewust laten staan" in zakelijk, support, docs | Ongewijzigd laten is een geldige uitkomst | validatie V09, V10 |

Bewust niet overgenomen uit de audit: suggesties die een vorm van de bron letterlijk zouden terugzetten waar de herschrijving een gelijkwaardige gewone formulering koos (bijvoorbeeld "probleemloos" tegenover "naadloos"); daar gaat het om woordkeus, niet om betekenis.
