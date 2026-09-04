---
id: verification/live-btp-execution
type: Test Evidence
title: Live-End-to-End Testlauf auf SAP BTP
description: Vollständiger Nachweis des erfolgreichen Live-Durchlaufs auf dem SAP BTP Tenant am 04.09.2026 mit HTTP 200 OK.
resource: btp://conciliamus/evidence/live-run
tags: [evidence, live-test, btp, http-200, verification]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: verifies, target: /architecture/dual-iflow-pattern.md }
  - { type: verifies, target: /iflows/batch-receiver-iflow.md }
  - { type: verifies, target: /iflows/item-processor-iflow.md }
sources:
  - id: test-evidences
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_evidences.md
    title: Prüfungs- & Testnachweise
    author: "Dieter Rüffler"
---

# Live-End-to-End Testlauf auf SAP BTP

## Testzeitpunkt & Umgebung
- **Ausführungsdatum:** 04. September 2026, 18:11:00 UTC+2
- **Tenant:** `b9c123f3trial` (Region: `US East - AWS`)
- **Endpunkt:** `/http/conciliamus/v1/businesspartners/batch`
- **Authentifizierung:** OAuth 2.0 Client Credentials Grant (`it-rt`, `ESBMessaging.send`)
- **Ergebnis:** **HTTP 200 OK** (Gesamtlaufzeit: 1.82s)

## Ausführungsprotokoll
```text
=== LIVE-INTEGRATIONSTEST: BTP CLOUD INTEGRATION ===
[*] Fordere OAuth2-Token an von: https://b9c123f3trial.authentication.us10.hana.ondemand.com/oauth/token
[+] OAuth2-Token erfolgreich erhalten! (Typ: bearer, Gültig: 3599s, Scope: ESBMessaging.send)
[*] Führe CSRF-Handshake durch an: https://b9c123f3trial.it-cpitrial06-rt.cfapps.us10-001.hana.ondemand.com/http/conciliamus/v1/businesspartners/batch
[+] CSRF-Token erhalten: 3al-SeNapJWa2iq_k9qzw0XMI4yTLQRM
[*] Lade Testdaten aus: testdata/Testdaten_prepared.json
[*] Sende Batch an SAP Cloud Integration:
    -> Endpunkt: /http/conciliamus/v1/businesspartners/batch
[+++] TEST ERFOLGREICH! HTTP Status: 200 OK
```

## Verifizierte Metriken
- 10 Business Partner im Batch empfangen
- 3x PATCH Update (`CUST15`, `BECHTLE AG`, `XYZ-PEPPOL`) erfolgreich geroutet
- 7x POST Neuanlage (`JSD-BP-100001` bis `100007`) erfolgreich vorbereitet
- Volltextsuche im BTP Web-Monitor verifiziert
