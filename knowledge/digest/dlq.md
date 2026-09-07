---
id: digest/dlq
type: Architecture Concept
title: "Dead Letter Queue & Technischer Fehlerpfad (Data Store)"
description: "Enterprise Integration Pattern (EIP): Nachrichten, die nach Erschöpfung der Retries nicht zugestellt werden können, werden in eine DLQ verschoben."
resource: btp://conciliamus/digest/dlq
tags: ["digest","concept","architektur","enterprise-erp-sap-btp","year-2003"]
status: verified
layer: 4
impact: 86
category: "Architektur"
year: "2003"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# Dead Letter Queue & Technischer Fehlerpfad (Data Store)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `DLQ`
- **Meilenstein / Epoche:** Jahr 2003
- **Kategorie:** `Architektur`
- **Architektur-Ebene:** `Layer 4: Enterprise ERP & SAP BTP`
- **Impact-Score:** `86 / 100`

## Bedeutung in der SAP-Welt
Data Store Fehlerspeicher zur Entkopplung technischer Ausfälle (z.B. Backend-Timeout) von fachlichen Validierungsfehlern.

## Fundamentale technische Bedeutung (Real World)
Enterprise Integration Pattern (EIP): Nachrichten, die nach Erschöpfung der Retries nicht zugestellt werden können, werden in eine DLQ verschoben.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Gemäß ADR-008 in DLQ_BusinessPartner_TechnicalErrors implementiert: Erlaubt selektiven Replay per ID ohne Neustart des Gesamtbatches.
