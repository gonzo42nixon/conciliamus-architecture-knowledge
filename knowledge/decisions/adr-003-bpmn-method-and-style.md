---
id: decisions/adr-003-bpmn-method-and-style
type: Decision Record
title: "ADR-003: Modellierung nach Bruce Silver (BPMN 2.0 Method & Style)"
description: Durchgängige Anwendung der Nomenklatur- und Modellierungsstandards von Bruce Silver für selbstdokumentierende Enterprise-iFlows.
resource: btp://conciliamus/decisions/ADR-003
tags: [adr, architecture-decision, bpmn, method-and-style, bruce-silver, governance]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /iflows/batch-receiver-iflow.md }
  - { type: implementedBy, target: /iflows/item-processor-iflow.md }
sources:
  - id: bruce-silver-book
    resource: https://www.methodandstyle.com/books/bpmn-method-and-style/
    title: "BPMN Method and Style (2nd Edition)"
    author: "Bruce Silver"
---

# ADR-003: Modellierung nach Bruce Silver (BPMN 2.0 Method & Style)

## Status
Akzeptiert (Accepted)

## Kontext
Viele Integration Flows in Enterprise-Landschaften sind unleserlich modelliert: kryptische Task-Namen, unklare Gateway-Bedingungen, fehlende semantische Trennung von Aktionen und Zuständen.

## Entscheidung
Wir etablieren die Nomenklatur nach **Bruce Silver (Method & Style)**:
1. **Tasks:** Werden strikt als `[Aktiv-Verb] + [Objekt]` benannt (z.B. `Existenz prüfen`, `Delta patchen`, `Header registrieren`).
2. **Events:** Werden als Zustände im Partizip Perfekt formuliert (`Batch empfangen`, `Treffer ermittelt`).
3. **Gateways:** Der Gateway-Rhombus bleibt unbeschriftet; die ausgehenden Sequenzflüsse tragen die Bedingungen. Der Default-Pfad wird schraffiert gekennzeichnet.

## Konsequenzen
- **Positiv:** iFlows sind für Fachbereich, Betriebsführung und Entwickler sofort selbsterklärend.
- **Positiv:** Drastische Reduktion von Dokumentations- und Einarbeitungsaufwand.
