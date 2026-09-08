---
id: architecture/message-format-transformations
type: Architecture Concept
title: Nachrichtenformat-Transformationen vom MDM-Batch zur S/4HANA OData Payload
description: Vollständige Format- und Strukturänderungen in Batch Receiver und Item Processor von JSON über XML und atomare JSON-Nachrichten bis zur OData Payload.
resource: btp://conciliamus/architecture/message-format-transformations
tags: [message-format, transformation, json, xml, batch, business-partner, odata, payload, btp, integration-suite]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-08T12:00:00+02:00"
relations:
  - { type: partOf, target: /architecture/dual-iflow-pattern.md }
  - { type: describes, target: /iflows/batch-receiver-iflow.md }
  - { type: describes, target: /iflows/item-processor-iflow.md }
  - { type: uses, target: /data-contracts/mdm-inbound-contract.md }
  - { type: produces, target: /data-contracts/s4-odata-mapping.md }
sources:
  - id: batch-receiver-design
    resource: https://b9c123f3trial.integrationsuite-trial01.cfapps.us10-001.hana.ondemand.com/shell/design/contentpackage/ConciliamusBusinessPartnerIntegration/integrationflows/IFL_MDM_BP_Batch_Receiver
    title: IFL_MDM_BP_Batch_Receiver im SAP Integration Suite Designer
    author: Conciliamus
  - id: batch-example
    resource: https://orcai-54321.web.app/json/?key=ORCAI-260907-16H03-JSON-2ZSPP
    title: Beispielnachricht MDM Business-Partner-Batch
    author: Conciliamus
  - id: item-processor-design
    resource: https://b9c123f3trial.integrationsuite-trial01.cfapps.us10-001.hana.ondemand.com/shell/design/contentpackage/ConciliamusBusinessPartnerIntegration/integrationflows/IFL_MDM_BP_Item_Processor
    title: IFL_MDM_BP_Item_Processor im SAP Integration Suite Designer
    author: Conciliamus
  - id: item-example
    resource: https://orcai-54321.web.app/json/?key=ORCAI-260908-20H20-JSON-4ZXFY
    title: Atomare Business-Partner-Nachricht
    author: Conciliamus
  - id: odata-payload-example
    resource: https://orcai-54321.web.app/json/?key=ORCAI-260908-20H27-JSON-Q6HKH
    title: Erzeugte S/4HANA OData Payload
    author: Conciliamus
---

# Nachrichtenformat-Transformationen

Die Nachrichtenstruktur verändert sich an vier fachlich relevanten Stellen in zwei iFlows.

## IFL_MDM_BP_Batch_Receiver – Folie 8

Der Batch Receiver startet mit dem JSON-Batch `ORCAI-260907-16H03-JSON-2ZSPP`.

1. **`Convert Batch JSON to XML Envelope`**
   - Eingang: ein JSON-Batch mit mehreren Business Partnern.
   - Ausgang: ein XML-Envelope mit denselben Batch- und Partnerdaten.
   - Grund: Die nachfolgende XPath-basierte Zerlegung benötigt eine XML-Struktur.
2. **`Split Batch into Individual Business Partners`**
   - Eingang: der XML-Envelope des gesamten Batches.
   - Ausgang: einzelne XML-Nachrichten, jeweils genau ein Business Partner.
   - Änderung: Aus einer Batch-Nachricht entstehen mehrere atomare Nachrichten.
3. **`Transform Business Partner to JSON Item`**
   - Eingang: eine atomare XML-Nachricht.
   - Ausgang: eine atomare JSON-Nachricht für einen Business Partner.
   - Diese Nachricht wird über ProcessDirect an den Item Processor übergeben.

## IFL_MDM_BP_Item_Processor – Folie 9

Der Item Processor startet mit der atomaren JSON-Nachricht
`ORCAI-260908-20H20-JSON-4ZXFY`.

4. **`Build S/4HANA OData Payload`**
   - Eingang: das interne JSON-Modell eines Business Partners.
   - Ausgang: eine auf das S/4HANA-Zielmodell zugeschnittene OData Payload.
   - Die erzeugte Payload ist unter `ORCAI-260908-20H27-JSON-Q6HKH` belegt.
   - Sie dient nach der Existenzprüfung abhängig vom Router-Ergebnis als Grundlage
     für die POST-Neuanlage oder die PATCH-Aktualisierung.

## Formatkette

`JSON-Batch → XML-Envelope → einzelne XML-Business-Partner → atomare JSON-Items → S/4HANA OData JSON Payload`

Damit sind sowohl reine Formatwechsel als auch die strukturelle Zerlegung des
Batches und die semantische Transformation in das SAP-Zielmodell dokumentiert.
