---
id: decisions/adr-006-idempotent-existence-check
type: Decision Record
title: "ADR-006: Idempotente Existenzprüfung & Router-Matrix"
description: Absicherung der Schnittstelle gegen Duplikate und Fehlversuche durch vorgeschalteten OData GET Existenzcheck und deterministische 3-Wege-Routing-Matrix (POST vs. PATCH).
resource: btp://conciliamus/decisions/ADR-006
tags: [adr, architecture-decision, idempotency, odata, existenzpruefung, router, business-partner, sap-s4hana]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T22:45:00Z"
relations:
  - { type: implements, target: /architecture/existence-check-and-routing.md }
  - { type: dependsOn, target: /data-contracts/s4-odata-mapping.md }
sources:
  - id: s4-bp-api
    resource: https://api.sap.com/api/API_BUSINESS_PARTNER/overview
    title: SAP S/4HANA Business Partner (A_BusinessPartner) OData API
    author: "SAP SE"
---

# ADR-006: Idempotente Existenzprüfung & Router-Matrix

## Status
Akzeptiert (Accepted)

## Kontext
In der Enterprise-Integration können Netzwerkabbrüche, temporäre Server-Timeouts oder wiederholte Quellsystem-Pushes dazu führen, dass derselbe Geschäftspartner-Batch mehrfach übertragen wird. Ein naiver Integrationsansatz, der jeden eingehenden Datensatz bedingungslos per `HTTP POST` an die S/4HANA OData API sendet, erzeugt gravierende Dateninkonsistenzen: Entweder entstehen identische Dubletten mit abweichenden internen Partnernummern oder die API bricht mit Primärschlüssel-Konflikten ab.

## Entscheidung
Wir haben entschieden, im `IFL_MDM_BP_Item_Processor` eine **vorgelagerte, semantische Existenzprüfung mit deterministischer 3-Wege-Router-Matrix** zu implementieren:

1. **Semantischer OData GET-Check:**
   - Vor jeder schreibenden Operation führt der iFlow einen OData GET-Call gegen das EntitySet `A_BusinessPartner` aus:
     `$filter=SearchTerm1 eq '${property.ExternalId}'`
   - Die externe Mandanten-ID (`externalId` aus dem MDM-JSON) wird als semantischer Suchbegriff (`SearchTerm1`) im SAP-Stammsatz geführt.
2. **Deterministische 3-Wege-Entscheidungsmatrix:**
   - **Pfad 1 (0 Treffer - Neuanlage):** Der Partner existiert noch nicht im ERP. Es erfolgt ein **HTTP POST** (`/A_BusinessPartner`) via Deep Insert inklusive Adress- und Rollenstrukturen.
   - **Pfad 2 (1 Treffer - Aktualisierung):** Der Partner existiert bereits. Seine interne S/4-Nummer (`BusinessPartner`) wird dynamisch extrahiert und für einen **HTTP PATCH** (`/A_BusinessPartner('{BusinessPartner}')`) verwendet.
   - **Pfad 3 (>1 Treffer - Stammdatenkonflikt):** Es existieren bereits mehrere Partner mit demselben Suchbegriff. Der Datensatz wird nicht überschrieben, sondern als fachlicher Fehler isoliert und im MPL als Dubletten-Alert markiert.

## Konsequenzen
- **Positiv:**
  - **Vollständige Idempotenz:** Derselbe Batch kann beliebig oft eingespielt werden, ohne das ERP-System zu korrumpieren.
  - **Dynamische Update-Fähigkeit:** Automatische Umschaltung zwischen Neuanlage und Stammdatenpflege ohne manuelle Steuerung durch das Quellsystem.
  - **Dublettenschutz:** Zuverlässiges Verhindern von Dubletten im S/4HANA Business Partner Pool.
- **Negativ / Trade-offs:**
  - Verdoppelung der HTTP-Aufrufe gegen S/4HANA (zuerst GET, dann POST/PATCH). Durch subsekundäre OData GET-Latenzen im LAN/VPC jedoch vernachlässigbar.
