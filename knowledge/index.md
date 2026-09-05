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
* [KI-Agenten-Bereitstellung & GitOps-Architektur](/architecture/agent-deployment-and-gitops.md) – Zero-Docker Serverless Hosting, GitOps Continuous Deployment und nativer SAP BTP CORS-Bypass.

---

## ⚙️ 2. Integration Flow Spezifikationen (`iflows/`)
* [IFL_MDM_BP_Batch_Receiver](/iflows/batch-receiver-iflow.md) – Empfang, Header-Validierung, XML-Enveloping, Streaming-Split.
* [IFL_MDM_BP_Item_Processor](/iflows/item-processor-iflow.md) – Atomare Validierung, Existenzcheck, dynamisches S/4HANA-Mapping, Error-Subprocess.
* [IFL_MDM_BP_Reprocessor](/iflows/reprocessor-iflow.md) – Selektiver Wiederanlauf fehlgeschlagener Sätze aus dem Data Store ohne Batch-Neustart.

---

## ⚖️ 3. Architecture Decision Records (`decisions/`)
* [ADR-001: Dual-iFlow Entkopplungsmuster](/decisions/adr-001-dual-iflow-decoupling.md) – Warum kein monolithischer iFlow?
* [ADR-002: Zero-Trust & BTP PaaS Security Architecture](/decisions/adr-002-zero-trust-btp-security.md) – BTP als Managed PaaS, OAuth2 Client Credentials & Vault ab Sekunde Null.
* [ADR-003: End-to-End Correlation & MPL Governance](/decisions/adr-003-end-to-end-correlation-mpl.md) – Globale Correlation-ID & Custom Header Properties im Message Processing Log.
* [ADR-004: BPMN 2.0 Method & Style (Bruce Silver)](/decisions/adr-004-bpmn-method-and-style.md) – Selbstdokumentierende Nomenklatur `[Aktiv-Verb] + [Objekt]`.
* [ADR-005: ProcessDirect statt Message Queues](/decisions/adr-005-process-direct.md) – Latenzfreie In-Memory Kopplung vs. JMS-Queue-Lizenzkosten.
* [ADR-006: Idempotente Existenzprüfung & Router-Matrix](/decisions/adr-006-idempotent-existence-check.md) – OData GET SearchTerm1 vor Schreibzugriff: POST vs. PATCH Matrix.
* [ADR-007: Two-Legged CSRF- & Cookie-Handshake](/decisions/adr-007-two-legged-csrf-handshake.md) – Zweistufiges Token- & Session-Handling für schreibende OData V2 Calls.
* [ADR-008: Data Store für Dead-Letter-Queue & Selektiver Replay](/decisions/adr-008-data-store-dlq.md) – Granularer Wiederanlauf fehlerhafter Datensätze ohne Batch-Neustart.
* [ADR-009: Single-Viewport Ergonomie für die Fiori Workbench](/decisions/adr-009-single-viewport-fiori.md) – 100% no-outer-scroll Layout-Architektur im Fiori Horizon Look.
* [ADR-010: Serverless KI-Agenten-Bereitstellung via Streamlit Cloud & GitOps](/decisions/adr-010-streamlit-cloud-agent-deployment.md) – Zero-Docker, Zero-Cost und BTP CORS-Bypass.
* [ADR-011: Google Open Knowledge Format (OKF v0.2) & Grounded AI Architecture Advisor](/decisions/adr-011-google-okf-knowledge-graph.md) – Maschinenlesbarer Wissensgraph & Zero-Hallucination Consulting.

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
* [Conciliamus Architecture Advisor (Streamlit)](/presentation-and-ui/streamlit-chat-advisor.md) – Weltweit verfügbare KI-Chat-App auf Basis von Google AI Studio & Gemini 3.6 Flash.

---

## ❓ 7. Architektur-FAQ für KI-Agenten (`qa/`)
* [Zentrale Architekturfragen & Antworten](/qa/core-architecture-faq.md) – Strukturierte Frage-Antwort-Paare zur Lösungsarchitektur.
* [Resilienz- und Troubleshooting-FAQ](/qa/error-handling-faq.md) – Verhalten bei Timeouts, Duplikaten und ungültigen Stammdaten.
