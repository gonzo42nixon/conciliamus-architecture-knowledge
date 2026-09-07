---
id: conformance/adr-007-csrf-conformance
type: Architecture Conformance Assessment
title: "Konformitätsprüfung: Item Processor gegen ADR-007"
description: Vergleich des exportierten Item Processors mit dem beschlossenen Two-Legged-CSRF- und Cookie-Handshake.
resource: btp://conciliamus/conformance/ADR-007
tags: [conformance, adr-007, csrf, cookie, gap]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /decisions/adr-007-two-legged-csrf-handshake.md }
  - { type: dependsOn, target: /implementation/item-processor-observed.md }
  - { type: handlesError, target: /gaps/missing-csrf-handshake.md }
---

# Konformitätsprüfung gegen ADR-007

## Ergebnis: nicht konform

Im Export fehlen sämtliche für ADR-007 verbindlichen Elemente:

- kein Request mit `X-CSRF-Token: Fetch`;
- keine Token-Extraktion;
- keine Sicherung von `Set-Cookie`;
- keine Re-Injektion von Token und Cookie vor POST oder PATCH;
- `httpSessionHandling=None`.

Die vorhandene API-Key-Authentisierung gegen die SAP-Sandbox ersetzt keinen produktiven CSRF-Handshake. ADR-007 bleibt eine akzeptierte Zielentscheidung, ist in diesem Export aber nicht implementiert.
