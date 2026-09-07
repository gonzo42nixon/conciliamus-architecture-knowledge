---
id: decisions/adr-012-camel-header-preservation
type: Decision Record
title: "ADR-012: Camel Exchange Property Preservation bei Request-Reply & Zero-Hardcoding"
description: Persistierung flüchtiger Authentifizierungs-Header in Camel Exchange Properties zur Vermeidung von HTTP 401-Verlusten über Request-Reply-Grenzen hinweg sowie striktes Zero-Hardcoding via parameters.prop.
resource: btp://conciliamus/decisions/ADR-012
tags: [adr, architecture-decision, camel, request-reply, headers, exchange-properties, zero-hardcoding, parameters-prop, security, http-401]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T10:00:00Z"
relations:
  - { type: implements, target: /architecture/dual-iflow-pattern.md }
  - { type: dependsOn, target: /iflows/item-processor-iflow.md }
  - { type: relatesTo, target: /decisions/adr-002-zero-trust-btp-security.md }
  - { type: relatesTo, target: /decisions/adr-007-two-legged-csrf-handshake.md }
sources:
  - id: camel-exchange-spec
    resource: https://camel.apache.org/manual/exchange.html
    title: Apache Camel Exchange and Message Lifecycle
    author: "Apache Software Foundation"
  - id: cpi-external-params
    resource: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/externalizing-parameters
    title: Externalizing Parameters in SAP Cloud Integration
    author: "SAP SE"
---

# ADR-012: Camel Exchange Property Preservation bei Request-Reply & Zero-Hardcoding

## Status
Akzeptiert (Accepted)

## Kontext
In der SAP Cloud Integration (basierend auf Apache Camel) löst ein `Request-Reply`-Schritt – beispielsweise die synchrone OData-Existenzprüfung (`GET /A_BusinessPartner?$filter=...`) oder der Two-Legged CSRF-Handshake (ADR-007) – einen Austausch des aktiven Nachrichtenobjekts aus. 

Werden Authentifizierungsmerkmale (wie der SAP API Business Hub `APIKey` oder Authorization-Header) ausschließlich im flüchtigen Camel-Header-Objekt geführt, gehen sie verloren: Die Antwort des Backends (z.B. `SAP NetWeaver Application Server 7.53 / EJS/100`) überschreibt die Request-Header mit den Response-Headern des Servers. 

Wird unmittelbar im Anschluss ein zweiter HTTP-/OData-Call (z.B. die Existenzprüfung oder Neuanlage) abgesetzt, schlägt dieser fehl mit:
```text
org.apache.camel.component.ahc.AhcOperationFailedException: 
HTTP operation failed invoking https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner?$filter=SearchTerm1%20eq%20'JSD-BP-100007' with statusCode: 401
```

Zusätzlich erfordert die Enterprise-Architektur-Governance der Conciliamus GmbH ein striktes **Zero-Hardcoding**: Keine API-Keys, Endpunkte oder Mandanten dürfen in Groovy-Skripten oder statischen XML-Konfigurationen fest codiert sein.

## Entscheidung
Wir haben entschieden, ein zweistufiges Muster zur Zustandserhaltung und Parameter-Externalisierung verbindlich einzusetzen:

1. **Camel Exchange Property Preservation:**
   - Camel Exchange Properties überdauern den gesamten Lebenszyklus des Message Exchanges und werden durch `Request-Reply`-Aufrufe an Drittsysteme **nicht** überschrieben oder geleert.
   - Beim Eintritt in den `IFL_MDM_BP_Item_Processor` sichert ein initialer Content Modifier alle geschäftskritischen Authentifizierungs- und Korrelationsdaten in Exchange Properties:
     - `property.sandboxApiKey` := `{{SANDBOX_API_KEY}}`
     - `property.targetHost` := `{{S4HANA_HOST}}`
     - `property.batchId` := `${header.SAP_BatchId}`
     - `property.externalId` := `${xpath(//ExternalId/text())}`
   - Vor jedem nachgelagerten HTTP- oder OData-Request-Reply re-injiziert ein nachfolgender Content Modifier die erforderlichen Header aus den gesicherten Properties:
     - `Header: APIKey` := `${property.sandboxApiKey}`
     - `Header: Accept` := `application/json`

2. **Strikte Externalisierung via `parameters.prop`:**
   - Sämtliche schlüssel- und umgebungsrelevanten Variablen werden in der Datei `src/main/resources/parameters.prop` deklariert:
     ```properties
     SANDBOX_API_KEY={{SANDBOX_API_KEY}}
     S4HANA_HOST={{S4HANA_HOST}}
     DATASTORE_DLQ_NAME=DLQ_BusinessPartner_TechnicalErrors
     ```
   - Beim Deployment auf dem SAP BTP Tenant bindet die Integration Suite die Werte direkt an die Konfigurationsmaske des iFlows oder bezieht sie aus dem BTP Credential Store (Secure Store).

## Konsequenzen
- **Positiv:**
  - **Zero 401 Unauthorized:** Authentifizierungs-Header bleiben über beliebig viele verkettete Request-Reply-Schritte (Existenzprüfung -> CSRF-Fetch -> Deep-Insert) stabil und unversehrt.
  - **Enterprise Compliance:** Keine Geheimnisse im Quellcode; vollständige Audit-Konformität bei Code-Reviews.
  - **Mandanten- & Stufenunabhängigkeit:** Derselbe iFlow-Code wird ohne Modifikation in DEV, QA und PROD über Tenant-spezifische Parameter betrieben.
- **Negativ / Trade-offs:**
  - Zusätzliche Content Modifier Elemente in den iFlow-Pipelines vor und nach externen Service-Aufrufen.
  - Erhöhter Disziplinierungsbedarf bei der iFlow-Modellierung (Dokumentation in BPMN-Modellen erforderlich).
