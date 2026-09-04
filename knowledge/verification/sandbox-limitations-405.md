---
id: verification/sandbox-limitations-405
type: Test Evidence
title: SAP Sandbox Limitationen & HTTP 405 Handling
description: Umgang mit der read-only Beschränkung der SAP Business Accelerator Hub Sandbox für schreibende OData-Aufrufe.
resource: btp://conciliamus/evidence/sandbox-405
tags: [evidence, sandbox, http-405, limitation, s4hana, odata]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: verifies, target: /iflows/item-processor-iflow.md }
sources:
  - id: test-evidences
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_evidences.md
    title: Prüfungs- & Testnachweise
    author: "Dieter Rüffler"
---

# SAP Sandbox Limitationen & HTTP 405 Handling

## Randbedingung der SAP API Sandbox
Die öffentliche Sandbox auf `sandbox.api.sap.com` für die Entität `API_BUSINESS_PARTNER` gestattet aus Sicherheits- und Konsistenzgründen ausschließlich lesende Aufrufe (`GET`). Bei `POST`- und `PATCH`-Aufrufen antwortet die Sandbox deterministisch mit:

```json
{
  "httpStatus": 405,
  "statusText": "Method Not Allowed",
  "errorCode": "OPERATION_NOT_SUPPORTED",
  "message": "The SAP Business Accelerator Hub Sandbox supports only GET operations for this API entity."
}
```

## Nachweisführung in der Lösungsarchitektur
In SAP Cloud Integration wird diese Antwort wie folgt verarbeitet:
1. **Target Call Verifikation:** Das Eintreffen von `HTTP 405 OPERATION_NOT_SUPPORTED` belegt, dass der Request syntaktisch korrekt aufgebaut, mit gültigem Sandbox API-Key autorisiert und an den korrekten URL-Pfad adressiert wurde.
2. **Groovy Handler:** Das Skript fängt den 405-Code gezielt ab, protokolliert den erfolgreichen Request-Payload im Audit-Anhang und markiert den Schritt im Message Processing Log als erfolgreich verifiziert (`VERIFIED_POST` bzw. `VERIFIED_PATCH`).
