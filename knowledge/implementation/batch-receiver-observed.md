---
id: implementation/batch-receiver-observed
type: Observed Implementation
title: "Beobachtete Implementierung des IFL_MDM_BP_Batch_Receiver"
description: Aus dem CPI-Export extrahierter Ist-Ablauf für HTTPS-Annahme, Validierung, Streaming-Split und ProcessDirect-Weitergabe.
resource: btp://conciliamus/implementation/IFL_MDM_BP_Batch_Receiver
tags: [implemented, iflow, batch, https, splitter, processdirect]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: implements, target: /iflows/batch-receiver-iflow.md }
  - { type: dependsOn, target: /artifacts/batch-receiver-export.md }
  - { type: routesTo, target: /implementation/item-processor-observed.md }
---

# Beobachtete Implementierung des Batch Receivers

## Ausführungsfolge

1. `MDM Batch Received` nimmt per HTTPS einen JSON-Batch an.
2. `Validate Batch & Set Audit Properties` ruft `ValidateBatchInbound.groovy` auf.
3. `Convert Batch JSON to XML Envelope` erzeugt ein XML-Dokument mit Root-Element `root`.
4. `Split Batch into Individual Business Partners` iteriert über `//businessPartners`.
5. `Transform Business Partner to JSON Item` wandelt jedes Split-Ergebnis zurück nach JSON.
6. `All Business Partners Dispatched` übergibt die Einzelnachricht über ProcessDirect.

## Beobachtete Adapter- und Splitterparameter

| Parameter | Exportierter Wert |
|---|---|
| HTTPS-Pfad | `/conciliamus/v1/businesspartners/batch` |
| Sender-Authentisierung | rollenbasiert |
| Rolle | `ESBMessaging.send` |
| Inbound-XSRF-Schutz | aktiviert |
| Splittertyp | Iterating Splitter |
| Ausdruck | `//businessPartners` |
| Streaming | `true` |
| Parallelverarbeitung | `false` |
| Timeout | `300` Sekunden |
| SplitterThreads | `10` |
| ProcessDirect-Ziel | `/conciliamus/v1/businesspartners/item` |

`SplitterThreads=10` aktiviert bei `ParallelProcessing=false` keine parallele Verarbeitung. Die beobachtete Semantik ist sequenziell.

## Validierung

`ValidateBatchInbound.groovy` verlangt `batchId` und ein als Liste interpretierbares `businessPartners`-Feld. Es setzt `batchId`, `createdAt`, `sourceSystem` und `bpTotalCount` als Exchange Properties und registriert Audit-Informationen im MPL.
