---
id: presentation-and-ui/streamlit-chat-advisor
type: UI Component
title: "Conciliamus Architecture Advisor (Streamlit Web App)"
description: Weltweit verfuegbare Serverless Webanwendung auf Basis von Streamlit Community Cloud und Google AI Studio (Gemini 3.6 Flash) mit dynamischem Grounding auf das OKF-Wissensbuendel.
resource: https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app
tags: [streamlit, ui, gemini, google-ai-studio, cloud, chat, grounding, serverless]
status: productive
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T09:20:00Z"
relations:
  - { type: implements, target: /decisions/adr-001-dual-iflow-decoupling.md }
  - { type: implements, target: /decisions/adr-010-streamlit-cloud-agent-deployment.md }
  - { type: dependsOn, target: /architecture/agent-deployment-and-gitops.md }
  - { type: references, target: /presentation-and-ui/fiori-workbench-ui.md }
sources:
  - id: streamlit-app
    resource: https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/app.py
    title: Streamlit Webanwendung
    author: "Dieter Rueffler"
---

# Conciliamus Architecture Advisor (Streamlit Web App)

## Live-Zugang
- **Produktions-URL:** [https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app](https://conciliamus-architecture-knowledge-n7yvultp4bp95kpjwx3hrb.streamlit.app)
- **Hosting-Plattform:** Streamlit Community Cloud (Serverless, Zero-Docker, Zero-Cost)
- **Backend-LLM:** Google AI Studio (Gemini 3.6 Flash via `google-genai` SDK)
- **Quellcode:** [`app.py`](file:///app.py) / [`streamlit_app.py`](file:///streamlit_app.py)

---

## Architektur & Funktionsweise

Die Webanwendung fungiert als interaktiver, menschenzentrierter KI-Berater fuer das gesamte Architekturensemble der Conciliamus SAP BTP Loesung:

1. **In-Memory Wissensindex:**
   Beim Starten der App werden alle 25 Markdown-Dokumente aus `knowledge/` sowie der Wissensgraph (`graph/knowledge-graph.json`) und das Agenten-Manifest (`manifest/agent.yaml`) ueber `@st.cache_resource` in den Hauptspeicher geladen.
2. **Semantischer Retriever:**
   Eingehende Benutzerfragen werden analysiert; die relevantesten Konzepte und ADRs werden automatisch priorisiert und formatiert.
3. **Kontext-Grounding & System Prompt:**
   Das offizielle Agenten-Profil (*Senior SAP BTP Cloud Integration Specialist & Enterprise Architect*) wird zusammen mit den extrahierten Originaldokumenten an Gemini uebergeben.
4. **Resilienz & Model Failover:**
   Sollte das Primaermodell `gemini-3.6-flash` temporaere Lastspitzen (`HTTP 503 UNAVAILABLE`) oder Rate Limits aufweisen, schwenkt die Anwendung automatisch auf `gemini-2.0-flash` bzw. `gemini-1.5-flash` um oder liefert einen garantierten Offline-Extrakt.
5. **Multimodale Praesentation:**
   Antworten koennen native Mermaid-Diagramme, anklickbare Quellenbelege zu GitHub-Dateien und interaktive Filter enthalten.

---

## Anwendungsreiter

- **💬 Architektur-Chat:** Dialogführung mit Historie, Schnellanfragen und klickbaren Quellen-Expandern.
- **📜 Architecture Decisions (ADRs):** Direkte Einsicht in alle verifizierten Architecture Decision Records ([ADR-001](/decisions/adr-001-dual-iflow-decoupling.md) bis [ADR-010](/decisions/adr-010-streamlit-cloud-agent-deployment.md)).
- **🎤 Pecha Kucha (20x20):** Interaktive 20-Folien-Präsentation mit automatischem 20s-Timer und Sprechertexten.
- **🧪 Test-Runner (Workbench):** Operative Testausführung von Batch-Payloads direkt gegen SAP CPI mit automatischer OAuth2- und CSRF-Handshake-Verarbeitung ohne CORS-Blockaden.
- **📐 OpenAPI & Schemas:** Direkte Einsicht und Verlinkung auf die Laufzeit-Schnittstellenspezifikationen (`api/conciliamus-runtime-iflows.openapi.yaml`).
