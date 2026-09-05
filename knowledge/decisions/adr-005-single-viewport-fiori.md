---
id: decisions/adr-005-single-viewport-fiori
type: Decision Record
title: "ADR-005: Single-Viewport Ergonomie für die Fiori-Lookalike Workbench"
description: Entwicklung einer schlanken Single-Page Web-App im SAP Fiori Horizon Lookalike-Design (ohne UI5-Framework-Overhead) mit striktem 100% no-outer-scroll Layout und interaktiven aufklappbaren JSON-Pills.
resource: btp://conciliamus/decisions/ADR-005
tags: [adr, architecture-decision, fiori-lookalike, ui-design, single-viewport, pills]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /presentation-and-ui/fiori-workbench-ui.md }
sources:
  - id: test-runner-app
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_runner_app.html
    title: SAP Fiori Lookalike Integration Test Runner & Workbench
    author: "Dieter Rüffler"
---

# ADR-005: Single-Viewport Ergonomie für die Fiori-Lookalike Workbench

## Status
Akzeptiert (Accepted)

## Kontext
Für die Demonstration und Validierung der SAP Cloud Integration Pipeline wird eine intuitive, visuelle Testoberfläche benötigt. 
Klassische SAPUI5/Fiori-Framework-Builds bringen oft signifikanten Bundle-Overhead, komplexe Launchpad-Abhängigkeiten und trägere Ladezeiten mit sich. Zudem wanderte in früheren Entwürfen der Container „INBOUND PAYLOAD“ durch feste Mindesthöhen auf kleineren Bildschirmen nach unten heraus, wodurch eine unvorteilhafte äußere Fensterscrollbar entstand.

## Entscheidung
1. **Fiori Horizon Lookalike-Architektur:** Bewusste Entscheidung für eine leichtgewichtige, performante Web-Applikation (Tailwind CSS, SAP 72 Font, Fiori Shellbar & Cards) im authentischen Fiori Horizon Design – ohne den Overhead eines vollen SAPUI5-Laufzeitstacks.
2. **Single-Viewport-Locking:** `html, body` werden auf `height: 100vh; overflow: hidden;` festgelegt (100% No-Outer-Scroll).
3. **Container-internes Scrollen:** Nur die Textarea bzw. der Pills-Baum erhalten `flex-1 min-h-0 overflow-y-auto`.
4. **Interaktive JSON-Pills:** Einführung eines hierarchischen, aufklappbaren Pill-Modus mit Farbstatus (POST/PATCH/FEHLER) zur schnellen Analyse umfangreicher Payloads.

## Konsequenzen
- **Positiv:** Authentischer, vertrauter Fiori-Look für Fachbereich und Prüfer bei subsekundären Ladezeiten und zero Bundle-Overhead.
- **Positiv:** Die Unterkante der Karte bleibt auf jedem Monitor immer sichtbar; keine störende Fensterscrollbar.
- **Positiv:** Signifikant höhere Übersichtlichkeit und spielerische Erkundung der Payload-Hierarchien.
