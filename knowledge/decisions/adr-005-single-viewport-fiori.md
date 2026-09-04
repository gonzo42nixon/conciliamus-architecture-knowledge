---
id: decisions/adr-005-single-viewport-fiori
type: Decision Record
title: "ADR-005: Single-Viewport Ergonomie für die Fiori Workbench"
description: Umstellung der Test-Runner Web-App auf ein striktes 100% no-outer-scroll Layout mit interaktiven aufklappbaren JSON-Pills.
resource: btp://conciliamus/decisions/ADR-005
tags: [adr, architecture-decision, fiori, ui-design, single-viewport, pills]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /presentation-and-ui/fiori-workbench-ui.md }
sources:
  - id: test-runner-app
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_runner_app.html
    title: SAP Fiori Integration Test Runner & Workbench
    author: "Dieter Rüffler"
---

# ADR-005: Single-Viewport Ergonomie für die Fiori Workbench

## Status
Akzeptiert (Accepted)

## Kontext
In früheren Fassungen wanderte der Container „INBOUND PAYLOAD“ durch feste Mindesthöhen (`min-h-[580px]`) auf kleineren Bildschirmen nach unten aus dem sichtbaren Bereich heraus, wodurch eine unvorteilhafte äußere Fensterscrollbar entstand.

## Entscheidung
1. **Single-Viewport-Locking:** `html, body` werden auf `height: 100vh; overflow: hidden;` festgelegt.
2. **Container-internes Scrollen:** Nur die Textarea bzw. der Pills-Baum erhalten `flex-1 min-h-0 overflow-y-auto`.
3. **Interaktive JSON-Pills:** Einführung eines hierarchischen, aufklappbaren Pill-Modus mit RGB-Farbstatus (POST/PATCH/FEHLER) zur schnellen Analyse umfangreicher Payloads.

## Konsequenzen
- **Positiv:** Die Unterkante der Karte bleibt auf jedem Monitor immer sichtbar; keine störende Fensterscrollbar.
- **Positiv:** Signifikant höhere Übersichtlichkeit und spielerische Erkundung der Hierarchien.
