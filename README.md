# Conciliamus Architecture Knowledge Base (OKF v0.2)

> **Google Open Knowledge Format (OKF)** Repository für die Enterprise-Architektur der **SAP BTP Cloud Integration Business Partner Synchronisation** der Conciliamus GmbH.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app)
[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1.0-green.svg)](api/conciliamus-runtime-iflows.openapi.yaml)
[![OKF Version](https://img.shields.io/badge/OKF-v0.2-blue.svg)](knowledge/index.md)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%203.6%20Flash-orange.svg)](https://aistudio.google.com)

Dieses Repository sammelt das vollständige architektonische, methodische, technische und betriebliche Wissen aus dem Referenz-Repository [gonzo42nixon/Conciliamus](https://github.com/gonzo42nixon/Conciliamus) und überführt es in den herstellerneutralen, agenten-optimierten Standard **Google Open Knowledge Format (OKF v0.2)**.

---

## 🌐 Weltweiter Live-KI-Architekturberater (Streamlit Cloud)

Der **Conciliamus Architecture Advisor** ist als serverlose, weltweit erreichbare Chat-Webanwendung live geschaltet:

👉 **[https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app](https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app)**

### Highlights der Webanwendung
- **Gegroundetes KI-Consulting:** Angetrieben von **Google Gemini 3.6 Flash** (via `google-genai` SDK) unter Verwendung der verifizierten OKF-Architekturdokumente und 6 ADRs als kanonische Faktenquelle.
- **Zero-Docker & GitOps CI/CD:** Vollautomatische Bereitstellung direkt aus GitHub auf Streamlit Community Cloud ([ADR-006](knowledge/decisions/adr-006-streamlit-cloud-agent-deployment.md)) mit nativer BTP CORS-Bypass-Architektur.
- **Multimodale Antworten:** Antwortet mit dynamisch generierten **Mermaid-Sequenzdiagrammen**, exakten Quellenverlinkungen und BPMN 2.0 Method & Style Nomenklatur.
- **Live BTP Test-Runner & Workbench:** Operative Ausführung von Test-Batches gegen SAP Cloud Integration inklusive automatischem OAuth2- & CSRF-Handshake.
- **Resilienz & Model Failover:** Fängt temporäre Lastspitzen (HTTP 503) automatisch über Failover-Modelle (`gemini-2.0-flash`, `gemini-1.5-flash`) und Offline-Grounding ab.
- **Integrierter ADR- & API-Explorer:** Ermöglicht das direkte Durchblättern aller Architecture Decision Records (ADR-001 bis ADR-006) und OpenAPI 3.1.0 Spezifikationen.
- **Lokaler Start:**
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```

---

## 🎯 Zweck & Zielbild

1. **Digital Brain für KI-Agenten:** Strukturierte Wissensrepräsentation als kanonische Faktenquelle (Grounding Layer) für LLM- und API-basierte Architektur-Agenten.
2. **Standardisierte OKF-Ontologie:** Jede Wissenseinheit liegt als eigenständiges Markdown-Dokument mit standardisiertem YAML-Frontmatter und obligatorischem `type`-Feld vor.
3. **Traversierbarer Knowledge Graph:** Explizite typisierte Kanten (`contains`, `implements`, `routesTo`, `verifies`, `dependsOn`, `handlesError`) verknüpfen Konzepte zu einem gerichteten Wissensgraphen.
4. **API-Agenten-Schnittstelle:** Deklarative Konfiguration via `manifest/agent.yaml` (`KnowledgeAgent`) und OpenAPI 3.1 Tools in `api/conciliamus-architecture.openapi.yaml`.
5. **Traceability & Verifikation:** Lückenlose Dokumentation von Architektur-Entscheidungen (ADRs), ISTQB-Teststrategien, Live-BTP-Prüfnachweisen (HTTP 200 OK) und Fiori-UI-Artefakten.

---

## 🏛️ Architektur-Überblick

Die dokumentierte Lösung realisiert eine robuste, idempotente Massendaten-Synchronisation zwischen einem externen MDM-System (`JSD-MDM`) und der SAP S/4HANA OData API via **Dual-iFlow Entkopplung** auf SAP BTP Cloud Integration:

```mermaid
flowchart TD
    MDM["MDM Quellsystem<br/>(JSD-MDM Batch JSON)"] -->|HTTPS Inbound| IF1["iFlow 1: Batch Receiver<br/>(IFL_MDM_BP_Batch_Receiver)"]
    
    subgraph IF1_BOX ["iFlow 1: Ingest & Entkopplung"]
        IF1 --> VAL1["Syntax- & Schema-Validierung"]
        VAL1 --> SPLIT["Streaming Iterating Splitter"]
    end
    
    SPLIT -->|ProcessDirect<br/>(In-Memory)| IF2["iFlow 2: Item Processor<br/>(IFL_MDM_BP_Item_Processor)"]
    
    subgraph IF2_BOX ["iFlow 2: Atomare Verarbeitung"]
        IF2 --> VAL2["Fachliche Validierung"]
        VAL2 --> GET["OData GET Existenzprüfung<br/>(SearchTerm1 eq externalId)"]
        GET --> ROUTER{"Treffermenge"}
        ROUTER -->|"0 Treffer"| POST["HTTP POST /A_BusinessPartner<br/>(Neuanlage / Deep Insert)"]
        ROUTER -->|"1 Treffer"| PATCH["HTTP PATCH /A_BusinessPartner('{id}')<br/>(Dynamische ID-Übernahme)"]
        ROUTER -->|">1 Treffer"| DUP["Fachlicher Fehler: Duplikat"]
    end

    subgraph RES_BOX ["Resilienz & Wiederanlauf"]
        IF2 -->|Technischer Fehler| DLQ[("Data Store: BP_FAILED_QUEUE")]
        DLQ -.->|Selektiver Replay| IF3["iFlow 3: Reprocessor<br/>(IFL_MDM_BP_Reprocessor)"]
        IF3 -.->|ProcessDirect| IF2
    end
```

---

## 📂 Repository-Struktur

```text
conciliamus-architecture-knowledge/
├── README.md                                  # Repository-Dokumentation & Spezifikationsüberblick
├── package.json                               # Node/Tooling Metadaten & Ausführungsskripte
├── manifest/                                  # Deklarative Agentenkonfiguration
│   └── agent.yaml                             # KnowledgeAgent Manifest (Rolle, Scope, Retrieval, Tools)
├── api/                                       # OpenAPI 3.1 Schnittstellenspezifikation
│   └── conciliamus-architecture.openapi.yaml  # API-Definition für Tool-Calls des Architektur-Agenten
├── schemas/                                   # JSON-Schemas zur formalen Validierung
│   ├── okf-concept.schema.json                # Schema für OKF Frontmatter & Relationen
│   ├── agent-manifest.schema.json             # Schema für KnowledgeAgent Manifest
│   ├── mdm-batch.schema.json                  # Schema für Quell-JSON (JSD-MDM)
│   └── s4-business-partner.schema.json        # Schema für Ziel-OData A_BusinessPartner
├── knowledge/                                 # Das kuratierte OKF-Bundle (Markdown mit Frontmatter)
│   ├── index.md                               # Root Knowledge Manifest (okf_version: "0.2")
│   ├── architecture/                          # Kernkonzepte der Lösungsarchitektur
│   │   ├── dual-iflow-pattern.md              # Entkopplung Transport vs. Atomare Verarbeitung
│   │   ├── process-direct-interconnect.md     # In-Memory Tenant-Kopplung
│   │   ├── streaming-iterating-splitter.md    # Speicherschonende Batch-Vereinzelung
│   │   ├── existence-check-and-routing.md     # OData GET Existenzprüfung & Router-Matrix
│   │   ├── session-and-csrf-handshake.md      # Two-Legged Handshake & Cookie-Handling
│   │   ├── resilience-and-dead-letter.md      # Dual-Channel Fehlerbehandlung & DLQ
│   │   └── agent-deployment-and-gitops.md     # Serverless GitOps & BTP CORS-Bypass
│   ├── iflows/                                # Spezifikationen der Integration Flows
│   │   ├── batch-receiver-iflow.md            # IFL_MDM_BP_Batch_Receiver Detail-Spezifikation
│   │   ├── item-processor-iflow.md            # IFL_MDM_BP_Item_Processor Detail-Spezifikation
│   │   └── reprocessor-iflow.md               # IFL_MDM_BP_Reprocessor (Selektiver Replay)
│   ├── decisions/                             # Architecture Decision Records (ADRs)
│   │   ├── adr-001-dual-iflow-decoupling.md   # ADR-001: Dual-iFlow Entkopplungsmuster
│   │   ├── adr-002-process-direct.md          # ADR-002: ProcessDirect statt JMS Queues
│   │   ├── adr-003-bpmn-method-and-style.md   # ADR-003: Bruce Silver Namenskonventionen
│   │   ├── adr-004-data-store-dlq.md          # ADR-004: Data Store für selektiven Replay
│   │   ├── adr-005-single-viewport-fiori.md   # ADR-005: Single-Viewport Fiori Workbench
│   │   └── adr-006-streamlit-cloud-agent-deployment.md # ADR-006: Serverless Streamlit Cloud & GitOps
│   ├── data-contracts/                        # Schnittstellenkontrakte & Datenmodelle
│   │   ├── mdm-inbound-contract.md            # JSD-MDM JSON Schema & Felddefinitionen
│   │   ├── s4-odata-mapping.md                # Feldmapping zu SAP S/4HANA OData
│   │   └── custom-header-properties.md        # Metadaten & Volltextsuche im MPL
│   ├── verification/                          # Prüf- & Testnachweise
│   │   ├── live-btp-execution.md              # Verifizierter Testlauf (HTTP 200) am 04.09.2026
│   │   ├── istqb-test-strategy.md             # ISTQB Testfallmatrix (3x PATCH, 7x POST)
│   │   └── sandbox-limitations-405.md         # Dokumentation & Handling des Sandbox HTTP 405
│   ├── presentation-and-ui/                   # Interaktive Werkzeuge & Präsentation
│   │   ├── pecha-kucha-20x20.md               # 20 Folien × 20s Konzept, Sprechtexte & Timing
│   │   └── fiori-workbench-ui.md              # Single-Viewport UI, JSON-Pills & Firebase-Login
│   └── qa/                                    # Strukturierte Fragen & Antworten für Agenten
│       ├── core-architecture-faq.md           # Häufige Architekturfragen & kanonische Antworten
│       └── error-handling-faq.md              # Resilienz- und Troubleshooting-FAQ
├── graph/                                     # Knowledge Graph Repräsentationen
│   ├── relations.yaml                         # Typisierte Relationen und Kanten
│   ├── architecture-graph.mmd                 # Mermaid Visualisierung des Knowledge Graph
│   └── knowledge-graph.json                   # Maschinenlesbarer Adjazenzgraph für Retrieval
└── tooling/                                   # Validierungs- & Query-Werkzeuge
    ├── validate_okf.py                        # Validiert Frontmatter, mandatory 'type', Links & Schemas
    ├── build_graph.py                         # Generiert knowledge-graph.json & Mermaid Graph
    └── query_agent_cli.py                     # CLI Tool zur interaktiven Simulation des Agenten
```

---

## 🤖 Agenten-Integration & API

Der künftige **Architektur-Agent** wird deklarativ gesteuert über:

1. **Manifest (`manifest/agent.yaml`):**
   - Definiert Persona, Aufgabenbereich und Retrieval-Beschränkungen.
   - Startet bei `knowledge/index.md` und traversiert Kanten über Relationen.
   - Fordert zwingende Quellenangaben für jede Antwort ein.
2. **OpenAPI Spezifikation (`api/conciliamus-architecture.openapi.yaml`):**
   - Stellt standardisierte Tools für LLMs bereit:
     - `searchConcepts`: Semantische Schlagwortsuche
     - `getConcept`: Abruf eines Wissensdokuments anhand der ID
     - `getArchitectureDecision`: Gezielte Konsultation von ADRs
     - `getKnowledgeGraph`: Topologie-Abfrage der Systemkomponenten

---

## 🛠️ Tooling & Validierung

```bash
# 1. OKF-Bundle auf Vollständigkeit, Links und Frontmatter validieren:
python tooling/validate_okf.py

# 2. Knowledge Graph neu aus den Markdown-Dateien generieren:
python tooling/build_graph.py

# 3. Interaktive Agenten-Abfrage in der Konsole testen:
python tooling/query_agent_cli.py "Warum wurde ein Dual-iFlow Entwurfsmuster gewählt?"
```

---

## 📜 Lizenz & Urheber
- **Autor:** Dieter Rüffler (Diplom-Informatiker, Senior SAP Integration Specialist & Architect)
- **Projekt:** Conciliamus GmbH (Johannesstift Diakonie gAG) – Dev-Task
- **Spezifikation:** Google Cloud Open Knowledge Format (OKF v0.2)
