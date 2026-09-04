---
id: decisions/adr-001-dual-iflow-decoupling
type: Decision Record
title: "ADR-001: Dual-iFlow Entkopplungsmuster"
description: Aufteilung der Integrationslogik in zwei separate iFlows zur Gewährleistung von Fehlerisolation und Ressourcenschonung.
resource: btp://conciliamus/decisions/ADR-001
tags: [adr, architecture-decision, dual-iflow, decoupling, cpi]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /architecture/dual-iflow-pattern.md }
  - { type: implementedBy, target: /iflows/batch-receiver-iflow.md }
  - { type: implementedBy, target: /iflows/item-processor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# ADR-001: Dual-iFlow Entkopplungsmuster

## Status
Akzeptiert (Accepted)

## Kontext
Ein externes MDM-System liefert Sammelbatches von Geschäftspartnern. Im Zielsystem SAP S/4HANA müssen Einzeloperationen durchgeführt werden. In einem monolithischen iFlow würde der Ausfall eines einzelnen Satzes den Gesamtbatch abbrechen und die HTTP-Verbindung des Senders unnötig lange blockieren.

## Entscheidung
Wir trennen die Verarbeitung strikt in:
1. `IFL_MDM_BP_Batch_Receiver` (Ingest, Validierung, Streaming-Split)
2. `IFL_MDM_BP_Item_Processor` (Einzelverarbeitung, Existenzcheck, POST/PATCH)

## Konsequenzen
- **Positiv:** Volle Fehlerisolation; scheiternde Datensätze blockieren nicht die erfolgreichen Partner.
- **Positiv:** Wartbarkeit und getrenntes Monitoring.
- **Negativ:** Zwei deployte iFlow-Artefakte im Tenant zu verwalten.
