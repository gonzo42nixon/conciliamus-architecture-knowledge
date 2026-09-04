---
id: data-contracts/custom-header-properties
type: Data Contract
title: Custom Header Properties & Message Processing Log (MPL)
description: Definition der im BTP Message Processing Log gesetzten Metadaten für Volltextsuche und Audit-Trails.
resource: btp://conciliamus/contracts/custom-headers
tags: [contract, monitoring, mpl, custom-headers, audit, fulltext-search]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /iflows/item-processor-iflow.md }
  - { type: verifies, target: /verification/live-btp-execution.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Custom Header Properties & Message Processing Log (MPL)

## Zweck
In der SAP Integration Suite können Nachrichten im Web-Monitoring über `Custom Header Properties` durchsucht werden. Dies ermöglicht es dem Betriebsteam, gezielt nach der externen MDM-ID oder der ermittelten SAP-Partnernummer zu suchen.

## Registrierte Properties

```groovy
def msgLog = messageLogFactory.getMessageLog(message)
if (msgLog != null) {
    msgLog.addCustomHeaderProperty("BatchId", batchId)
    msgLog.addCustomHeaderProperty("ExternalId", externalId)
    msgLog.addCustomHeaderProperty("CompanyName", company)
    msgLog.addCustomHeaderProperty("City", city)
    msgLog.addCustomHeaderProperty("Country", country)
    msgLog.addCustomHeaderProperty("Operation", plannedOperation) // POST oder PATCH
    msgLog.addCustomHeaderProperty("BP_Number", bpNumber)         // gefundene/neue ID
}
```

## Custom Status Werte (`SAP_MessageProcessingLogCustomStatus`)
- `POST_PLANNED`: Neuanlage ermittelt und vorbereitet
- `PATCH_PLANNED`: Existierender Datensatz erkannt, Update vorbereitet
- `VERIFIED_POST` / `VERIFIED_PATCH`: Erfolgreich an S/4HANA übermittelt
- `FAILED_BUSINESS`: Validierungsfehler (ungültige Mail, Dublette)
- `FAILED_TECHNICAL`: Netzwerk-/Timeout-Fehler (in DLQ gesichert)
