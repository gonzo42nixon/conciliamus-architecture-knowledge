---
id: data-contracts/mdm-inbound-contract
type: Data Contract
title: MDM Inbound JSON Kontrakt
description: Schnittstellenspezifikation und Validierungsregeln für die vom Quellsystem JSD-MDM übermittelten JSON-Sammelbatches.
resource: btp://conciliamus/contracts/mdm-inbound
tags: [contract, mdm, json, schema, validation]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implements, target: /iflows/batch-receiver-iflow.md }
  - { type: routesTo, target: /data-contracts/s4-odata-mapping.md }
sources:
  - id: mdm-schema
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/testdata/Testdaten.json
    title: Original-Testdaten JSD-MDM
---

# MDM Inbound JSON Kontrakt

## JSON-Struktur
```json
{
  "batchId": "BP-20260714-001",
  "createdAt": "2026-07-14T09:00:00Z",
  "sourceSystem": "JSD-MDM",
  "businessPartners": [
    {
      "externalId": "CUST15",
      "company": "Musterfirma Berlin GmbH",
      "street": "Musterstraße",
      "houseNumber": "10",
      "postalCode": "10115",
      "city": "Berlin",
      "country": "DE",
      "email": "kontakt@musterfirma-berlin.de",
      "phone": "+49 30 10000001",
      "vatId": "DE100000001"
    }
  ]
}
```

## Validierungsregeln
1. **`batchId`:** Pflichtfeld, Muster `BP-YYYYMMDD-NNN`.
2. **`businessPartners`:** Pflicht-Array, mindestens 1 Element.
3. **`externalId`:** Nicht-leerer String, max. 20 Zeichen (wird auf `SearchTerm1` gemappt).
4. **`company`:** Nicht-leerer String, max. 40 Zeichen (wird auf `OrganizationBPName1` gemappt).
5. **`country`:** Exakt 2 Großbuchstaben (ISO 3166-1 alpha-2, z.B. `DE`).
6. **`email`:** Valide E-Mail-Syntax (Regex `^[^@]+@[^@]+\.[^@]+$`).
