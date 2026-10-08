# Beoordelaarsprompt (vastgelegd)

De beoordelaar krijgt per case het verzoek, de input, de invarianten en de verboden fouten, plus de outputs onder neutrale labels (X, Y, Z, W) in een per case geschudde volgorde. De beoordelaar weet niet welke conditie welk label is.

Score elke output op zes dimensies (0-3):

| Dimensie | 3 | 2 | 1 | 0 |
|---|---|---|---|---|
| inhoudsbehoud | alle invarianten intact, niets toegevoegd | lichte nuanceverschuiving | invariant verzwakt | feit, handeling, voorwaarde, actor of bron veranderd, of iets verzonnen |
| natuurlijk | goed Nederlands van een moedertaalschrijver | één stroeve plek | meerdere stijve of vertaalde constructies | even onnatuurlijk als de input of erger |
| register_stem | past precies bij lezer, kanaal, locale en stem | kleine afwijking | duidelijk verkeerd register of u/je gewisseld | verkeerd register of locale, of lekkage uit stemvoorbeeld |
| correctheid | foutloos Nederlands | één kleine fout | meerdere fouten | storende fouten |
| taak | doet precies wat gevraagd is | kleine afwijking | taak deels gemist | verkeerde taak |
| onnodig | alleen gewijzigd wat beter werd (ongewijzigd laten van goede tekst = 3) | paar overbodige ingrepen | veel overbodige ingrepen | goede tekst slechter gemaakt |

Daarnaast: **kritiek** (ja/nee). Ja bij elke betekenisfout die een lezer verkeerd zou informeren. Citeer bij elke score onder 3 en bij kritiek de concrete passage uit bron en output. Twijfel je, zeg dat (veld `twijfel`).
