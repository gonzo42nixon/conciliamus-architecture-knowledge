---
id: conformance/adr-008-dlq-conformance
type: Architecture Conformance Assessment
title: "Konformitätsprüfung: Item Processor gegen ADR-008"
description: Vergleich des exportierten Error Subprocess mit der beschlossenen persistenten Data-Store-DLQ.
resource: btp://conciliamus/conformance/ADR-008
tags: [conformance, adr-008, dlq, data-store, gap]
status: verified
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /decisions/adr-008-data-store-dlq.md }
  - { type: dependsOn, target: /implementation/item-processor-observed.md }
  - { type: handlesError, target: /gaps/missing-dlq-persistence.md }
---

# Konformitätsprüfung gegen ADR-008

## Ergebnis: teilweise konform

Implementiert sind:

- Unterscheidung zwischen fachlichen und technischen Fehlern;
- MPL-Status `FAILED_BUSINESS` beziehungsweise `FAILED_TECHNICAL`;
- strukturierter JSON-Fehlerbody;
- technische Fehlerbeschreibung für einen späteren Wiederanlauf.

Nicht implementiert ist die in ADR-008 geforderte Persistenz. Der Error Subprocess enthält nur `HandleExceptionAndDLQ.groovy` und ein End Event, aber keinen Data-Store-Write-Schritt. Das Skript bereitet einen DLQ-fähigen Body vor, speichert ihn jedoch nicht in `BP_FAILED_QUEUE`.
