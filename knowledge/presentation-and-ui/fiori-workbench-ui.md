---
id: presentation-and-ui/fiori-workbench-ui
type: UI Concept
title: SAP Fiori Integration Workbench & Test-Runner
description: Architektur der Single-Viewport Fiori Horizon Web-Applikation mit aufklappbaren RGB-JSON-Pills und Monitoring-Drawer.
resource: btp://conciliamus/ui/fiori-workbench
tags: [ui, fiori, workbench, json-pills, single-viewport, test-runner, firebase-auth]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implements, target: /decisions/adr-005-single-viewport-fiori.md }
  - { type: verifies, target: /verification/live-btp-execution.md }
sources:
  - id: test-runner-app
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_runner_app.html
    title: SAP Fiori Integration Test Runner & Workbench
    author: "Dieter Rüffler"
---

# SAP Fiori Integration Workbench & Test-Runner

## Ergonomie: 100% Single-Viewport Design
- **Keine äußere Fensterscrollbar:** `html, body { height: 100vh; overflow: hidden; }`
- **Volle Bildschirmausnutzung:** Die Karte „INBOUND PAYLOAD“ nutzt flexibel (`flex-1 min-h-0 h-full`) den gesamten vertikalen Raum bis zum unteren Bildschirmrand.
- **Innere Fiori-Scrollbars:** Nur die Payload-Container (`#jsonInput` bzw. `#pillsTreeRoot`) scrollen intern bei Bedarf.

## Interaktiver JSON-Pills-Modus
Über einen Toggle-Switch kann zwischen **Rohem JSON-Code** und **Aufklappbaren JSON-Pills** umgeschaltet werden:
1. **Level 1 (Batch-Pill):** Ovale blaue Pill mit Batch-ID, Erstellungsdatum und Quellsystem (`JSD-MDM`).
2. **Level 2 (Partnerliste-Pill):** Grüne Pill mit Datensatzanzahl.
3. **Level 3 (Partner-Pills):**
   - 🟣 **POST:** Neuanlage
   - 🟠 **PATCH:** Existierender Datensatz (`CUST15`, `BECHTLE AG`, `XYZ-PEPPOL`)
   - 🔴 **FEHLER:** Validierungsfehler bei ungültigen Daten
4. **Interaktion:** Klick auf eine Pill klappt die nächste Ebene ein oder aus. Buttons für „Alle aufklappen“ und „Alles zuklappen“.

## Monitoring-Drawer (sap.m.SideSheet)
Ein aufklappbarer Seitendrawer bietet detaillierte Einsicht in:
- Ausführungsprotokoll & Timing
- HTTP Request & Response Headers
- Direktlinks zu den deployed iFlow-Screenshots (Google Photos)
- Literatur-Empfehlungen (Bruce Silver: *BPMN Method & Style*, Rheinwerk Verlag: *KI mit SAP*)
