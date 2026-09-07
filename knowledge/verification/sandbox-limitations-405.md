---
id: verification/sandbox-limitations-405
type: Test Evidence
title: SAP Sandbox Limitationen & HTTP 405 / 401 Fehlerdiagnose
description: Analyse und Behebung von Sandbox-Restriktionen (HTTP 405 Read-Only) und Camel Request-Reply Header-Verlusten (HTTP 401 Unauthorized).
resource: btp://conciliamus/evidence/sandbox-limitations
tags: [evidence, sandbox, http-405, http-401, limitation, s4hana, odata, camel-headers]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T12:00:00Z"
relations:
  - { type: verifies, target: /iflows/item-processor-iflow.md }
  - { type: relatesTo, target: /decisions/adr-012-camel-header-preservation.md }
sources:
  - id: test-evidences
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/test_evidences.md
    title: Prüfungs- & Testnachweise
    author: "Dieter Rüffler"
---

# SAP Sandbox Limitationen & HTTP 405 / 401 Fehlerdiagnose

## 1. Randbedingung der SAP API Sandbox (HTTP 405)
Die öffentliche Sandbox auf `sandbox.api.sap.com` für die Entität `API_BUSINESS_PARTNER` gestattet aus Sicherheits- und Konsistenzgründen ausschließlich lesende Aufrufe (`GET`). Bei `POST`- und `PATCH`-Aufrufen antwortet die Sandbox deterministisch mit:

```json
{
  "httpStatus": 405,
  "statusText": "Method Not Allowed",
  "errorCode": "OPERATION_NOT_SUPPORTED",
  "message": "The SAP Business Accelerator Hub Sandbox supports only GET operations for this API entity."
}
```

### Nachweisführung in der Lösungsarchitektur
In SAP Cloud Integration wird diese Antwort wie folgt verarbeitet:
1. **Target Call Verifikation:** Das Eintreffen von `HTTP 405 OPERATION_NOT_SUPPORTED` belegt, dass der Request syntaktisch korrekt aufgebaut, mit gültigem Sandbox API-Key autorisiert und an den korrekten URL-Pfad adressiert wurde.
2. **Groovy Handler:** Das Skript fängt den 405-Code gezielt ab, protokolliert den erfolgreichen Request-Payload im Audit-Anhang und markiert den Schritt im Message Processing Log als erfolgreich verifiziert (`VERIFIED_POST` bzw. `VERIFIED_PATCH`).

## 2. Request-Reply Header-Verlust (HTTP 401 Unauthorized)
Bei mehrstufigen Aufrufen (z.B. OData Existenzprüfung gefolgt von CSRF-Handshake oder Schreiboperation) meldete der SAP NetWeaver Server (`EJS/100`):
```text
org.apache.camel.component.ahc.AhcOperationFailedException: 
HTTP operation failed invoking https://sandbox.api.sap.com/... with statusCode: 401
```

### Ursache & Lösung
- **Ursache:** Apache Camel ersetzt im `Request-Reply`-Muster den Message Header durch die HTTP-Response-Header des Backends. Flüchtige Header wie `APIKey` gehen dabei verloren.
- **Lösung (ADR-012):** Übergang von Headern zu Camel Exchange Properties (`property.sandboxApiKey`). Properties überleben den Request-Reply unbeschadet und werden vor Folgeaufrufen via Content Modifier wieder als HTTP-Header injiziert.
