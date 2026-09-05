---
id: decisions/adr-003-end-to-end-correlation-mpl
type: Decision Record
title: "ADR-003: End-to-End Correlation & MPL Governance"
description: Durchgängige Rückverfolgbarkeit von Massen-Batches und Einzelnachrichten mittels globaler Correlation-ID und Custom Header Properties im SAP Message Processing Log.
resource: btp://conciliamus/decisions/ADR-003
tags: [adr, architecture-decision, governance, observability, mpl, correlation-id, custom-header-properties, monitoring]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T22:45:00Z"
relations:
  - { type: implements, target: /data-contracts/custom-header-properties.md }
  - { type: dependsOn, target: /iflows/item-processor-iflow.md }
sources:
  - id: cpi-mpl-doc
    resource: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-processing-log
    title: SAP Cloud Integration Message Processing Log (MPL)
    author: "SAP SE"
---

# ADR-003: End-to-End Correlation & MPL Governance

## Status
Akzeptiert (Accepted)

## Kontext
Bei verteilten Integrationsprozessen (MDM Quellsystem ➔ BTP CPI Ingest ➔ ProcessDirect Bus ➔ S/4HANA Backend) führt ein Mangel an durchgängiger Transparenz im Fehlerfall zu langwieriger Ursachenforschung. Standardmäßig vergibt jeder iFlow eine eigene interne `MessageGuid`. Ohne systemübergreifende Korrelation müssen Support-Mitarbeiter tausende Log-Einträge manuell abgleichen oder sensible Roh-Payloads herunterladen, was Datenschutzrichtlinien verletzt.

## Entscheidung
Wir haben entschieden, ein **durchgängiges Observability- und Governance-Modell** auf Basis von SAP-Correlation-IDs und indizierten Custom Header Properties zu etablieren:

1. **Globale SAP-CorrelationID:**
   - Der Ingest-Flow (`IFL_MDM_BP_Batch_Receiver`) übernimmt eine übergebene `SAP-CorrelationID` oder generiert beim Eintreffen des Batches eine eineindeutige GUID (`${header.SAP-CorrelationID}`).
   - Diese Correlation-ID wird über den ProcessDirect-Header transparent an den `IFL_MDM_BP_Item_Processor` weitergereicht.
2. **Indizierte Custom Header Properties im MPL:**
   - Für jede verarbeitete Nachricht werden zentrale Geschäftsmetadaten programmatisch in das Message Processing Log geschrieben:
     - `MDM_Batch_ID`: Identifikator des Gesamtbatches
     - `BusinessPartner_ID`: Externe Partnernummer aus dem Quellsystem
     - `Processing_Action`: Geplante Operation (`POST` oder `PATCH`)
     - `S4_Partner_Number`: Finale interne S/4HANA-Nummer (nach erfolgreichem Call)
3. **Payload-freie Fehlerdiagnose:**
   - Im Fehlerfall schreibt der Error-Subprocess detaillierte Fehlercodes (`SAP_Error_Code`, `HTTP_Status`) in die MPL-Properties, sodass Administratoren Fehler ohne Payload-Inspektion analysieren können.

## Konsequenzen
- **Positiv:**
  - **Sekundenschnelle Volltextsuche:** Support-Teams filtern in der BTP-Monitoring-Webkonsole direkt nach der `BusinessPartner_ID` oder `MDM_Batch_ID`.
  - **Datenschutzkonform:** Keine Ablage personenbezogener Daten im Klartext-Log; Audit-Trails sind DSGVO-konform.
  - **Lückenlose Nachvollziehbarkeit:** Der gesamte Lebenszyklus eines Geschäftspartners ist vom Ingest bis zum S/4HANA Commit auditierbar.
- **Negativ / Trade-offs:**
  - Minimaler CPU-Overhead für Groovy-Skripte zur MPL-Property-Injektion (im Mikrosekundenbereich vernachlässigbar).
