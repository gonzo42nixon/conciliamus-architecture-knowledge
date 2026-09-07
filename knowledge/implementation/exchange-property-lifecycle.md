---
id: implementation/exchange-property-lifecycle
type: Implementation Contract
title: "Exchange-Property- und Header-Lebenszyklus im Item Processor"
description: Beobachtete Erzeuger und Verbraucher der für Routing, HTTP-Aufrufe, Mapping und Monitoring relevanten Camel-Werte.
resource: btp://conciliamus/implementation/exchange-property-lifecycle
tags: [camel, exchange-properties, headers, mpl, traceability]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: partOf, target: /implementation/item-processor-observed.md }
  - { type: references, target: /data-contracts/custom-header-properties.md }
---

# Exchange-Property- und Header-Lebenszyklus

| Wert | Erzeuger | Verbraucher |
|---|---|---|
| `batchId`, `BatchId` | Batch-/Item-Validierung | MPL, Fehlerbody |
| `externalId`, `ExternalId` | Item-Validierung | GET-Query, Payload, MPL |
| `company` | Item-Validierung | Payload, MPL |
| `sandboxApiKey` | Content Modifier aus `{{SANDBOX_API_KEY}}` | Payload-Skript |
| Header `APIKey` | Content Modifier | HTTP-GET; nach GET nicht explizit erneut gesetzt |
| `searchResultCount` | GET-Auswertung | Monitoring |
| `operationMode`, `Operation` | Validierung, danach GET-Auswertung | Payload, Router, MPL |
| `bpNumber` | GET-Auswertung | PATCH-Adresse, MPL |
| `targetEndpoint` | GET-Auswertung | Protokollierung im Payload-Skript |
| `isBusinessError` | Validierung oder Duplikaterkennung | Exception-Klassifizierung |
| `SAP_MessageProcessingLogCustomStatus` | Validierungs-/Auswertungsskripte | MPL |

Der API-Key wird als Exchange Property gesichert. Das Modell enthält jedoch keinen expliziten Content Modifier, der ihn nach dem GET aus der Property erneut als HTTP-Header setzt. Ob der Header den Request-Reply-Schritt überlebt, ist aus dem Design-Time-Export allein nicht beweisbar.
