---
id: architecture/resilience-and-dead-letter
type: Architecture Concept
title: Resilienz & Dead-Letter-Behandlung
description: Zweikanalige Fehlerdifferenzierung in Business Errors (Audit Log) und Technical Errors (Data Store DLQ mit selektivem Replay).
resource: btp://conciliamus/architecture/resilience-dlq
tags: [architecture, resilience, error-handling, dlq, data-store, replay]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implements, target: /decisions/adr-004-data-store-dlq.md }
  - { type: contains, target: /iflows/reprocessor-iflow.md }
  - { type: handlesError, target: /iflows/item-processor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Resilienz & Dead-Letter-Behandlung

## Dual-Channel Fehlerbehandlung
In Enterprise-Schnittstellen dürfen fachliche Datenfehler niemals dieselbe Fehlerbehandlung wie technische Netzwerkausfälle durchlaufen:

```mermaid
flowchart TD
    ERR[Fehler im Item Processor] --> CLASSIFY{Fehlerursache}
    
    CLASSIFY -->|Ungültige Daten, Formatfehler, Dublette| BIZ[Fachlicher Fehler: FAILED_BUSINESS]
    CLASSIFY -->|Timeout, HTTP 500, Connection Refused| TECH[Technischer Fehler: FAILED_TECHNICAL]
    
    BIZ --> AUDIT[Audit Log & MPL Custom Status]
    BIZ --> NO_RETRY[Kein automatischer Wiederanlauf!]
    
    TECH --> DS[Data Store: BP_FAILED_QUEUE]
    DS --> REPLAY[Selektiver Replay via IFL_MDM_BP_Reprocessor]
```

## Fachliche Fehler (Non-Retryable)
- **Ursachen:** Fehlende `externalId`, ungültige E-Mail-Syntax, Land nicht ISO-2, Mehrfachtreffer im OData GET.
- **Behandlung:** Sofortige Protokollierung in den Message Attachments (`Validation_Errors.txt`), Status `FAILED_BUSINESS`. Ein erneutes automatisches Senden ist sinnlos, da der Fehler in den Daten liegt.

## Technische Fehler (Retryable)
- **Ursachen:** Timeout gegen S/4HANA, HTTP 503 Service Unavailable, Netzwerkunterbrechung.
- **Behandlung:** Der Original-Payload des Einzelsatzes wird als Eintrag in der persistenten Data Store Queue `BP_FAILED_QUEUE` gesichert.
- **Vorteil:** Nach Beseitigung der Störung kann der Satz einzeln verarbeitet werden, ohne den gesamten Batch erneut aus dem MDM anfordern zu müssen.
