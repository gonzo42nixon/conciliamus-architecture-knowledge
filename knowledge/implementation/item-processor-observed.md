---
id: implementation/item-processor-observed
type: Observed Implementation
title: "Beobachtete Implementierung des IFL_MDM_BP_Item_Processor"
description: Aus dem CPI-Export extrahierter Ist-Ablauf des atomaren Business-Partner-Prozessors einschließlich Skripten, Router und HTTP-Adaptern.
resource: btp://conciliamus/implementation/IFL_MDM_BP_Item_Processor
tags: [implemented, iflow, item-processor, odata, post, patch, routing]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: implements, target: /iflows/item-processor-iflow.md }
  - { type: dependsOn, target: /artifacts/item-processor-export.md }
  - { type: dependsOn, target: /implementation/exchange-property-lifecycle.md }
  - { type: references, target: /conformance/adr-007-csrf-conformance.md }
  - { type: references, target: /conformance/adr-008-dlq-conformance.md }
  - { type: references, target: /conformance/adr-012-property-conformance.md }
---

# Beobachtete Implementierung des Item Processors

## Ausführungsfolge

1. ProcessDirect empfängt einen Datensatz auf `/conciliamus/v1/businesspartners/item`.
2. `ValidateBusinessPartnerItem.groovy` normalisiert und validiert den Datensatz.
3. Ein Content Modifier setzt `sandboxApiKey`, `APIKey` und `Accept`.
4. Ein HTTP-GET sucht über `SearchTerm1 eq '${property.externalId}'` nach vorhandenen Partnern.
5. `EvaluateODataExistenceResponse.groovy` setzt bei null Treffern `POST`, bei einem Treffer `PATCH` und wirft bei mehreren Treffern einen fachlichen Fehler.
6. `BuildS4HanaPayload.groovy` erzeugt den POST- oder PATCH-Payload.
7. Das Gateway verwendet POST als Default-Pfad. Der PATCH-Pfad greift bei `operationMode = 'PATCH'`, `Operation = 'PATCH'` oder einem `operationMode`, der `PATCH` enthält.
8. Ein Error Subprocess klassifiziert Ausnahmen und erzeugt einen Fehlerbody.

## HTTP-Konfiguration

| Operation | Ziel | Body | Timeout | Adapter-Retry |
|---|---|---:|---:|---:|
| GET | `{{S4HANA_BASE_URL}}/A_BusinessPartner?$filter=SearchTerm1 eq '${property.externalId}'` | nein | 60 s | nein |
| POST | `{{S4HANA_BASE_URL}}/A_BusinessPartner` | ja | 60 s | nein |
| PATCH | `{{S4HANA_BASE_URL}}/A_BusinessPartner('${property.bpNumber}')` | ja | 60 s | nein |

Alle drei Adapter verwenden `authenticationMethod=None`, `throwExceptionOnFailure=true` sowie uneingeschränkte Request- und Response-Header (`*`). Der exportierte Standardwert von `S4HANA_BASE_URL` verweist auf `sandbox.api.sap.com`.

## Payload-Semantik

- POST erzeugt einen Deep Insert mit Organisation, Adresse, E-Mail und Telefon.
- PATCH aktualisiert ausschließlich `SearchTerm1`, `OrganizationBPName1`, `Language` und `CorrespondenceLanguage`.
- `vatId` wird validierungsnah als Property gespeichert, aber weder im POST- noch im PATCH-Payload verwendet.

## Beobachtete Besonderheit

Die Validierung setzt zunächst anhand der festen IDs `CUST15`, `BECHTLE AG`, `BECHTLE-AG` und `XYZ-PEPPOL` eine erwartete Operation. Die GET-Auswertung überschreibt diese später anhand des tatsächlichen Suchergebnisses. Für Routing ist die spätere Entscheidung maßgeblich; frühe Monitoringdaten können bei einem Fehler vor der GET-Auswertung dennoch irreführend sein.
