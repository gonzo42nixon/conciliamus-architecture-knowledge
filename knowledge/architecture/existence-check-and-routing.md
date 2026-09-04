---
id: architecture/existence-check-and-routing
type: Architecture Concept
title: Existenzprüfung & Deterministische Router-Matrix
description: Idempotente Existenzprüfung via OData GET und deterministische Verzweigung zu POST, PATCH oder Fehlerbehandlung.
resource: btp://conciliamus/architecture/existence-routing
tags: [architecture, odata, routing, idempotency, s4hana, content-based-router]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: contains, target: /iflows/item-processor-iflow.md }
  - { type: implements, target: /data-contracts/s4-odata-mapping.md }
  - { type: verifies, target: /verification/istqb-test-strategy.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Existenzprüfung & Deterministische Router-Matrix

## Idempotenz-Konzept
Um Mehrfachanlagen von Geschäftspartnern zu verhindern (z.B. bei wiederholtem Senden desselben Batches), fragt der Prozess vor jeder schreibenden Aktion das Zielsystem ab:

```http
GET /s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner?$filter=SearchTerm1 eq '${property.externalId}'&$select=BusinessPartner,SearchTerm1,OrganizationBPName1 HTTP/1.1
Host: sandbox.api.sap.com
Accept: application/json
APIKey: {{SANDBOX_API_KEY}}
```

## Entscheidungsmatrix

| Trefferanzahl | Ziel-Operation | Ziel-Pfad | Bedeutung / Verhalten |
| :--- | :--- | :--- | :--- |
| **`0` Treffer** | **POST** | `/A_BusinessPartner` | Neuanlage (Deep Insert mit Adresse & Kommunikation) |
| **`1` Treffer** | **PATCH** | `/A_BusinessPartner('{id}')` | Aktualisierung: Interne ID wird dynamisch in URI eingesetzt |
| **`>1` Treffer** | **Fachlicher Fehler** | *(Abbruch Einzelsatz)* | Duplikat im SAP-System (`FAILED_BUSINESS`) |

## Dynamische URI-Adressierung bei PATCH
Wird genau ein Treffer gefunden, liest ein Groovy-Skript die SAP-Geschäftspartnernummer aus der Antwort aus:
```groovy
def bpNumber = jsonResponse.d.results[0].BusinessPartner
message.setProperty("bpNumber", bpNumber)
message.setHeader("CamelHttpPath", "/A_BusinessPartner('" + bpNumber + "')")
```
Es existiert **keine statische ID-Hinterlegung** im Flow.
