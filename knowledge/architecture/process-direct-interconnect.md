---
id: architecture/process-direct-interconnect
type: Architecture Concept
title: ProcessDirect Interconnect
description: Latenzfreie, speicherinterne Kommunikation zwischen Integration Flows innerhalb desselben Cloud Integration Tenants.
resource: btp://conciliamus/architecture/process-direct
tags: [architecture, process-direct, cpi, performance, in-memory, btp]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implements, target: /decisions/adr-002-process-direct.md }
  - { type: dependsOn, target: /architecture/dual-iflow-pattern.md }
  - { type: routesTo, target: /iflows/item-processor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# ProcessDirect Interconnect

## Funktionsweise
Der `ProcessDirect`-Adapter verbindet zwei Integration Flows, die auf demselben Worker-Node bzw. Tenant der SAP Cloud Integration laufen. Der Aufruf erfolgt über ein internes Java-Methoden-Routing im Hauptspeicher:
- **Kein TCP/IP Overhead:** Keine TLS-Verschlüsselung innerhalb der Tenant-Grenze nötig.
- **Keine Serialisierungskosten:** Objekte werden direkt im JVM-Speicher referenziert.
- **Transaktionale Konsistenz:** Fehlerzustände können synchron an den aufrufenden Flow propagiert werden, wenn konfiguriert.

## Konfiguration in Conciliamus
- **Sender-Adresse in `IFL_MDM_BP_Item_Processor`:** `/conciliamus/v1/businesspartners/item`
- **Receiver-Adapter in `IFL_MDM_BP_Batch_Receiver`:**
  - Adapter-Typ: `ProcessDirect`
  - Address: `/conciliamus/v1/businesspartners/item`
