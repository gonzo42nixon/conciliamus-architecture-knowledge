---
id: data-contracts/s4-odata-mapping
type: Data Contract
title: SAP S/4HANA OData Mapping
description: Vollständige Zuordnungsmatrix zwischen MDM-Feldern und den SAP OData Entitäten A_BusinessPartner und Address.
resource: btp://conciliamus/contracts/s4-odata-mapping
tags: [contract, mapping, odata, s4hana, api-business-partner]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: dependsOn, target: /data-contracts/mdm-inbound-contract.md }
  - { type: implementedBy, target: /iflows/item-processor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# SAP S/4HANA OData Mapping

## Feldzuordnung

| MDM Feld | SAP OData Feld | Datentyp | Beschreibung |
| :--- | :--- | :--- | :--- |
| `externalId` | `SearchTerm1` | String(20) | Primärer Suchbegriff für die Existenzprüfung |
| `company` | `OrganizationBPName1` | String(40) | Firmenname / Name der Organisation |
| `street` | `to_BusinessPartnerAddress[0].StreetName` | String(60) | Straßenbezeichnung |
| `houseNumber` | `to_BusinessPartnerAddress[0].HouseNumber` | String(10) | Hausnummer |
| `postalCode` | `to_BusinessPartnerAddress[0].PostalCode` | String(10) | Postleitzahl |
| `city` | `to_BusinessPartnerAddress[0].CityName` | String(40) | Ort / Stadt |
| `country` | `to_BusinessPartnerAddress[0].Country` | String(2) | ISO 3166-1 alpha-2 Ländercode |
| `email` | `to_BusinessPartnerAddress[0].to_EmailAddress[0].EmailAddress` | String(241) | E-Mail-Adresse |
| `phone` | `to_BusinessPartnerAddress[0].to_PhoneNumber[0].PhoneNumber` | String(30) | Telefonnummer |

## Gesetzte Konstanten
- `BusinessPartnerCategory`: `"2"` (Organisation)
- `BusinessPartnerGrouping`: `"BP02"` (Standard-Nummernkreis)
- `Language`: `"DE"`
- `CorrespondenceLanguage`: `"DE"`
