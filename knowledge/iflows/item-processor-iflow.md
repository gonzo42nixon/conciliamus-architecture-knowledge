---
id: iflows/item-processor-iflow
type: iFlow Specification
title: "IFL_MDM_BP_Item_Processor: Atomare Partner-Verarbeitung"
description: Spezifikation des verarbeitenden iFlows für Validierung, OData GET Existenzprüfung, deterministisches Routing und S/4HANA OData Aufrufe.
resource: btp://conciliamus/iflows/IFL_MDM_BP_Item_Processor
tags: [iflow, item-processor, cpi, btp, odata, routing, s4hana, error-handling]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: partOf, target: /architecture/dual-iflow-pattern.md }
  - { type: routedFrom, target: /iflows/batch-receiver-iflow.md }
  - { type: implements, target: /architecture/existence-check-and-routing.md }
  - { type: implements, target: /architecture/resilience-and-dead-letter.md }
  - { type: implements, target: /decisions/adr-004-bpmn-method-and-style.md }
  - { type: verifies, target: /verification/live-btp-execution.md }
sources:
  - id: btp-doku
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/btp_setup_doku.md
    title: BTP Testaccount & Integration Suite Einrichtung
    author: "Dieter Rüffler"
---

# IFL_MDM_BP_Item_Processor

## Technische Kenndaten
- **Paket:** `Conciliamus - Business Partner Integration`
- **Technischer Name:** `IFL_MDM_BP_Item_Processor`
- **Inbound-Adapter:** ProcessDirect (`/conciliamus/v1/businesspartners/item`)
- **Outbound-Adapter:** HTTP (OData REST an `sandbox.api.sap.com`)
- **Security Material:** `SANDBOX_API_KEY` (Secure Parameter)
- **Status im Tenant:** `Deployed` / `Started`

## Modellierungs-Schritte (Method & Style)
1. **Start-Event:** `Einzelsatz empfangen`
2. **Task 1:** `Felder fachlich validieren` (Groovy Script `ValidateItem.groovy`: Prüft `externalId`, `company`, E-Mail-Regex, Ländercode).
3. **Task 2:** `Header Properties registrieren` (MPL Custom Status & Volltext-Header).
4. **Task 3:** `Existenz prüfen (GET)` (HTTP Request-Reply an `/A_BusinessPartner?$filter=SearchTerm1 eq ...`).
5. **Task 4:** `Suchergebnis analysieren` (Groovy Script `EvaluateSearchResult.groovy`: Ermittelt Trefferanzahl).
6. **Entscheidungs-Gateway (Unbeschrifteter Rhombus):**
   - **Pfad 1 (0 Treffer):** Task `POST Payload aufbauen` ➔ Task `Neuanlage ausführen (POST)` ➔ `/A_BusinessPartner`
   - **Pfad 2 (1 Treffer):** Task `PATCH Payload aufbauen & ID zuweisen` ➔ Task `Delta aktualisieren (PATCH)` ➔ `/A_BusinessPartner('{id}')`
   - **Pfad 3 (Default, >1 Treffer):** Task `Fachlichen Fehler protokollieren`
7. **Exception Subprocess:**
   - Fängt technische HTTP-Ausfälle ab und schreibt in Data Store `BP_FAILED_QUEUE`.
   - Schreibt Audit Log für fachliche Fehler.
8. **End-Event:** `Verarbeitung beendet`
