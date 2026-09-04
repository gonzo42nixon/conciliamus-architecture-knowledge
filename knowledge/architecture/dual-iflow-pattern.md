---
id: architecture/dual-iflow-pattern
type: Architecture Concept
title: Dual-iFlow Entkopplungsmuster
description: Trennung von Netzwerk-Ingest/Transport und atomarer Geschäftslogik zur Erzielung von Fehlertoleranz und Skalierbarkeit.
resource: btp://conciliamus/architecture/dual-iflow
tags: [architecture, pattern, dual-iflow, cpi, btp, decoupling, resilience]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: contains, target: /iflows/batch-receiver-iflow.md }
  - { type: contains, target: /iflows/item-processor-iflow.md }
  - { type: implements, target: /decisions/adr-001-dual-iflow-decoupling.md }
  - { type: dependsOn, target: /architecture/process-direct-interconnect.md }
  - { type: verifies, target: /verification/live-btp-execution.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Dual-iFlow Entkopplungsmuster

## Motivation & Problemstellung
Wird ein Batch von 10 oder mehr Geschäftspartnern in einem einzigen monolithischen iFlow verarbeitet, führt das Scheitern eines einzelnen Partner-Datensatzes (z.B. durch Validierungsfehler oder ERP-Sperren) unweigerlich zum Gesamtabbruch der Transaktion. Zudem blockiert ein langer sequentieller Lauf den eingehenden HTTP-Thread.

## Architektur-Lösung
Die Lösung teilt den Prozess streng in zwei lose gekoppelte Artefakte auf:

1. **`IFL_MDM_BP_Batch_Receiver` (Ingest- & Transport-Ebene):**
   - Nimmt den HTTPS-Batch entgegen.
   - Führt eine syntaktische Validierung des Gesamt-JSON durch.
   - Extrahiert Batch-Metadaten (`batchId`, `sourceSystem`, `bpTotalCount`).
   - Zerlegt den Batch via **Streaming Iterating Splitter** in Einzelsätze.
   - Übergibt jeden Satz an den internen Endpunkt `/conciliamus/v1/businesspartners/item`.
2. **`IFL_MDM_BP_Item_Processor` (Fachliche Verarbeitungs-Ebene):**
   - Agiert als atomarer Einzelverarbeiter.
   - Führt die fachliche Validierung (Email, Land, Pflichtfelder) durch.
   - Führt die OData GET Existenzprüfung aus.
   - Entscheidet über POST (Neuanlage) oder PATCH (Delta-Update).
   - Fängt Fehler isoliert im Exception Subprocess ab.

## Vorteile
- **Fehlerisolation:** Scheitert Partner #5, werden die Partner #1-4 und #6-10 davon nicht beeinträchtigt.
- **Unabhängige Skalierbarkeit:** Der Item Processor kann je nach Worker-Thread-Kapazität parallelisiert werden.
- **Wartbarkeit:** Änderungen an der OData-Struktur betreffen nur iFlow 2, nicht den Ingest-Kanal.
