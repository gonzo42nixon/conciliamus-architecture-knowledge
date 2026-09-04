---
id: architecture/session-and-csrf-handshake
type: Architecture Concept
title: Session & CSRF Handshake
description: Handhabung von CSRF-Tokens und Session-Cookies bei schreibenden OData-Aufrufen auf SAP S/4HANA.
resource: btp://conciliamus/architecture/csrf-handshake
tags: [architecture, csrf, security, odata, cookies, s4hana, http]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: contains, target: /iflows/item-processor-iflow.md }
  - { type: dependsOn, target: /architecture/existence-check-and-routing.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# Session & CSRF Handshake

## Sicherheitsmechanismus in SAP OData
SAP S/4HANA schützt alle mutierenden HTTP-Methoden (`POST`, `PUT`, `PATCH`, `DELETE`) gegen Cross-Site Request Forgery (CSRF). Ein direkter schreibender Call ohne Token wird mit `HTTP 403 Forbidden` abgewiesen.

## Two-Legged Handshake Ablauf
1. **Pre-Flight Fetch:**
   - Ein vorangehender `GET`- oder `HEAD`-Request wird mit dem Header `X-CSRF-Token: Fetch` an das Zielsystem gesendet.
   - Der S/4HANA-Server antwortet mit:
     - `X-CSRF-Token: <token-string>`
     - `Set-Cookie: SAP_SESSIONID_...; MYSAPSSO2=...`
2. **Session Cookie Propagation:**
   - In SAP Cloud Integration wird der HTTP-Empfängeradapter so konfiguriert oder über Scripting gesteuert, dass sowohl das Token (`X-CSRF-Token`) als auch die Session-Cookies im darauffolgenden `POST`/`PATCH` mitgeführt werden.
   - Dadurch ordnet S/4HANA den Schreibzugriff derselben authentifizierten Benutzersitzung zu.
