---
id: digest/processdirect
type: Architecture Concept
title: "ProcessDirect Adapter (In-Memory iFlow-Verkettung)"
description: "In-Memory Direct Method Invocation ohne Serialisierungsoverhead oder Netzwerk-Latenz auf Basis des Apache Camel Direct Components."
resource: btp://conciliamus/digest/processdirect
tags: ["digest","concept","sap-integration","enterprise-erp-sap-btp","year-2018"]
status: verified
layer: 4
impact: 90
category: "SAP Integration"
year: "2018"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# ProcessDirect Adapter (In-Memory iFlow-Verkettung)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `ProcessDirect`
- **Meilenstein / Epoche:** Jahr 2018
- **Kategorie:** `SAP Integration`
- **Architektur-Ebene:** `Layer 4: Enterprise ERP & SAP BTP`
- **Impact-Score:** `90 / 100`

## Bedeutung in der SAP-Welt
Adapter zur schnellen, transaktionalen und lizenzeffizienten Kommunikation zwischen verschiedenen Integration Flows auf demselben Tenant.

## Fundamentale technische Bedeutung (Real World)
In-Memory Direct Method Invocation ohne Serialisierungsoverhead oder Netzwerk-Latenz auf Basis des Apache Camel Direct Components.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Verbindet iFlow 1 (Batch Receiver) mit iFlow 2 (Item Processor) nach ADR-005 – spart 100% JMS-Queue-Kosten und garantiert Sub-Millisekunden-Latenz.
