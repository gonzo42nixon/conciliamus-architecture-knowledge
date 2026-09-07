---
id: conformance/adr-012-property-conformance
type: Architecture Conformance Assessment
title: "Konformitätsprüfung: Item Processor gegen ADR-012"
description: Vergleich der exportierten Externalisierung und Headerbehandlung mit ADR-012.
resource: btp://conciliamus/conformance/ADR-012
tags: [conformance, adr-012, camel, headers, externalization]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /decisions/adr-012-camel-header-preservation.md }
  - { type: dependsOn, target: /implementation/exchange-property-lifecycle.md }
  - { type: handlesError, target: /gaps/incomplete-header-restoration.md }
---

# Konformitätsprüfung gegen ADR-012

## Ergebnis: teilweise konform

Konform umgesetzt sind:

- `SANDBOX_API_KEY` und `S4HANA_BASE_URL` sind externalisierte Parameter;
- der API-Key wird zusätzlich in `property.sandboxApiKey` gesichert;
- Geschäfts- und Korrelationswerte werden als Exchange Properties geführt.

Abweichungen:

- ADR-012 nennt `S4HANA_HOST` und einen DLQ-Namen; exportiert sind nur `S4HANA_BASE_URL` und `SANDBOX_API_KEY`.
- Das Modell re-injiziert `property.sandboxApiKey` nach dem GET nicht explizit in den Header `APIKey`.
- CSRF-Token und Session-Cookie sind weder als Properties noch als Header modelliert.

Damit ist Zero-Hardcoding für Basis-URL und Sandbox-Key umgesetzt; die vollständige Header-Preservation über mehrere Request-Reply-Schritte ist nicht nachgewiesen.
