---
id: decisions/adr-002-process-direct
type: Decision Record
title: "ADR-002: ProcessDirect statt Message Queues für iFlow-Kopplung"
description: Nutzung des ProcessDirect-Adapters zur latenzfreien internen Kopplung ohne JMS-Ressourcenbindung.
resource: btp://conciliamus/decisions/ADR-002
tags: [adr, architecture-decision, process-direct, jms, performance, cpi]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /architecture/process-direct-interconnect.md }
  - { type: dependsOn, target: /decisions/adr-001-dual-iflow-decoupling.md }
sources:
  - id: btp-doku
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/btp_setup_doku.md
    title: BTP Testaccount & Integration Suite Einrichtung
    author: "Dieter Rüffler"
---

# ADR-002: ProcessDirect statt Message Queues für iFlow-Kopplung

## Status
Akzeptiert (Accepted)

## Kontext
Für die Kopplung zwischen Ingestion- und Verarbeitungs-iFlow stehen auf SAP BTP Cloud Integration primär `ProcessDirect` und `JMS (Message Queues)` zur Verfügung. JMS erfordert ein separates Message-Queue-Kontingent (in Trial begrenzt, in Produktion kostenintensiv).

## Entscheidung
Wir nutzen den **`ProcessDirect`**-Adapter. Er verbindet Flows innerhalb desselben Tenants rein speicherintern (In-Memory Java Call), ohne TCP/IP-Overhead und ohne JMS-Queue-Kosten.

## Konsequenzen
- **Positiv:** Höchste Durchsatzrate und minimale Latenz.
- **Positiv:** Keine Abhängigkeit von JMS-Broker-Kapazitäten.
- **Negativ:** Synchroner Aufruf blockiert den Thread des aufrufenden Flows während der Ausführung.
