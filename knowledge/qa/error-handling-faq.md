---
id: qa/error-handling-faq
type: Architecture FAQ
title: Resilienz- und Troubleshooting-FAQ
description: Antworten auf Fragen zu Fehlerbehandlung, Dead Letter Queue und Wiederanlaufstrategien.
resource: btp://conciliamus/qa/error-handling
tags: [qa, faq, resilience, dlq, troubleshooting, errors]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: references, target: /architecture/resilience-and-dead-letter.md }
  - { type: references, target: /iflows/reprocessor-iflow.md }
  - { type: references, target: /decisions/adr-004-data-store-dlq.md }
sources:
  - id: conciliamus-arch
    resource: https://github.com/gonzo42nixon/Conciliamus/blob/main/docs/architektur.md
    title: Technische Architektur & Lösungskonzept
---

# Resilienz- und Troubleshooting-FAQ

### F: Wie unterscheidet die Architektur zwischen fachlichen und technischen Fehlern?
**A:** 
- **Fachliche Fehler (Business Errors):** Ungültige E-Mail-Adresse, Ländercode ungleich 2 Zeichen, fehlende Pflichtfelder oder mehr als 1 Treffer (Dublette). Sie erhalten den Status `FAILED_BUSINESS` und werden in den Message Attachments dokumentiert. Sie durchlaufen **keinen automatischen Wiederanlauf**, da identische Daten erneut scheitern würden.
- **Technische Fehler (Technical Errors):** HTTP 500, Timeout gegen S/4HANA, Netzwerkverbindungsabbrüche. Sie erhalten den Status `FAILED_TECHNICAL` und werden im persistenten BTP Data Store `BP_FAILED_QUEUE` gesichert.

### F: Wie funktioniert der Wiederanlauf (Replay) nach einer technischen Störung?
**A:** Über den dedizierten Flow `IFL_MDM_BP_Reprocessor` werden die im Data Store abgelegten Einzelsätze erneut an den `IFL_MDM_BP_Item_Processor` übergeben. Dadurch müssen bereits erfolgreich verarbeitete Datensätze des ursprünglichen Batches nicht erneut angefasst werden.

### F: Warum liefert die S/4HANA Sandbox HTTP 405 Method Not Allowed?
**A:** Die SAP Business Accelerator Hub Sandbox unterstützt für die Entität `API_BUSINESS_PARTNER` aus Sicherheitsgründen ausschließlich GET-Operationen. Ein `HTTP 405 OPERATION_NOT_SUPPORTED` bestätigt, dass der Aufruf syntaktisch und autorisierungstechnisch korrekt am SAP-Zielsystem ankam (siehe [Sandbox Limitationen](/verification/sandbox-limitations-405.md)).
