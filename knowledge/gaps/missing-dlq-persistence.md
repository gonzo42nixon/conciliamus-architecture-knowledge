---
id: gaps/missing-dlq-persistence
type: Knowledge and Implementation Gap
title: "Fehlende Data-Store-Persistenz im Error Subprocess"
description: Der exportierte Item Processor klassifiziert technische Fehler, persistiert sie aber nicht in der von ADR-008 vorgesehenen DLQ.
resource: btp://conciliamus/gaps/missing-dlq-persistence
tags: [gap, dlq, data-store, replay, resilience]
status: draft
generated:
  by: "codex:artifact-analysis"
  at: "2026-09-07T19:30:00+02:00"
relations:
  - { type: references, target: /conformance/adr-008-dlq-conformance.md }
---

# Fehlende Data-Store-Persistenz

Erforderlich sind mindestens ein Data-Store-Write-Schritt, ein deterministischer Entry Key, ein versionierter DLQ-Datenvertrag und ein nachgewiesener Replay-Pfad. Erst danach darf der Implementierungsstatus von ADR-008 als vollständig konform gelten.
