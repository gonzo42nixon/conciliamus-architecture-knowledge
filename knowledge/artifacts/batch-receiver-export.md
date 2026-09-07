---
id: artifacts/batch-receiver-export
type: Implementation Artifact
title: "SAP Cloud Integration Export: IFL_MDM_BP_Batch_Receiver"
description: Provenienz und Inventar des analysierten SAP-Cloud-Integration-Exports für Batch-Annahme, Konvertierung, Split und ProcessDirect-Dispatch.
resource: artifact://conciliamus/IFL_MDM_BP_Batch_Receiver.zip
tags: [artifact, iflow, batch-receiver, provenance, sha256, sap-cloud-integration]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: verifies, target: /implementation/batch-receiver-observed.md }
  - { type: references, target: /iflows/batch-receiver-iflow.md }
sources:
  - id: batch-receiver-zip
    resource: artifact://conciliamus/IFL_MDM_BP_Batch_Receiver.zip
    title: IFL_MDM_BP_Batch_Receiver.zip
    author: "Dieter Rüffler"
---

# SAP Cloud Integration Export: IFL_MDM_BP_Batch_Receiver

## Integrität und Herkunft

- **Dateiname:** `IFL_MDM_BP_Batch_Receiver.zip`
- **SHA-256:** `364FF44BFE3CCCA54241C92A4D5B6F346C98F07BC4A8D178DEBE080043FB2F40`
- **Analysezeitpunkt:** 07.09.2026

## Enthaltene Primärartefakte

- `src/main/resources/scenarioflows/integrationflow/IFL_MDM_BP_Batch_Receiver.iflw`
- `src/main/resources/script/ValidateBatchInbound.groovy`
- `src/main/resources/parameters.prop`
- `src/main/resources/parameters.propdef`

## Evidenzgrenze

Der Export belegt das Design-Time-Modell einschließlich HTTPS-, Splitter- und ProcessDirect-Konfiguration. Er belegt keine aktive Deploymentversion und keinen konkreten Lauf im BTP-Tenant.
