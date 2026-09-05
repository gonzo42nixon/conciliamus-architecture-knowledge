---
id: qa/core-architecture-faq
type: Architecture FAQ
title: Zentrale Architekturfragen & Antworten
description: Kanonische Fragen und Antworten zur Architektur für den API-Architektur-Agenten.
resource: btp://conciliamus/qa/core-architecture
tags: [qa, faq, architecture, agent, reasoning]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: references, target: /architecture/dual-iflow-pattern.md }
  - { type: references, target: /architecture/existence-check-and-routing.md }
  - { type: references, target: /decisions/adr-001-dual-iflow-decoupling.md }
  - { type: references, target: /decisions/adr-005-process-direct.md }
sources:
  - id: conciliamus-repo
    resource: https://github.com/gonzo42nixon/Conciliamus
    title: Conciliamus Master Repository
---

# Zentrale Architekturfragen & Antworten

### F: Warum wurde die Lösung in zwei getrennte iFlows aufgeteilt (Dual-iFlow)?
**A:** Ein monolithischer iFlow würde beim Scheitern eines einzigen Geschäftspartners den gesamten Batch abbrechen. Das Dual-iFlow Entkopplungsmuster (`IFL_MDM_BP_Batch_Receiver` ➔ ProcessDirect ➔ `IFL_MDM_BP_Item_Processor`) trennt den Netzwerk-Ingest und das Streaming-Splitting von der fachlichen Einzelverarbeitung. Dies stellt vollständige Fehlerisolation sicher: 9 erfolgreiche Partner werden ins ERP eingespielt, selbst wenn 1 Partner wegen falscher Daten scheitert (siehe [ADR-001](/decisions/adr-001-dual-iflow-decoupling.md)).

### F: Warum wird ProcessDirect statt JMS Message Queues verwendet?
**A:** ProcessDirect verbindet iFlows innerhalb desselben Tenants rein speicherintern (In-Memory Java Call). Dies vermeidet Netzwerk- und Serialisierungskosten und benötigt keine kostenpflichtigen oder begrenzten JMS-Queue-Ressourcen auf SAP BTP (siehe [ADR-005](/decisions/adr-005-process-direct.md)).

### F: Wie wird Idempotenz bei wiederholtem Senden sichergestellt?
**A:** Vor jeder schreibenden Operation führt der `Item_Processor` eine OData-GET-Existenzprüfung gegen S/4HANA aus (`SearchTerm1 eq '${property.externalId}'`). Werden 0 Treffer gefunden, erfolgt ein `POST` (Neuanlage). Wird genau 1 Treffer gefunden, wird die ermittelte interne BusinessPartner-Nummer dynamisch in die URL übernommen und ein `PATCH` (Delta-Update) ausgeführt (siehe [Existenzprüfung & Router-Matrix](/architecture/existence-check-and-routing.md)).
