---
id: iflows/batch-receiver-iflow
type: iFlow Specification
title: "IFL_MDM_BP_Batch_Receiver: Batch Ingest & Dispatcher"
description: Spezifikation des Ingestion-iFlows zur Annahme von MDM-Massen-Batches, syntaktischen Vorvalidierung und Streaming-Zerlegung.
resource: btp://conciliamus/iflows/IFL_MDM_BP_Batch_Receiver
tags: [iflow, batch-receiver, cpi, btp, bpmn, streaming, ingest]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: partOf, target: /architecture/dual-iflow-pattern.md }
  - { type: routesTo, target: /iflows/item-processor-iflow.md }
  - { type: implements, target: /decisions/adr-004-bpmn-method-and-style.md }
  - { type: verifies, target: /verification/live-btp-execution.md }
sources:
  - id: btp-doku
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/btp_setup_doku.md
    title: BTP Testaccount & Integration Suite Einrichtung
    author: "Dieter Rüffler"
---

# IFL_MDM_BP_Batch_Receiver

## Technische Kenndaten
- **Paket:** `Conciliamus - Business Partner Integration`
- **Technischer Name:** `IFL_MDM_BP_Batch_Receiver`
- **Inbound-Adapter:** HTTPS
- **URL-Pfad:** `/http/conciliamus/v1/businesspartners/batch`
- **Sicherheits-Level:** Rollenbasiert (`ESBMessaging.send`) + OAuth 2.0 Client Credentials Grant
- **CSRF-Schutz:** Konfiguriert im HTTPS-Sender
- **Status im Tenant:** `Deployed` / `Started`

## Modellierung nach Bruce Silver (Method & Style)
1. **Start-Event:** `Batch empfangen`
2. **Task 1:** `Syntax validieren` (Groovy Script: Prüfung auf gültiges JSON und Vorhandensein von `batchId` und `businessPartners`).
3. **Task 2:** `Metadaten extrahieren` (Content Modifier: `batchId`, `sourceSystem`, `bpTotalCount`).
4. **Task 3:** `JSON zu XML konvertieren` (JSON-to-XML Converter).
5. **Task 4:** `Datensätze vereinzeln` (Iterating Splitter: XPath `//businessPartners`, Streaming Mode aktiviert).
6. **Task 5:** `XML zu JSON transformieren` (XML-to-JSON Converter).
7. **Task 6:** `Einzelsatz übergeben` (ProcessDirect Adapter an `/conciliamus/v1/businesspartners/item`).
8. **End-Event:** `Batch zerlegt`
