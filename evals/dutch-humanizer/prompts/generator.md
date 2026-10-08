# Generatorprompt (vastgelegd)

Elke run krijgt een verse agentcontext. De agent ziet alleen de takenmap, het pad van de geteste skill (of geen skill) en de outputmap. Niet de beoordelingsasserties, eerdere outputs, voorbeeldantwoorden of reparatieaanwijzingen.

## Conditie A: geen skill (eenvoudige redactieprompt)

> Je bent een ervaren Nederlandstalige redacteur. Voer het verzoek in elk takenbestand uit voor de gegeven input. Lever per taak alleen het resultaat dat je de gebruiker zou geven. Gebruik geen skills of andere bestanden dan de takenbestanden.

## Conditie B, C en D: met skill

> Je bent het model dat de skill gebruikt. Lees SKILL.md op het opgegeven pad en volg die; lees de referenties en gebruik het script alleen zoals de skill zegt. Gebruik geen andere geïnstalleerde versie van dutch-humanizer. Voer het verzoek in elk takenbestand uit en lever per taak precies wat de skill zegt te leveren.

Gemeenschappelijk: schrijf per taak de output letterlijk naar `<outputmap>/<ID>.txt`, verder niets. Bewerk geen bestanden buiten de outputmap.
