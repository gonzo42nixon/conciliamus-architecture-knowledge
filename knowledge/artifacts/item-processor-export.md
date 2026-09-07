---
id: artifacts/item-processor-export
type: Implementation Artifact
title: "SAP Cloud Integration Export: IFL_MDM_BP_Item_Processor"
description: Provenienz und Inventar des analysierten SAP-Cloud-Integration-Exports des atomaren Business-Partner-Prozessors.
resource: artifact://conciliamus/IFL_MDM_BP_Item_Processor_Abgabe.zip
tags: [artifact, iflow, item-processor, provenance, sha256, sap-cloud-integration]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: verifies, target: /implementation/item-processor-observed.md }
  - { type: references, target: /iflows/item-processor-iflow.md }
sources:
  - id: item-processor-zip
    resource: artifact://conciliamus/IFL_MDM_BP_Item_Processor_Abgabe.zip
    title: IFL_MDM_BP_Item_Processor_Abgabe.zip
    author: "Dieter Rüffler"
---

# SAP Cloud Integration Export: IFL_MDM_BP_Item_Processor

## Integrität und Herkunft

- **Dateiname:** `IFL_MDM_BP_Item_Processor_Abgabe.zip`
- **SHA-256:** `2E9612DE744D3F5AA97D2CF1343327AF8CE7E1CF5B444BC238F1BFFB35653464`
- **Analysezeitpunkt:** 07.09.2026
- **Geheimnisse:** `SANDBOX_API_KEY` ist im Export leer; der Hash belegt ausschließlich die analysierte Version.

## Enthaltene Primärartefakte

- `src/main/resources/scenarioflows/integrationflow/IFL_MDM_BP_Item_Processor.iflw`
- `src/main/resources/script/ValidateBusinessPartnerItem.groovy`
- `src/main/resources/script/EvaluateODataExistenceResponse.groovy`
- `src/main/resources/script/BuildS4HanaPayload.groovy`
- `src/main/resources/script/HandleExceptionAndDLQ.groovy`
- `src/main/resources/parameters.prop`
- `src/main/resources/parameters.propdef`

## Evidenzgrenze

Der Export belegt Modell, Skripte und Design-Time-Adapterparameter. Er belegt weder den aktuellen Deploymentstatus noch externe Credentials, Tenant-Konfiguration, Laufzeit-Header oder erfolgreiche Nachrichtenverarbeitung.
