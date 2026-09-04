---
okf_version: "0.2"
title: Conciliamus SAP BTP Architecture Knowledge Index
description: Einstiegspunkt und Wurzelknoten der Wissensbasis für die MDM Business Partner Synchronisation mit SAP S/4HANA auf SAP BTP Cloud Integration.
---

# Conciliamus SAP BTP Architecture Knowledge Index

Willkommen im **Google Open Knowledge Format (OKF v0.2)** Bundle der Conciliamus GmbH. Dieser Index dient als Wurzelknoten für KI-Agenten und Architekten, um strukturiert in die Entwurfs- und Laufzeitkonzepte der Integrationslösung einzutauchen.

---

## 🏛️ 1. Architekturkonzepte (`architecture/`)
* [Dual-iFlow Entkopplungsmuster](/architecture/dual-iflow-pattern.md) – Grundlegendes Entwurfsmuster zur Trennung von Ingest und Fachlogik.
* [ProcessDirect Interconnect](/architecture/process-direct-interconnect.md) – Hochperformante, latenzfreie In-Memory-Kopplung innerhalb des BTP-Tenants.
* [Streaming Iterating Splitter](/architecture/streaming-iterating-splitter.md) – Speicheroptimierte Zerlegung von Massen-Batches ohne OOM-Gefahr.
* [Existenzprüfung & Router-Matrix](/architecture/existence-check-and-routing.md) – Idempotente OData GET Suche und deterministisches POST/PATCH Routing.
* [Session & CSRF Handshake](/architecture/session-and-csrf-handshake.md) – Two-Legged Handshake, X-CSRF-Token und Cookie-Handling für schreibende OData-Operationen.
* [Resilienz & Dead-Letter-Behandlung](/architecture/resilience-and-dead-letter.md) – Strikte Differenzierung von Business Errors und Technical Errors mit Data Store DLQ.

---

## ⚙️ 2. Integration Flow Spezifikationen (`iflows/`)
* [IFL_MDM_BP_Batch_Receiver](/iflows/batch-receiver-iflow.md) – Empfang, Header-Validierung, XML-Enveloping, Streaming-Split.
* [IFL_MDM_BP_Item_Processor](/iflows/item-processor-iflow.md) – Atomare Validierung, Existenzcheck, dynamisches S/4HANA-Mapping, Error-Subprocess.
* [IFL_MDM_BP_Reprocessor](/iflows/reprocessor-iflow.md) – Selektiver Wiederanlauf fehlgeschlagener Sätze aus dem Data Store ohne Batch-Neustart.

---

## ⚖️ 3. Architecture Decision Records (`decisions/`)
* [ADR-001: Dual-iFlow Entkopplungsmuster](/decisions/adr-001-dual-iflow-decoupling.md) – Warum kein monolithischer iFlow?
* [ADR-002: ProcessDirect statt Message Queues](/decisions/adr-002-process-direct.md) – Latenzfreie Kopplung vs. JMS-Kosten.
* [ADR-003: BPMN 2.0 Method & Style (Bruce Silver)](/decisions/adr-003-bpmn-method-and-style.md) – Selbstdokumentierende Nomenklatur `[Aktiv-Verb] + [Objekt]`.
* [ADR-004: Data Store für Dead-Letter-Queue & Selektiver Replay](/decisions/adr-004-data-store-dlq.md) – Granularer Wiederanlauf fehlerhafter Datensätze.
* [ADR-005: Single-Viewport Ergonomie für die Fiori Workbench](/decisions/adr-005-single-viewport-fiori.md) – 100% no-outer-scroll Layout-Architektur.

---

## 📋 4. Datenkontrakte & Mappings (`data-contracts/`)
* [MDM Inbound JSON Kontrakt](/data-contracts/mdm-inbound-contract.md) – Quellformat von JSD-MDM, Validierungsregeln und Feldmatrix.
* [SAP S/4HANA OData Mapping](/data-contracts/s4-odata-mapping.md) – Semantische Zuordnung zu `A_BusinessPartner` und Deep-Insert-Strukturen.
* [Custom Header Properties & MPL](/data-contracts/custom-header-properties.md) – Metadaten zur Volltextsuche im Web-Monitoring der Integration Suite.

---

## ✅ 5. Verifikation & Prüfnachweise (`verification/`)
* [Live-End-to-End Testlauf auf SAP BTP](/verification/live-btp-execution.md) – Erfolgreicher Durchlauf am 04.09.2026 mit HTTP 200 OK.
* [ISTQB Teststrategie & Testdaten](/verification/istqb-test-strategy.md) – Grenzwertanalyse, 10er-Vollbatch (3x PATCH, 7x POST) und Fehlertests.
* [SAP Sandbox Limitationen (HTTP 405)](/verification/sandbox-limitations-405.md) – Nachweisführung und Abfangen von `OPERATION_NOT_SUPPORTED`.

---

## 🖥️ 6. Präsentation & Interaktive Werkzeuge (`presentation-and-ui/`)
* [Pecha Kucha 20x20 Präsentation](/presentation-and-ui/pecha-kucha-20x20.md) – 20 Folien à 20s (6:40 Min.), Sprechtexte, Timer & Firebase-Login.
* [SAP Fiori Workbench UI](/presentation-and-ui/fiori-workbench-ui.md) – Single-Viewport, interaktive aufklappbare JSON-Pills & Monitoring-Drawer.

---

## ❓ 7. Architektur-FAQ für KI-Agenten (`qa/`)
* [Zentrale Architekturfragen & Antworten](/qa/core-architecture-faq.md) – Strukturierte Frage-Antwort-Paare zur Lösungsarchitektur.
* [Resilienz- und Troubleshooting-FAQ](/qa/error-handling-faq.md) – Verhalten bei Timeouts, Duplikaten und ungültigen Stammdaten.
