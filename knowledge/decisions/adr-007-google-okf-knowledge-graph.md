---
id: decisions/adr-007-google-okf-knowledge-graph
type: Decision Record
title: "ADR-007: Google Open Knowledge Format (OKF v0.2) & Grounded AI Architecture Advisor"
description: Einführung des Google Open Knowledge Format (OKF v0.2) als maschinenlesbarer, graphbasierter Architektur-Standard für quellenbasierte KI-Architekturberatung mit Google Gemini.
resource: btp://conciliamus/decisions/ADR-007
tags: [adr, architecture-decision, google-okf, open-knowledge-format, knowledge-graph, gemini, ai-advisor, grounding, zero-hallucination]
status: accepted
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T22:30:00Z"
relations:
  - { type: implements, target: /presentation-and-ui/streamlit-chat-advisor.md }
  - { type: dependsOn, target: /architecture/agent-deployment-and-gitops.md }
sources:
  - id: okf-spec
    resource: https://github.com/gonzo42nixon/conciliamus-architecture-knowledge
    title: Google Open Knowledge Format Specification & Knowledge Repository
    author: "Dieter Rüffler"
---

# ADR-007: Google Open Knowledge Format (OKF v0.2) & Grounded AI Architecture Advisor

## Status
Akzeptiert (Accepted)

## Kontext
In traditionellen Enterprise-Integrationsprojekten verstaubt Architekturwissen häufig in isolierten PDF-Konzepten, Word-Dokumenten oder schwer auffindbaren Confluence-Wikis. Daraus resultieren gravierende Probleme:
1. **Wissenserosion & Veraltung:** Dokumente werden nach dem Go-Live selten gepflegt und weichen rasch vom tatsächlichen BTP-Laufzeitverhalten ab.
2. **Fehlende Maschinenlesbarkeit:** Herkömmliche Fließtexte können von automatisierten Validierungswerkzeugen (CI/CD) nicht geprüft werden.
3. **Halluzinationsgefahr bei KI-Einsatz:** Werden Large Language Models (LLMs) ungestützt auf lose Dokumente losgelassen, erfinden sie Parameter, Endpunkte oder iFlow-Verhalten ("Halluzinationen").
4. **Mangelnde Traceability:** Zusammenhänge zwischen Anforderungen, Architektur-Entscheidungen (ADRs), Datenkontrakten und Testnachweisen sind nicht formal verknüpft.

## Entscheidung
Wir haben entschieden, die gesamte Architektur der Conciliamus Business Partner Synchronisation nach dem **Google Open Knowledge Format (OKF v0.2)** zu modellieren und als Grounding-Layer für den **Conciliamus AI Architecture Advisor** bereitzustellen:

1. **Strukturierte OKF-Ontologie:**
   - Jede Wissenseinheit (Architekturkonzepte, iFlow-Spezifikationen, ADRs, Datenkontrakte, Testnachweise) liegt als eigenständige Markdown-Datei mit obligatorischem YAML-Frontmatter (`id`, `type`, `title`, `description`, `tags`) vor.
2. **Explizite Knowledge-Graph-Kanten:**
   - Relationen zwischen Konzepten werden im Frontmatter deklarativ typisiert (`contains`, `implements`, `routesTo`, `verifies`, `dependsOn`, `handlesError`).
   - Daraus wird automatisch ein vollständiger, maschinenlesbarer Graph generiert (`graph/knowledge-graph.json` und `graph/architecture-graph.mmd` mit 28 Knoten und 72 Kanten).
3. **Formale Schema-Validierung:**
   - Ein Python-Validierungsframework (`tooling/validate_okf.py`) prüft alle Dokumente gegen formale JSON-Schemas (`schemas/okf-concept.schema.json`) und sichert Link-Integrität in CI/CD ab.
4. **Quellengestütztes LLM-Grounding (Zero-Hallucination):**
   - Der KI-Architekturberater nutzt **Google Gemini 3.6 Flash** (via `google-genai` SDK).
   - Der Prompt erzwingt striktes Grounding: Antworten basieren ausschließlich auf dem geladenen OKF-Knowledge-Bundle und enthalten zwingende, klickbare Quellenangaben.
5. **Standardisierte Agenten-Schnittstelle:**
   - Über `manifest/agent.yaml` und OpenAPI 3.1 (`api/conciliamus-architecture.openapi.yaml`) wird die Wissensbasis direkt für autonome KI-Coding- und Integrations-Agenten aufrufbar gemacht.

## Konsequenzen
- **Positiv:**
  - **Single Source of Truth:** Architekturwissen, Schnittstellenkontrakte und Prüfnachweise liegen konsolidiert im Git-Repository vor.
  - **Zero-Hallucination Consulting:** Der AI Advisor liefert auditierbare, exakte Antworten mit Fundstellen auf Zeilenebene.
  - **Graph-Traversierung:** Abhängigkeiten und Fehlerkaskaden können algorithmisch über Kanten analysiert werden.
  - **Zukunftssicherheit:** Nahtlose Integration in künftige Multi-Agenten-Systeme und Enterprise-Workflows.
- **Negativ / Trade-offs:**
  - **Disziplin bei Änderungen:** Neue oder modifizierte Konzepte müssen den OKF-Frontmatter-Konventionen entsprechen und die Validierungsskripte bestehen.
