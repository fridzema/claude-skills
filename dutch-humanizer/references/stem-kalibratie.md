# Stemkalibratie

Als de gebruiker een eigen schrijfvoorbeeld aanlevert, imiteer hun stem. Dat is bijna altijd betere humanisering dan de generieke standaardaanpak.

## Werkwijze

1. **Lees het voorbeeld twee keer.** Eerste keer voor inhoud, tweede voor stijl.
2. **Maak intern een stijlprofiel** (niet opleveren tenzij de gebruiker erom vraagt). Let op:
   * **Zinslengte**: kort, lang, sterk wisselend?
   * **Lid-/vulwoorden** die deze schrijver wél gebruikt: "eigenlijk", "gewoon", "best wel", "trouwens", "overigens"? Welke zijn typisch voor deze persoon?
   * **Leestekens**: komma's, puntkommas, gedachtestreepjes (de echte, niet de AI-versie), drie puntjes?
   * **Persoonsvorm**: "ik", "we", "je", afstandelijk?
   * **Overgangen**: hoe verbindt deze schrijver alinea's? Met losse zinnen? Met "en", "maar"? Met witregels zonder verbinding?
   * **Eigenaardigheden**: terugkerende woorden, syntactische tics, registerwisseling, ironie, understatement.
   * **Wat ontbreekt**: geen drieslag-opsommingen? geen vetdruk? geen bullets? Dat is óók signaal.
3. **Vervang AI-patronen met patronen uit het voorbeeld.**
   * Een opgeblazen zin van AI vervang je door iets dat past bij hun gemiddelde zinslengte en woordkeuze.
   * Een drieledige opsomming? Kijk hoe deze schrijver opsommingen doet. Soms helemaal niet.
   * Een formele kop? Misschien gebruikt deze schrijver helemaal geen koppen.
4. **Behoud hun feiten en standpunten.** Stem aanpassen ≠ inhoud aanpassen. Als de input een mening bevat die niet in het stem-voorbeeld staat, verander de mening niet, alleen de toon.

## Wat NIET doen

* **Niet karikaturiseren.** Eén tic uit het voorbeeld in elke alinea herhalen klinkt geforceerd.
* **Niet hun fouten reproduceren.** Typo's, dt-fouten en losse leestekens komen meestal van haast, niet van stem. Corrigeer stilzwijgend.
* **Niet hun stem mengen** met die van een ander voorbeeld dat eerder in de conversatie kwam. Per opdracht één stem.
* **Niet hun stem op andere taken toepassen** tenzij de gebruiker daar expliciet om vraagt.
* **Niet de stem winnen van de inhoud.** Als de tekst een veiligheidswaarschuwing is, blijft die helder voorop staan, ook als de schrijver normaal lossere stijl heeft.

## Sjabloon (voor complexere taken)

Bij twijfel kun je kort vragen:

> Wil je dat ik de stijl van het voorbeeld letterlijk overneem (zinsritme, woordkeuze, leestekens) of alleen het register? En mag ik kortere zinnen maken dan in het voorbeeld als de inhoud daarom vraagt?

Niet automatisch vragen, alleen als het echt nodig is voor het resultaat.

## Zonder voorbeeld

Geen voorbeeld → val terug op:

* Het gedetecteerde register (zie hoofd-SKILL.md tabel).
* Standaard NL-stijl: helder, direct, geen opsmuk, korte zinnen waar het kan.
* De voorbeelden in `voorbeeld-zakelijk.md`, `voorbeeld-linkedin.md`, `voorbeeld-docs.md` of `voorbeeld-essay.md`, afhankelijk van het register.

## Combineren met de patroon-lijst

Stemkalibratie en `patronen.md` werken samen, niet tegen elkaar:

* `patronen.md` zegt **wat** je weghaalt.
* Stem-voorbeeld zegt **waarmee** je het vervangt.

Eerst patronen identificeren, dan stem als gids voor de herschrijving.
