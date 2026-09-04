---
id: iflows/reprocessor-iflow
type: iFlow Specification
title: "IFL_MDM_BP_Reprocessor: Selektiver Wiederanlauf"
description: Spezifikation des Wiederanlauf-Flows zum selektiven Wiedereinspielen fehlgeschlagener Datensätze aus der Dead Letter Queue.
resource: btp://conciliamus/iflows/IFL_MDM_BP_Reprocessor
tags: [iflow, reprocessor, dlq, data-store, replay, resilience]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implements, target: /decisions/adr-004-data-store-dlq.md }
  - { type: routesTo, target: /iflows/item-processor-iflow.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
    author: "Dieter Rüffler"
---

# IFL_MDM_BP_Reprocessor

## Technische Kenndaten
- **Paket:** `Conciliamus - Business Partner Integration`
- **Technischer Name:** `IFL_MDM_BP_Reprocessor`
- **Trigger:** Timer-basiert (z.B. alle 15 Minuten) oder manueller HTTP-Trigger
- **Datenquelle:** Data Store `BP_FAILED_QUEUE`
- **Ziel:** ProcessDirect `/conciliamus/v1/businesspartners/item`

## Ablauf
1. **Poll Data Store:** Liest persistierte Nachrichteneinträge aus `BP_FAILED_QUEUE`.
2. **Selektives Routing:** Übergibt die Payload erneut an den `IFL_MDM_BP_Item_Processor`.
3. **Erfolgsprüfung:** Bei erfolgreicher Verarbeitung wird der Eintrag aus dem Data Store gelöscht.
4. **Resilienz:** Bei erneutem Fehlschlag verbleibt der Satz mit inkrementiertem Retry-Zähler im Store.
