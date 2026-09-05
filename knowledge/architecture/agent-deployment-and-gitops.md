---
id: architecture/agent-deployment-and-gitops
type: Architecture Concept
title: KI-Agenten-Bereitstellung & GitOps-Architektur
description: Architekturkonzept für die serverlose Bereitstellung des Conciliamus AI Architecture Advisor via Streamlit Community Cloud, GitHub GitOps und hybrider BTP-Ausführung.
resource: btp://conciliamus/architecture/agent-deployment-gitops
tags: [architecture, deployment, gitops, streamlit, serverless, cors, security, gemini, btp]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T10:00:00Z"
relations:
  - { type: implements, target: /decisions/adr-006-streamlit-cloud-agent-deployment.md }
  - { type: contains, target: /presentation-and-ui/streamlit-chat-advisor.md }
sources:
  - id: conciliamus-repo
    resource: https://github.com/gonzo42nixon/conciliamus-architecture-knowledge
    title: Conciliamus Architecture Knowledge Base
    author: "Dieter Rüffler"
---

# KI-Agenten-Bereitstellung & GitOps-Architektur

## 1. Topologie & Gesamtsystem

Der **Conciliamus AI Architecture Advisor** kombiniert agentenbasierte Wissensvermittlung auf Basis des Google Open Knowledge Format (OKF v0.2) mit einer operativen SAP BTP Integrations-Workbench in einer **vollständig serverlosen, Docker-freien Cloud-Architektur**.

```mermaid
flowchart TD
    subgraph GITHUB ["GitHub: Single Source of Truth (gonzo42nixon)"]
        REPO["Repository: conciliamus-architecture-knowledge<br/>• OKF Knowledge Bundle (knowledge/)<br/>• OpenAPI 3.1 Spezifikationen (api/)<br/>• Streamlit App (app.py, requirements.txt)"]
    end

    subgraph STREAMLIT_CLOUD ["Streamlit Community Cloud (Serverless Python Runtime)"]
        HOOK["Automated GitOps Webhook Engine"]
        CACHE[("@st.cache_resource In-Memory Index<br/>25+ OKF-Konzepte & Knowledge Graph")]
        SEC["Secrets Vault (st.secrets)<br/>• GEMINI_API_KEY<br/>• BTP Service Credentials<br/>• SESSION_PASSWORD"]
        RUNNER["Python Execution Engine<br/>• OAuth2 Client Credentials Handshake<br/>• X-CSRF-Token & Session-Cookies<br/>• Batch POST Inbound Execution"]
        CHAT["AI Chat Engine & Multi-Tier Fallback"]
    end

    subgraph EXTERNAL_SERVICES ["Externe Cloud-Dienste"]
        GEMINI["Google AI Studio<br/>Gemini 3.6 Flash / 2.0 / 1.5"]
        BTP["SAP BTP Cloud Integration Tenant<br/>• IFL_MDM_BP_Batch_Receiver<br/>• Inbound HTTPS Adapter"]
    end

    USER(["Globaler Benutzer / Architekt (Browser)"])

    REPO -->|Git Push Event / Webhook| HOOK
    HOOK -->|Auto-Build & Deployment| CACHE
    SEC -.->|Injektion| RUNNER
    SEC -.->|Injektion| CHAT

    USER <-->|HTTPS Web Interface| STREAMLIT_CLOUD
    CHAT <-->|Gegroundeter Prompt & Streaming| GEMINI
    RUNNER <-->|Direkter Server-zu-Server Call (Zero CORS)| BTP
```

---

## 2. GitHub als Single Source of Truth & GitOps CI/CD

Das gesamte Projekt folgt dem deklarativen **GitOps-Paradigma**:

1. **Zentrales Wissens- und Code-Repository:**
   - Alle Architekturentscheidungen (ADR-001 bis ADR-006), Schnittstellenverträge, BPMN-Dokumentationen und UI-Komponenten sind als versionierte Markdown-Dokumente im Ordner `knowledge/` abgelegt.
   - Code, Abhängigkeiten (`requirements.txt`) und Agenten-Manifeste (`manifest/agent.yaml`) befinden sich im selben Repository.
2. **Zero-Touch Continuous Deployment:**
   - Sobald ein Commit auf den Branch `main` gepusht wird, erkennt die Streamlit Community Cloud über einen Webhook die Änderung.
   - Ein automatisierter Build-Prozess zieht das Repository, installiert bei Bedarf geänderte Abhängigkeiten und startet den Container unterbrechungsfrei neu.
   - Entwicklungs- und Dokumentationszyklen erfordern keinerlei manuelles Eingreifen auf Serverebene.
3. **Lokale Validierung vor dem Push:**
   - Qualitätssicherungs-Skripte stellen sicher, dass nur fehlerfreie Wissensbündel live geschaltet werden:
     ```bash
     # Validierung aller Frontmatter-Metadaten und Markdown-Hyperlinks
     python tooling/validate_okf.py
     
     # Neuerstellung der Knowledge-Graph-Topologie
     python tooling/build_graph.py
     
     # Automatisierte Testsuite (OKF-Konformität)
     python -m pytest tests/test_okf.py
     ```

---

## 3. Beseitigung der SAP BTP CORS-Hürde

### Das Problem bei reinen Browser-Anwendungen (SPAs)
Wird eine Webanwendung (z. B. ein SAP Fiori Test-Runner) rein im Client-Browser ausgeführt, erzwingt die Same-Origin-Policy bei Cross-Origin-Requests an SAP Cloud Integration einen HTTP `OPTIONS`-Preflight:

$$\text{Browser} \xrightarrow{\text{OPTIONS (unauthenticated)}} \text{SAP Cloud Integration Inbound Adapter} \xrightarrow{\text{HTTP 401 Unauthorized}} \text{Browser CORS Error}$$

Da der Standard-HTTPS-Adapter von SAP CPI unauthentifizierte `OPTIONS`-Aufrufe standardmäßig mit `HTTP 401 Unauthorized` abweist und kein CORS-Modul besitzt, schlägt jeder direkte Browseraufruf fehl. Die Einrichtung von SAP BTP API Management zur CORS-Terminierung scheitert in Trial-Tenants häufig an 30-minütigen Provisionierungs-Warteschleifen ("Integration Cell") und Rollenberechtigungen.

### Die Lösung: Serverseitige Python-Ausführung in Streamlit
In Streamlit Community Cloud wird der Testlauf **nicht im Browser des Clients**, sondern im **Python-Backend des Streamlit-Containers** ausgeführt:

1. **Kein CORS-Preflight:** Server-zu-Server-Aufrufe (`urllib.request` / `requests`) unterliegen keiner Browser-Sicherheitsrestriktion.
2. **Vollständiger Two-Legged Handshake:**
   - **Schritt 1 (OAuth2 Token):** POST mit `grant_type=client_credentials` gegen den XSUAA/IAS Token-Service unter Verwendung von Base64-kodierten Service-Credentials.
   - **Schritt 2 (CSRF & Session Cookies):** HEAD-Request an den CPI-Endpunkt mit Header `X-CSRF-Token: Fetch` und Verwaltung des Session-Cookies via `http.cookiejar`.
   - **Schritt 3 (Batch Payload POST):** POST des JSD-MDM Inbound-JSON mit `Content-Type: application/json`, mitgeführtem `X-CSRF-Token` und Session-Cookies.
3. **Audit-Log-Streaming:** Die einzelnen Ausführungsschritte und detaillierte MPL-Metadaten werden in Echtzeit in der Streamlit-Oberfläche visualisiert.

---

## 4. Sicherheits- & Secrets-Architektur

Die Architektur folgt strikt den Prinzipien der *12-Factor App* bezüglich Konfiguration und Geheimhaltung:

| Parameter | Speicherort Lokal | Speicherort Cloud | Zweck |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | Zugriff auf Google AI Studio Gemini API |
| `SESSION_PASSWORD` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | Absicherung des Live-Runners & Chat-Limits |
| `BTP_CLIENT_ID` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | OAuth2 Authentifizierung an SAP CPI |
| `BTP_CLIENT_SECRET` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | OAuth2 Authentifizierung an SAP CPI |
| `BTP_TOKEN_URL` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | Token-Endpunkt des BTP Subaccounts |
| `BTP_RUNTIME_URL` | `.streamlit/secrets.toml` (gitignored) | Streamlit Cloud Secrets Vault | HTTPS-Inbound-Endpunkt des Batch Receivers |

- **Kein Secret-Leak im Git:** Das `.streamlit/`-Verzeichnis mit lokalen Secrets ist in `.gitignore` eingetragen.
- **Passwortschranke:** Die Streamlit-App prüft bei geschützten Aktionen ein Sitzungspasswort. Ohne Freischaltung können weder LLM-Token-Kontingente noch SAP BTP-Testläufe verbraucht werden.

---

## 5. In-Memory Grounding Engine & LLM-Resilienz

1. **Ultraschneller In-Memory Wissenszugriff:**
   - Beim ersten Aufruf parst die App alle Markdown-Dateien im Verzeichnis `knowledge/` und lädt die vorab berechnete Graph-Struktur `graph/knowledge-graph.json`.
   - Mittels `@st.cache_resource` bleibt dieser Zustand über Benutzerinteraktionen hinweg resident im Speicher (<50 MB RAM).
2. **Dynamisches Prompt-Grounding:**
   - Nutzerfragen werden mit dem Wissensbestand abgeglichen (Keyword- und Tag-Matching).
   - Die Originaltexte relevanter OKF-Dokumente und ADRs werden verbatim in den System-Prompt des Google Gemini Modells injiziert.
   - Der Agent antwortet mit BPMN 2.0 Method & Style Nomenklatur, generiert dynamische Mermaid-Diagramme und referenziert GitHub-Dateien.
3. **Multi-Tier Fallback Kette:**
   Bei Überlastung oder temporären Störungen der externen KI-Dienste schützt eine kaskadierende Fallback-Kette die Benutzererfahrung:
   - **Primär:** `gemini-3.6-flash` (Neueste Argumentationslogik & hohe Geschwindigkeit)
   - **Sekundär:** `gemini-2.0-flash` (Hohe Verfügbarkeit bei Lastspitzen)
   - **Tertiär:** `gemini-1.5-flash` (Bewährtes Fallback-Modell)
   - **Quartär:** Lokaler deterministischer Auszug der relevantesten OKF-Konzepte ohne LLM.

---

## 6. Architektur-Vergleich

| Kriterium | Traditioneller Docker/K8s/Kyma Stack | Google Cloud Run / AWS ECS | Streamlit Community Cloud & GitHub GitOps (Gewählt) |
| :--- | :--- | :--- | :--- |
| **Infrastrukturkosten** | Hoch (VMs, Cluster, Egress) | Gering (Pay-per-Use), aber Abrechnungskonto nötig | **0,00 € (Zero-Cost Free Tier)** |
| **Build- & Deploy-Pipeline** | Komplex (Dockerfile, GitHub Actions, Registry) | Mittel (Container-Build, Image-Push) | **Keine (Zero-Docker, Push-to-Deploy)** |
| **Wartungsaufwand** | OS-, Image-, Patch-Management | Container-Baseimage-Updates | **Null (Verwaltete Python-Plattform)** |
| **SAP BTP CORS-Kompatibilität**| Ja (Server-Side) | Ja (Server-Side) | **Ja (Vollständige Server-Side Bridge)** |
| **GitOps Integration** | Erfordert CI/CD Pipeline Konfiguration | Erfordert CI/CD Pipeline Konfiguration | **Nativ per Webhook integriert** |
