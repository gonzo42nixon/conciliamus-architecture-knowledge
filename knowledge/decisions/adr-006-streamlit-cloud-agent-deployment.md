---
id: decisions/adr-006-streamlit-cloud-agent-deployment
type: Decision Record
title: "ADR-006: Serverless KI-Agenten-Bereitstellung via Streamlit Community Cloud & GitHub GitOps"
description: Bereitstellung des Conciliamus AI Architecture Advisor als Zero-Docker, Zero-Cost Serverless Web-App direkt aus GitHub mit nativer SAP BTP CORS-Bypass-Architektur.
resource: btp://conciliamus/decisions/ADR-006
tags: [adr, architecture-decision, streamlit, serverless, gitops, zero-docker, gemini, btp-cors, secrets-management]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T10:00:00Z"
relations:
  - { type: implements, target: /presentation-and-ui/streamlit-chat-advisor.md }
  - { type: dependsOn, target: /architecture/agent-deployment-and-gitops.md }
sources:
  - id: streamlit-repo
    resource: https://github.com/gonzo42nixon/conciliamus-architecture-knowledge
    title: Conciliamus Architecture Knowledge Repository
    author: "Dieter Rüffler"
---

# ADR-006: Serverless KI-Agenten-Bereitstellung via Streamlit Community Cloud & GitHub GitOps

## Status
Akzeptiert (Accepted)

## Kontext
Der **Conciliamus AI Architecture Advisor** dient als interaktiver KI-Architekturberater, Wissensvermittler und operative Test-Workbench für die SAP BTP Cloud Integration Business Partner Synchronisation. Bei der Bereitstellung der Anwendung für globale Stakeholder, Prüfer und Entwickler traten folgende Herausforderungen auf:

1. **Infrastruktur-Overhead vs. Wartbarkeit:**
   Klassische containerisierte Bereitstellungen (Docker-Container auf Cloud Foundry, SAP BTP Kyma, Google Cloud Run oder Kubernetes) verursachen kontinuierliche Hosting-Kosten, erfordern Container-Registries, Dockerfile-Wartung, Cluster-Konfigurationen und Kaltstart-Management.
2. **Das SAP BTP CORS-Dilemma (Cross-Origin Resource Sharing):**
   Wird die Test-Workbench als reine clientseitige Browser-Applikation (Single Page Application / SAP Fiori) ausgeführt, scheitern direkte HTTPS-Aufrufe an die Inbound-Adapter von SAP Cloud Integration. Der Browser erzwingt einen unauthentifizierten `OPTIONS`-Preflight-Request, den der CPI-Adapter mit `HTTP 401 Unauthorized` abweist. Ein Umweg über SAP BTP API Management war im Trial-Tenant durch 30-minütige Bereitstellungszeiten ("Integration Cell") und Rollenblockaden nicht zeitnah umsetzbar.
3. **Continuous Deployment (GitOps):**
   Änderungen an Architekturdokumenten (Google OKF v0.2), OpenAPI-Spezifikationen, BPMN-Konzepten oder UI-Komponenten müssen ohne manuelle Build- und Release-Schritte sofort weltweit verfügbar sein.
4. **Sicherheit & Geheimhaltung:**
   API-Schlüssel (Google AI Studio Gemini API) und vertrauliche SAP BTP Service-Credentials (OAuth2 Client-ID, Secret, Endpunkte) dürfen niemals im öffentlichen Git-Repository offengelegt werden.

## Entscheidung
Wir haben entschieden, den **Conciliamus AI Architecture Advisor** als serverlose Python-Webanwendung auf **Streamlit Community Cloud** mit direkter Anbindung an das GitHub-Repository bereitzustellen:

1. **Zero-Docker & Zero-Cost Serverless Hosting:**
   - Die Anwendung wird direkt aus dem GitHub-Repository (`gonzo42nixon/conciliamus-architecture-knowledge`) auf der Streamlit Community Cloud betrieben.
   - Der Stack wird deklarativ über eine standardisierte [`requirements.txt`](file:///requirements.txt) definiert; es sind keine Dockerfiles, Helm-Charts oder Container-Registries erforderlich.
2. **Automatisierte GitOps-Pipeline:**
   - Jeder Git-Push auf den Branch `main` triggert über Webhooks eine vollautomatische Aktualisierung der produktiven Live-App.
   - Das GitHub-Repository ist die kanonische *Single Source of Truth* für Wissen (OKF), API-Spezifikationen und Code.
3. **Serverseitige BTP-Testausführung (CORS-Bypass):**
   - Die Live-Ausführung von Batch-Tests gegen den SAP CPI Tenant erfolgt serverseitig in der Python-Runtime von Streamlit (`urllib.request`).
   - Da HTTP-Calls vom Server und nicht vom Webbrowser abgesetzt werden, greifen keine Browser-CORS-Restriktionen; der zweistufige OAuth2- und CSRF-Handshake wird direkt und performant ausgeführt.
4. **Hierarchisches Secrets Management & Session Gate:**
   - Sensitive Konfigurationsdaten (`GEMINI_API_KEY`, BTP-Credentials) werden verschlüsselt im Streamlit Secrets Vault hinterlegt und via `st.secrets` injiziert.
   - Eine Passwortschranke (`SESSION_PASSWORD`) schützt die Live-BTP-Ausführung und LLM-Quotas vor Missbrauch.
5. **In-Memory OKF Grounding:**
   - Beim App-Start werden alle OKF-Markdown-Dokumente und der Wissensgraph über `@st.cache_resource` in den Arbeitsspeicher geladen, was subsekundäre Retrieval-Zeiten für das LLM-Grounding ermöglicht.

## Konsequenzen
- **Positiv:**
  - **Zero-Cost & Zero-Maintenance:** Keine laufenden Server- oder Cloud-Kosten; keine Betriebssystem- oder Container-Patches.
  - **GitOps-Agilität:** Jede Dokumentations- oder Code-Änderung ist nach `git push` innerhalb von 10-30 Sekunden weltweit live.
  - **CORS-Eliminierung:** Zuverlässige, direkte Testausführung gegen SAP CPI ohne komplexe API-Gateway- oder Proxy-Konfigurationen.
  - **Robuste Sicherheit:** Strikte Trennung von Open-Source-Dokumentation (öffentlich) und Laufzeit-Secrets (privater Secret-Store).
- **Einschränkungen / Randbedingungen:**
  - **Ephemerer Speicher:** Zur Laufzeit geschriebene Dateien persistieren nicht über Neustarts hinaus; persistente Artefakte müssen im Git-Repository versioniert werden.
  - **Kaltstart bei Inaktivität:** Nach längerer Inaktivität wird die App in den Schlafmodus versetzt; das Aufwecken beim ersten Klick benötigt 3–5 Sekunden.
  - **Ressourcengrenze:** Free-Tier-Speicherbegrenzung auf 1 GB RAM; durch sparsames Caching der Wissensbasis (<50 MB) liegt der reale Verbrauch weit darunter.
