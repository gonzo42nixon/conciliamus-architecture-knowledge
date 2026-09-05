---
id: decisions/adr-007-two-legged-csrf-handshake
type: Decision Record
title: "ADR-007: Two-Legged CSRF- & Cookie-Handshake"
description: Zweistufiges Kommunikationsmuster zur zuverlässigen Aushandlung und Persistierung von X-CSRF-Tokens und Session-Cookies für schreibende SAP S/4HANA OData V2 Calls.
resource: btp://conciliamus/decisions/ADR-007
tags: [adr, architecture-decision, odata, csrf, two-legged, session-handling, security, s4hana]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T22:45:00Z"
relations:
  - { type: implements, target: /architecture/session-and-csrf-handshake.md }
  - { type: dependsOn, target: /iflows/item-processor-iflow.md }
sources:
  - id: odata-csrf-spec
    resource: https://help.sap.com/docs/SAP_NETWEAVER_750/68bf51330b5d49e7be18413b5a452ef3/178cf2305a414e21a2eb318c2ce1d2f7.html
    title: CSRF Protection in SAP Gateway Foundation
    author: "SAP SE"
---

# ADR-007: Two-Legged CSRF- & Cookie-Handshake

## Status
Akzeptiert (Accepted)

## Kontext
SAP S/4HANA OData V2 und V4 Services erzwingen für alle zustandsverändernden HTTP-Operationen (`POST`, `PATCH`, `PUT`, `DELETE`) einen Schutz gegen Cross-Site Request Forgery (CSRF). Jeder direkte Schreibaufruf ohne gültigen CSRF-Token-Header wird vom SAP Gateway mit `HTTP 403 Forbidden` abgewiesen. Der integrierte Standard-OData-Adapter von SAP Cloud Integration stößt bei dynamischen Routing-Zweigen oder nachgelagerten Subprozessen an Grenzen, wenn Session-Cookies und Token nicht transparent synchronisiert werden.

## Entscheidung
Wir haben entschieden, für alle schreibenden Aufrufe an `API_BUSINESS_PARTNER` ein explizites **Two-Legged Handshake-Verfahren mit Session-Cookie-Preservation** zu etablieren:

1. **Leg 1: Synchroner Token-Fetch:**
   - Vor der eigentlichen Schreiboperation setzt der iFlow einen leichtgewichtigen `GET`-Call auf den Service-Root (`/sap/opu/odata/sap/API_BUSINESS_PARTNER/`) ab.
   - Der Request enthält den obligatorischen Header: `x-csrf-token: fetch`.
2. **Session Preservation (Cookie & Token Handling):**
   - Das Antwort-Headerfeld `x-csrf-token` und alle vom Backend gesetzten `Set-Cookie`-Header (Session-IDs, Application-Context) werden über ein Content-Modifier-Element in flüchtige Exchange Properties gesichert (`${header.x-csrf-token}`, `${header.Set-Cookie}`).
3. **Leg 2: Autorisierte Schreiboperation:**
   - Beim eigentlichen `POST` (Neuanlage) oder `PATCH` (Aktualisierung) werden die gesicherten Werte als Request-Header mitgesendet:
     - `x-csrf-token`: `${property.csrf_token}`
     - `Cookie`: `${property.session_cookie}`
   - Dadurch erkennt das SAP Gateway die Schreiboperation als Fortführung der im ersten Schritt autorisierten Session an.

## Konsequenzen
- **Positiv:**
  - **100% verlässliche Schreibzugriffe:** Keine unvorhersehbaren `HTTP 403 Forbidden` Abbrüche.
  - **Standard-Konformität:** Erfüllt die strengen Sicherheitsanforderungen von SAP NetWeaver und S/4HANA Gateway Foundation.
  - **Session-Sicherheit:** Temporäre Session-Cookies verfallen automatisch nach Abschluss der Transaktion.
- **Negativ / Trade-offs:**
  - Vor jeder Schreibtransaktion ist ein zusätzlicher HTTP-Roundtrip (Token-Fetch) erforderlich. Durch HTTP Keep-Alive und Verbindungspooling beträgt die Latenz wenige Millisekunden.
