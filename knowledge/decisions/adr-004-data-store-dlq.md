---
id: decisions/adr-004-data-store-dlq
type: Decision Record
title: "ADR-004: Data Store für Dead-Letter-Queue & Selektiven Replay"
description: Einsatz eines persistenten BTP Data Stores für fehlgeschlagene Einzelnachrichten zur Ermöglichung eines punktuellen Wiederanlaufs.
resource: btp://conciliamus/decisions/ADR-004
tags: [adr, architecture-decision, data-store, dlq, resilience, replay]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /architecture/resilience-and-dead-letter.md }
  - { type: implementedBy, target: /iflows/reprocessor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# ADR-004: Data Store für Dead-Letter-Queue & Selektiven Replay

## Status
Akzeptiert (Accepted)

## Kontext
Bei technischen Netzwerkfehlern oder ERP-Ausfällen dürfen fehlgeschlagene Partnerdaten weder verloren gehen noch darf der Quell-Batch im MDM komplett neu getriggert werden (da dies zu doppelten OData-Zugriffen auf bereits angelegte Datensätze führen würde).

## Entscheidung
Wir nutzen den **BTP Cloud Integration Data Store** (`BP_FAILED_QUEUE`) als Dead Letter Queue:
- Fehlgeschlagene Einzelsätze werden serialisiert dort abgelegt.
- Ein Replay-Flow (`IFL_MDM_BP_Reprocessor`) kann diese Sätze einzeln wiedereinspielen.

## Konsequenzen
- **Positiv:** Kein Batch-Re-Run erforderlich.
- **Positiv:** Vollständige Nachvollziehbarkeit und Behebung von Transaktionsstörungen.
