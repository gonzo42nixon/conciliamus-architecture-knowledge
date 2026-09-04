---
id: architecture/streaming-iterating-splitter
type: Architecture Concept
title: Streaming Iterating Splitter
description: Speicheroptimierte Zerlegung von JSON-Massen-Batches ohne Erzeugung von Java Out-Of-Memory Fehlern.
resource: btp://conciliamus/architecture/streaming-splitter
tags: [architecture, splitter, streaming, memory-management, cpi, json]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: contains, target: /iflows/batch-receiver-iflow.md }
  - { type: routesTo, target: /architecture/process-direct-interconnect.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Streaming Iterating Splitter

## Herausforderung
Große JSON-Batches mit hunderten oder tausenden Datensätzen überfordern den JVM-Heap von SAP Cloud Integration, wenn der gesamte Batch als DOM-Objektbaum in den Speicher geladen wird.

## Lösungsansatz in Conciliamus
1. **JSON-to-XML Konvertierung:** Der eingehende Batch wird in einen XML-Envelope transformiert.
2. **Iterating Splitter mit Streaming-Aktivierung:**
   - Expression Type: `XPath`
   - XPath Expression: `//businessPartners`
   - **Streaming Mode: Enabled (Checked):** Statt das gesamte Dokument einzulesen, nutzt der Splitter einen StAX-basierten Cursor (Streaming API for XML).
3. **XML-to-JSON Rücktransformation:** Jeder vereinzelte Datensatz wird im Stream zurück nach JSON formatiert und via ProcessDirect abgesetzt.
