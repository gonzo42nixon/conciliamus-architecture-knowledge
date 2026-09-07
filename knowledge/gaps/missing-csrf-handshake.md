---
id: gaps/missing-csrf-handshake
type: Knowledge and Implementation Gap
title: "Fehlender CSRF- und Session-Handshake im Item Processor"
description: Der akzeptierte ADR-007 ist im analysierten CPI-Export nicht umgesetzt.
resource: btp://conciliamus/gaps/missing-csrf-handshake
tags: [gap, csrf, session, production-readiness]
status: draft
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /conformance/adr-007-csrf-conformance.md }
---

# Fehlender CSRF- und Session-Handshake

Für ein produktives SAP-S/4HANA-OData-Ziel sind Token-Fetch, Cookie-Erhalt und Re-Injektion vor POST/PATCH zu ergänzen und mit einem Integrationslauf zu verifizieren. Der Sandbox-API-Key ist kein Nachweis für diese Produktionsfähigkeit.
