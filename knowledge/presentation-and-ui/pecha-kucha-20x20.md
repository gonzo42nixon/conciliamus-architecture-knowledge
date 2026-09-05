---
id: presentation-and-ui/pecha-kucha-20x20
type: Presentation Concept
title: Pecha Kucha 20x20 Präsentationsarchitektur
description: Konzeption, Sprechtexte, Zeitsteuerung und technische Umsetzung der interaktiven 20x20 Präsentation (6:40 Min.).
resource: btp://conciliamus/ui/pecha-kucha
tags: [ui, pecha-kucha, presentation, timer, audio, firebase-auth]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: references, target: /decisions/adr-004-bpmn-method-and-style.md }
  - { type: references, target: /verification/live-btp-execution.md }
sources:
  - id: pecha-kucha-doc
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/pecha_kucha_konzept.md
    title: Pecha-Kucha-Präsentationskonzept
    author: "Dieter Rüffler"
---

# Pecha Kucha 20x20 Präsentationsarchitektur

## Formatregeln & Parameter
- **Folienanzahl:** Exakt 20 Folien.
- **Redezeit:** Exakt 20 Sekunden pro Folie (automatischer Folienwechsel).
- **Gesamtlaufzeit:** 6 Minuten 40 Sekunden (400 Sekunden).
- **Zielgruppe:** Markus Engelmann & Team *Plattform & Integration*, Conciliamus GmbH.

## Technische Implementierungsdetails
1. **Single-File Standalone HTML:** Vollständig autarke Datei (`docs/pecha_kucha_presentation.html`) mit base64-eingebetteten Screenshots.
2. **Audio Synthesizer:** Nutzung der browsernativen Web Audio API zur Erzeugung eines dezenten Chime-Signals (Gong) beim Folienübergang ohne externe Audio-Dateien.
3. **SVG-Timer Ring:** Animierter kreisförmiger Countdown-Indikator mit Restsekundenanzeige.
4. **Interaktives Folienraster:** Schnellübersicht aller 20 Folien per Tastendruck (`G`) mit Direktansprung.
5. **ORCAI Google Firebase Login & Schutz:**
   - Im ausgeloggten Zustand: Folien sind mit CSS-Filter `blur-md` unleserlich maskiert; Tastatur- und Klick-Events sind deaktiviert (`pointer-events: none`).
   - Schirm (`#pechaAuthShield`) fordert zur Google-Anmeldung auf.
