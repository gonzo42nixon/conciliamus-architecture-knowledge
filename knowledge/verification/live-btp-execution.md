---
id: verification/live-btp-execution
type: Test Evidence
title: Live-End-to-End Testlauf auf SAP BTP & Audit-Trail
description: Vollständiger Nachweis der erfolgreichen Live-Durchläufe auf dem SAP BTP Tenant (04.09. & 07.09.2026) mit 11/11 COMPLETED Messages und lückenlosem Foto-Audit-Trail.
resource: btp://conciliamus/evidence/live-run
tags: [evidence, live-test, btp, http-200, verification, audit-trail, completed, 11-messages]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T12:00:00Z"
relations:
  - { type: verifies, target: /architecture/dual-iflow-pattern.md }
  - { type: verifies, target: /iflows/batch-receiver-iflow.md }
  - { type: verifies, target: /iflows/item-processor-iflow.md }
  - { type: verifies, target: /decisions/adr-012-camel-header-preservation.md }
sources:
  - id: audit-trail-photos
    resource: https://photos.app.goo.gl/JR7B5Ds1cfqmkKyUA
    title: Live-Audit-Trail (14 Screenshots) im Google Photos Album
    author: "Dieter Rüffler"
  - id: final-doc
    resource: ORCAI-260907-12H05-FILE-MDE5K
    title: Praxisaufgabe SAP Cloud Integration Dokumentation (v5.0 Final)
    author: "Dieter Rüffler"
  - id: aufgabenstellung
    resource: ORCAI-260905-17H10-FILE-HSWWD
    title: Aufgabenstellung Praxisaufgabe – SAP Cloud Integration
    author: "Conciliamus GmbH"
---

# Live-End-to-End Testlauf auf SAP BTP & Audit-Trail

## Testzeitpunkt & Umgebungen
- **Referenz-Dokumentation (Abgabe):** `ORCAI-260907-12H05-FILE-MDE5K` (5 Seiten, v5.0 Final Release)
- **Aufgabenstellung:** `ORCAI-260905-17H10-FILE-HSWWD`
- **Ausführungsdatum (Erstabnahme):** 04. September 2026, 18:11:00 UTC+2 (HTTP 200 OK)
- **Ausführungsdatum (Finaler Live-Audit-Lauf):** 07. September 2026
- **Tenant:** SAP BTP Cloud Integration Trial / Production Node
- **Endpunkt:** `/http/conciliamus/v1/businesspartners/batch`
- **Status im SAP Message Monitor:** **11 / 11 Messages COMPLETED** (0 Failed)

## Verifizierte End-to-End Metriken
- **1 Batch Ingest Message:** Empfang des 10-teiligen Test-JSONs, Generierung der globalen `SAP_BatchId` und Spaltung via Iterating Splitter.
- **10 Item Processor Messages:** Sequenzielle bzw. parallele Abarbeitung über `ProcessDirect`:
  - **3x PATCH Update (Status: COMPLETED):** Treffer bei OData-Filter (`CUST15`, `BECHTLE AG`, `XYZ-PEPPOL`) -> dynamischer PATCH auf `/A_BusinessPartner('{id}')`.
  - **7x POST Deep-Insert (Status: COMPLETED):** Null Treffer bei OData-Filter (`JSD-BP-100001` bis `100007`) -> Deep-Insert POST auf `/A_BusinessPartner`.
- **Camel Exchange Property Preservation:** Beseitigung des HTTP 401-Verlustes durch Property-Sicherung gemäss ADR-012.
- **DLQ-Resilienz:** Bei simuliertem Netzausfall Weiterleitung in den Data Store `DLQ_BusinessPartner_TechnicalErrors` gemäss ADR-008.

## Foto-Beweiskette & Live-Audit-Trail
Die lückenlose Nachweisführung aller 14 Einzelschritte (inkl. Message Processing Log, Content Modifier Inspektion, Trace-Ansicht und HTTP-Status-Rückmeldungen) ist im offiziellen Audit-Album hinterlegt:
- **Google Photos Live-Audit-Trail:** [14 Beleg-Screenshots ansehen](https://photos.app.goo.gl/JR7B5Ds1cfqmkKyUA)
- **Interaktive Präsentation:** [Pecha Kucha 20x20 Web App](https://orcai-54321.web.app/pecha-kucha.html)
