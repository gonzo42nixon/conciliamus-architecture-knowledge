---
id: presentation-and-ui/pecha_kucha_konzept
type: Presentation Concept
title: "Pecha Kucha 20x20 Konzept & Foliensprechertexte"
description: "Vollständiges Drehbuch, Struktur und 20-Sekunden-Sprechertexte der 20 Folien umfassenden Pecha Kucha Architekturpräsentation."
resource: btp://conciliamus/presentation/pecha-kucha-script
tags: [presentation, pecha-kucha, 20x20, concept, script, speech]
status: verified
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-05T21:00:00Z"
relations:
  - { type: implementedBy, target: /presentation-and-ui/pecha-kucha-20x20.md }
  - { type: refersTo, target: /decisions/adr-001-dual-iflow-decoupling.md }
  - { type: refersTo, target: /decisions/adr-002-zero-trust-btp-security.md }
  - { type: refersTo, target: /decisions/adr-003-end-to-end-correlation-mpl.md }
  - { type: refersTo, target: /decisions/adr-004-bpmn-method-and-style.md }
  - { type: refersTo, target: /decisions/adr-005-process-direct.md }
  - { type: refersTo, target: /decisions/adr-006-idempotent-existence-check.md }
  - { type: refersTo, target: /decisions/adr-007-two-legged-csrf-handshake.md }
  - { type: refersTo, target: /decisions/adr-008-data-store-dlq.md }
  - { type: refersTo, target: /decisions/adr-009-single-viewport-fiori.md }
  - { type: refersTo, target: /decisions/adr-010-streamlit-cloud-agent-deployment.md }
  - { type: refersTo, target: /decisions/adr-011-google-okf-knowledge-graph.md }
---

# Pecha-Kucha-Präsentation: MDM Business Partner Synchronisation
## SAP Cloud Integration • Dual-iFlow Architektur • BPMN 2.0 Method & Style
**Referent:** Dieter Rüffler (Dipl.-Inform. TU Berlin, ISTQB CTFL, ITIL V2, Certified AI Engineer)  
**Zielgruppe:** Markus Engelmann & Team *Plattform & Integration*, Conciliamus GmbH (Johannesstift Diakonie gAG)  
**Format:** Pecha Kucha (20 Folien × 20 Sekunden = 6 Minuten 40 Sekunden)  
**Datum:** Mittwoch, 09.09.2026, 14:30 Uhr  
**Sprachregelung:** Kollegiales Team-Duzen („Du / Ihr / Wir“)  

---

## Übersicht der 20 Folien

| # | Phase | Folientitel | Kernbotschaft / Visual |
|---|---|---|---|
| **01** | Intro | **Start & Willkommen** | Praxisaufgabe Conciliamus GmbH: Dieter Rüffler löst Business Partner Synchronisation mit SAP BTP Integration Suite |
| **02** | Intro | **Profil & Werte** | TU Berlin, CPI, PO 7.50, AWS, ISTQB, ITIL V2, Make.com, AI Engineer – Solide Ingenieurskunst & Cloud-Agilität |
| **03** | Kontext | **Conciliamus & Johannesstift Diakonie** | Resiliente Stammdaten für das Rückgrat der Gesundheitswirtschaft |
| **04** | Challenge | **Die Integrationsaufgabe** | MDM-Massenbatch trifft auf transaktionales S/4HANA OData (CVI-Transition) |
| **05** | Architektur | **ADR-001: Das Dual-iFlow-Paradigma** | Architektur-Governance nach Michael Nygard (Docs-as-Code); strikte Trennung von Ingest & Fachlogik |
| **06** | Security | **ADR-002: Zero-Trust & BTP Cloud Security** | BTP als Managed PaaS, OAuth2 Client Credentials, TLS 1.3, Vault statt Basic Auth |
| **07** | Governance | **ADR-003: End-to-End Nachvollziehbarkeit** | Globale Correlation-ID & Custom Header Properties im Message Processing Log (MPL) |
| **08** | Deep Dive | **ADR-004: iFlow 1 – Ingest & Streaming Splitter** | BPMN 2.0 Inbound-Pipeline (Bruce Silver): Sofortiges HTTP 202, flaches RAM-Profil via Streaming Splitter |
| **09** | Deep Dive | **ADR-005: iFlow 2 – Item Processor & ProcessDirect** | `IFL_MDM_BP_Item_Processor` via ProcessDirect: Latenzfreier In-Memory Bus ohne JMS-Lizenzkosten |
| **10** | Logik | **ADR-006: Idempotenz & Existenzprüfung** | OData GET `A_BusinessPartner`: Duplikatschutz durch semantische Schlüsselprüfung (POST vs. PATCH) |
| **11** | Protokoll | **ADR-007: Der CSRF- & Session-Handshake** | Two-Legged OData Call: Token & Cookie-Handling für schreibende Operationen ohne Session-Abbrüche |
| **12** | Resilienz | **ADR-008: Dual-Channel Fehlerbehandlung & DLQ** | Fachlicher Fehler (Audit Log) vs. Technischer Ausfall (Data Store `BP_FAILED_QUEUE` Replay) |
| **13** | Qualität | **ISTQB-getriebenes Testing** | Strukturierte 10er-Testsuite des Conciliamus-Kollegen: 3x PATCH, 7x POST, Grenzwertanalyse & Äquivalenzklassen |
| **14** | Beweis | **Live auf SAP BTP verifiziert** | Erfolgreicher End-to-End Durchlauf mit HTTP 200 OK am 04.09.2026 auf dem produktiven BTP-Tenant (1,42s) |
| **15** | Tooling | **ADR-009: Der Fiori Horizon Test-Runner** | Single-Viewport Web-App im authentischen SAP Fiori Horizon Look ohne äußeres Scrollen |
| **16** | GitOps | **ADR-010: Serverless GitOps & BTP CORS-Bypass** | Zero-Docker & Zero-Cost via GitHub & Streamlit Community Cloud (20s CI/CD) |
| **17** | Innovation | **ADR-011: Generative AI & Knowledge Graph** | Google OKF v0.2 (33 Knoten, 82 Kanten) & Gemini 3.6 Flash: Das Digital Brain des Architekten |
| **18** | Value | **Mehrwert für Conciliamus & Dieter Rüffler** | Drei Säulen: Integrationserfahrung, Test- & Betriebsmethodik sowie Innovationskraft mit GenAI |
| **19** | Digest | **Das Enterprise Acronym Digest** | 200 Meilensteine, Frameworks & Standards von 825 bis AGI 2030 (Scrollbar-frei, 4-Wege-Filterung) |
| **20** | Ausblick | **Diskussion & Live-Demo** | Punktlandung bei 06:40: Übergang in die Fragerunde und den gemeinsamen Live-Testlauf |

---

### Folie 01: Start & Willkommen
* **Visuelles Motiv:** Zweigeteiltes Dashboard: Links Hero-Card mit Praxisaufgabe und Conciliamus-Branding, rechts Steckbrief mit Referent Dieter Rüffler, Zielgruppe Markus Engelmann & Team sowie 6:40 Pecha-Kucha-Timer.
* **Kernbotschaft:** Herzliches Willkommen zum Architekturvortrag über die synchrone und asynchrone Business Partner Anbindung auf SAP BTP.
* **Sprechertext (20 Sek. / 49 Wörter):**
> „Hallo Markus, hallo Team Conciliamus! Mein Name ist Dieter Rüffler. Diese Präsentation dokumentiert meine Lösungsarchitektur zu eurer Praxisaufgabe: die synchrone und asynchrone Anbindung von Business Partnern an SAP S/4HANA auf der BTP. In sechs Minuten und vierzig Sekunden zeige ich euch Architektur, Mapping und Ausfallsicherheit – fundiert und praxiserprobt.“

---

### Folie 02: Profil, Ingenieurskunst & Zertifizierungen
* **Visuelles Motiv:** 8-Kachel-Tableau (2×4 Grid): 1. Diplom-Urkunde TU Berlin, 2. SAP CPI Specialist, 3. SAP PO 7.50 Specialist, 4. AWS Certified Cloud Practitioner, 5. ISTQB Certified Tester, 6. ITIL V2 TÜV SÜD Cert, 7. Make Foundation Automation, 8. Certified AI Engineer mit Direktverlinkung auf Credly und Zeugnisse.
* **Kernbotschaft:** Solide theoretische Informatik-Grundlagen gepaart mit offiziell verifizierten Zertifizierungen in Cloud Integration, Process Orchestration, Qualitätsmanagement und generativer KI.
* **Sprechertext (20 Sek. / 46 Wörter):**
> „Als Diplom-Informatiker der TU Berlin verbinde ich fundierte theoretische Grundlagen mit moderner Cloud-Praxis. Mein Profil umfasst offizielle Zertifizierungen in SAP Cloud Integration, Process Orchestration, AWS und ISTQB, ergänzt durch ITIL-Servicemanagement, Make.com-Automatisierung und modernste Qualifikation als AI Engineer – höchste Qualität und technologische Zukunftssicherheit auf einen Blick.“

---

### Folie 03: Conciliamus & Johannesstift Diakonie
* **Visuelles Motiv:** Logo Johannesstift Diakonie gAG & Conciliamus GmbH, Organigramm Plattform & Integration, Bild eines modernen Klinikums.
* **Kernbotschaft:** IT in der Gesundheits- und Sozialwirtschaft verzeiht keine Datenfehler oder Systemstillstände: Resilienz sichert operative Versorgung.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Conciliamus bildet das technologische Rückgrat für Krankenhäuser, Pflege- und Sozialeinrichtungen der Johannesstift Diakonie. Hier geht es nicht um beliebige Datensätze – hinter jedem Geschäftspartner stehen Lieferanten lebenswichtiger Medizingüter oder Dienstleister. Ausfallzeiten oder inkonsistente Stammdaten haben direkte operative Auswirkungen. Deshalb steht bei mir Ausfallsicherheit und Nachvollziehbarkeit an allererster Stelle.“

---

### Folie 04: Die Integrationsaufgabe
* **Visuelles Motiv:** Quellsystem JSD-MDM ([Mitarbeitenden-Login](https://www.johannesstift-diakonie.de/mitarbeitenden-login), JSON-Batch mit 10 Geschäftspartnern) ➔ Barriere ➔ Zielsystem SAP S/4HANA OData API. Fußnote: Zusatz-Challenge bei R/3-Transition (Harmonisierung getrennter Debitoren & Kreditoren zum unifizierten Business Partner) via [Customer-Vendor-Integration (CVI)](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/74b0b157c81944ffaac6ebc07245b9dc/25b46c8241fd4852bf7876d87bed8fd0.html).
* **Kernbotschaft:** Massen-Batches dürfen das transaktionale ERP-System niemals überlasten oder blockieren: Entkopplung schützt S/4HANA.
* **Sprechertext (20 Sek. / 47 Wörter):**
> „Die Ausgangslage: Unser MDM-System liefert Geschäftspartner gesammelt als JSON-Batch an. Das Zielsystem, ein SAP S/4HANA Cloud, verlangt jedoch granulare OData-Aufrufe. Wie verhindern wir, dass ein einziger fehlerhafter Datensatz den gesamten Batch abbricht? Und wie schützen wir das ERP vor Lastspitzen? Die Antwort liegt in einer entkoppelten Integrationsarchitektur.“

---

### Folie 05: ADR-001: Das Dual-iFlow-Paradigma
* **Visuelles Motiv:** Infobox zur ADR-Methodik (*Architecture Decision Records nach Michael Nygard 2011 / ThoughtWorks Radar „Adopt“; Docs-as-Code im Git-Repo statt TOGAF/LeanIX-Ordnern*). Gegenüberstellung: Monolithischer Anti-Pattern-Flow ❌ vs. Dual-iFlow Entkopplung nach ADR-001 (Ingest-Flow mit sofortigem HTTP 202 ➔ ProcessDirect In-Memory Bus ➔ Item-Processor mit atomarer Fehlerisolation) ✅.
* **Kernbotschaft:** Single Responsibility & Fehlerisolation: Strikte Trennung von Netzwerk-Ingest und fachlicher Verarbeitung.
* **Sprechertext (20 Sek. / 43 Wörter):**
> „Gute Architektur darf nicht in schwerfälligen TOGAF-Ordnern oder vergessenen Confluence-Wikis verstauben. Ich nutze Architecture Decision Records – ADRs nach Michael Nygard, als versioniertes Docs-as-Code direkt im Git-Repository. Unsere erste fundamentale Weichenstellung ist ADR-001: Das Dual-iFlow-Paradigma zur strikten Entkopplung von Ingest und fachlicher Fehlerisolation.“

---

### Folie 06: ADR-002: Zero-Trust & BTP Cloud Security
* **Visuelles Motiv:** Großflächiger Screenshot des realen SAP BTP Cockpits (Unterkonto *trial*: Instanzen und Abonnements für *Integration Suite* und *SAP Process Integration*), ergänzt durch die Sicherheitsmerkmale nach ADR-002 (BTP als Managed PaaS, OAuth2 Client Credentials, TLS 1.3, XSUAA Service Keys, Security Material Vault statt Basic Auth).
* **Kernbotschaft:** Sicherheit ist kein nachträgliches Feature, sondern integraler Bestandteil der Plattformarchitektur.
* **Sprechertext (20 Sek. / 42 Wörter):**
> „Nach ADR-002 ist Sicherheit kein nachträgliches Feature. Die BTP fungiert als Managed PaaS, und der Inbound-Kanal ist über OAuth2 Client Credentials geschützt – Basic Authentication ist strikt deaktiviert. Alle Tokens und Passwörter liegen verschlüsselt im Security Material Vault, transportiert über TLS 1.3.“

---

### Folie 07: ADR-003: End-to-End Nachvollziehbarkeit & Governance
* **Visuelles Motiv:** Message Processing Log (MPL) Architektur: Globale SAP-Correlation-ID, Custom Header Properties für `MDM_BP_ID` und `S4_BP_ID` nach ADR-003.
* **Kernbotschaft:** Lückenlose Rückverfolgbarkeit im Supportfall: Schnelles Auffinden fehlerhafter Datensätze ohne zeitraubende Payload-Analysen.
* **Sprechertext (20 Sek. / 42 Wörter):**
> „Nach ADR-003 zählt im Störfall jede Minute. Unser Ingest-Flow generiert eine globale SAP-Correlation-ID, die durch alle Verarbeitungsschritte propagiert wird. Über Custom Header Properties im Message Processing Log können Administratoren jeden Partner sofort nach seiner MDM-ID oder S/4-Nummer filtern – ohne zeitraubende Payload-Analysen.“

---

### Folie 08: ADR-004: iFlow 1 – Ingest & Streaming Splitter
* **Visuelles Motiv:** Reales iFlow-Diagramm (`IFL_MDM_BP_Batch_Receiver`, 1535x807) mit BPMN 2.0 Ingest, selbstdokumentierender Bruce Silver Nomenklatur, sofortigem HTTP 202 Quittieren und Iterating Streaming Splitter mit flachem Speicherprofil nach ADR-004.
* **Kernbotschaft:** Schonen der BTP-Ressourcen: Konstante Speichernutzung auch bei sehr großen Inbound-Payloads.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Hier seht ihr unseren Ingest-Flow nach ADR-004 mit selbstdokumentierender Bruce Silver Nomenklatur. Er nimmt den JSON-Batch entgegen, validiert den Header und quittiert sofort mit HTTP 202 Accepted. Anschließend zerlegt ein Streaming Iterating Splitter den Batch speicherschonend – so bleibt der RAM-Verbrauch des BTP-Tenants selbst bei Lastspitzen völlig flach.“

---

### Folie 09: ADR-005: iFlow 2 – Item Processor & ProcessDirect
* **Visuelles Motiv:** Reales iFlow-Diagramm (`IFL_MDM_BP_Item_Processor`, 3070x1200) angebunden über ProcessDirect In-Memory Bus. Latenzfreier Datenaustausch ohne Message Queue Lizenzkosten nach ADR-005.
* **Kernbotschaft:** Kosteneffizienz und maximale Geschwindigkeit durch native In-Memory Adapter.
* **Sprechertext (20 Sek. / 40 Wörter):**
> „Der zweite iFlow, IFL_MDM_BP_Item_Processor, steuert die Interaktion mit SAP S/4HANA. Er empfängt die vereinzelten Nachrichten über den ProcessDirect-Adapter – latenzfrei im Speicher, ohne teure JMS-Queue-Lizenzen nach ADR-005. Jeder Datensatz wird isoliert transformiert, sodass ein fehlerhafter Partner niemals gesunde Datensätze beeinträchtigt.“

---

### Folie 10: ADR-006: Idempotenz & Existenzprüfung
* **Visuelles Motiv:** Entscheidungsmatrix für idempotente Schreibvorgänge nach ADR-006: OData GET Abfrage auf `SearchTerm1` (`$filter=SearchTerm1 eq 'MDM_ID'`). Verzweigung: 0 Treffer ➔ POST (Create); 1 Treffer ➔ PATCH (Update).
* **Kernbotschaft:** Mathematische Idempotenz schützt vor kostspieligen Dubletten im ERP-System.
* **Sprechertext (20 Sek. / 44 Wörter):**
> „Nach ADR-006 müssen Schnittstellen mathematisch idempotent sein: Wiederholte Batches dürfen keine Dubletten erzeugen. Vor jedem Schreibzugriff prüfen wir über einen OData-GET-Call auf SearchTerm1, ob der Partner existiert. Bei null Treffern erfolgt ein POST zur Neuanlage, bei genau einem Treffer ein gezielter PATCH zur Aktualisierung.“

---

### Folie 11: ADR-007: Der Two-Legged CSRF- & Cookie-Handshake
* **Visuelles Motiv:** Sequenzdiagramm des zweistufigen OData-Handshakes nach ADR-007: Step 1 HEAD-Call mit `X-CSRF-Token: Fetch` ➔ Speichern von Token und Session-Cookie (`MYSAPSSO2` / `SAP_SESSIONID`) ➔ Step 2 Schreib-Call mit validem Token und Cookie.
* **Kernbotschaft:** Robuste Protokollbehandlung verhindert Session-Abbrüche bei schreibenden OData-Aufrufen.
* **Sprechertext (20 Sek. / 42 Wörter):**
> „Nach ADR-007 scheitern schreibende OData-Aufrufe oft an abgelaufenen CSRF-Tokens. In unserem Item Processor sichert ein robuster zweistufiger Handshake die Transaktion: Zuerst wird das X-CSRF-Token samt Session-Cookie abgerufen und in Exchange Properties gesichert, bevor der eigentliche Schreib-Call feuert – stabil und absolut fehlertolerant.“

---

### Folie 12: ADR-008: Dual-Channel Fehlerbehandlung & DLQ
* **Visuelles Motiv:** Verzweigung der Fehlerpfade nach ADR-008: Fachlicher Validierungsfehler ➔ Sofortige Fehlerquittierung & Audit-Log (kein Retry). Technischer Backend-Ausfall ➔ Persistierung in BTP Data Store Queue (`BP_FAILED_QUEUE`) mit automatischem Replay.
* **Kernbotschaft:** Differenzierte Fehlerbehandlung: Fachliche Fehler nicht unnötig wiederholen, technische Ausfälle resilient auffangen.
* **Sprechertext (20 Sek. / 45 Wörter):**
> „Resilienz bedeutet Differenzierung: Ein fachlicher Fehler darf nicht zu Endlos-Retries führen, sondern wird sofort gemeldet. Bricht jedoch das S/4HANA-Backend weg, greift unser technischer Fehlerpfad nach ADR-008: Die Nachricht wird in einer BTP Data Store Queue gesichert und automatisch wiederholt, sobald das ERP wieder online ist.“

---

### Folie 13: ISTQB-getriebenes Testing
* **Visuelles Motiv:** Matrix der 10 Testdatensätze aus der Testsuite des Conciliamus-Kollegen: 3x PATCH (Bestandskunden), 7x POST (Neukunden), Grenzwert-Szenarien (Sonderzeichen, max. Feldlängen). Badge: 10/10 Bestanden (100%).
* **Kernbotschaft:** Systematische Verifikation der vom Conciliamus-Kollegen bereitgestellten Testsuite nach ISTQB-Methodik.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Als ISTQB-zertifizierter Tester verlasse ich mich niemals auf das Prinzip Hoffnung. Für die Verifikation nutze ich die Testsuite aus zehn differenzierten Geschäftspartnern, die mir ein Conciliamus-Kollege bereitgestellt hat: Drei bestehende Datensätze für den PATCH-Zweig, sieben neue für den POST-Zweig sowie Grenzwerte mit Sonderzeichen. So stellen wir gemeinsam reproduzierbare Qualität sicher.“

---

### Folie 14: Live auf SAP BTP verifiziert (HTTP 200)
* **Visuelles Motiv:** Screenshot des produktiven BTP Tenants vom 04.09.2026: Status `COMPLETED`, Verarbeitungszeit 1,42 Sekunden, 10 von 10 Nachrichten grün prozessiert, sauberes Message Processing Log.
* **Kernbotschaft:** Theorie ist gut – funktionierender Live-Betrieb auf dem echten Tenant ist der unumstößliche Beweis.
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Papier ist geduldig – der laufende Tenant lügt nicht. Am 4. September habe ich die gesamte Pipeline end-to-end auf dem echten BTP-Tenant getestet. Zehn Datensätze in 1,42 Sekunden verarbeitet, Status grün, Message Processing Log sauber. Alles, worüber ich heute spreche, existiert nicht nur in PowerPoint, sondern läuft live in der Cloud.“

---

### Folie 15: ADR-009: Der Fiori Horizon Test-Runner
* **Visuelles Motiv:** Reale Web-App im authentischen SAP Fiori Horizon Look nach ADR-009: Großflächiger Screenshot der Testrunner-Workbench (`orcai-54321.web.app/test-runner.html`) mit Direkt-Link zur Live-App, 10 differenzierten Testfällen (3x PATCH, 7x POST), aufklappbaren JSON-Payload-Pills und Live BTP-Dispatch ohne äußeres Scrollen.
* **Kernbotschaft:** Transparenz und Bedienbarkeit für Entwickler und Fachbereich durch eine leichtgewichtige Test-App.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Um Integration für alle Beteiligten greifbar zu machen, habe ich eine eigenständige Test-Runner Web-App im SAP Fiori Horizon Look nach ADR-009 gebaut. Ohne schwere Framework-Altlasten, komplett responsiv und auf einen einzigen Bildschirm optimiert. Jeder Datensatz lässt sich per Klick live gegen die BTP feuern – inklusive vollständiger JSON-Payload-Transparenz.“

---

### Folie 16: ADR-010: Serverless GitOps & BTP CORS-Bypass
* **Visuelles Motiv:** Zweiteiliges Lösungs-Tableau nach ADR-010: Links automatisierte GitOps-Pipeline (`git push origin main` ➔ Streamlit Community Cloud in 20s, Zero-Docker, Zero-Cost); rechts SAP BTP CORS-Bypass (Browser-Preflight-Blockade HTTP 401 ❌ vs. serverseitige Python-Runtime HTTP 200/202 ✅).
* **Kernbotschaft:** Schlanke Bereitstellung ohne Infrastrukturkosten und zuverlässiges Umgehen von Browser-CORS-Beschränkungen.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Mit ADR-010 lösen wir zwei zentrale Herausforderungen: Bereitstellungsaufwand und das berüchtigte SAP BTP CORS-Dilemma. Statt teurer Kubernetes-Cluster betreiben wir unseren Architecture Advisor serverlos via Streamlit Community Cloud direkt aus GitHub. Jeder Git-Push ist in zwanzig Sekunden weltweit live – und serverseitige Python-Calls umgehen die Browser-CORS-Blockade bei BTP-Aufrufen elegant und sicher.“

---

### Folie 17: ADR-011: Generative AI & Knowledge Graph
* **Visuelles Motiv:** Google Open Knowledge Format v0.2 Knowledge Graph (33 Konzepte, 82 Kanten), gekoppelt an Gemini 3.6 Flash. Quellenbasierte Architekturberatung ohne Halluzinationen nach ADR-011.
* **Kernbotschaft:** Zukunftsfähiges Architektur-Knowledge-Management durch kanonische Wissensgraphen und Grounded Generative AI.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Als zertifizierter AI Engineer denke ich Integration mit euch weiter. In ADR-011 definieren wir das Google Open Knowledge Format als kanonischen Standard: 33 Konzepte und 82 Kanten verknüpfen Architektur, Tests und ADRs. Unser KI-Advisor auf Basis von Gemini 3.6 Flash beantwortet jede eurer Fragen quellenbasiert und ohne Halluzinationen.“

---

### Folie 18: Mehrwert für Conciliamus & Dieter Rüffler
* **Visuelles Motiv:** Drei Säulen des Mehrwerts: 1. Sofortige Entlastung bei der BTP- & S/4-Migration durch 20 Jahre Integrationserfahrung; 2. Höchste Qualität durch ISTQB- & ITIL-Methodik; 3. Innovationsschub durch pragmatischen GenAI-Einsatz.
* **Kernbotschaft:** Ganzheitliche Verstärkung für das Plattform- und Integrationsteam der Conciliamus GmbH.
* **Sprechertext (20 Sek. / 46 Wörter):**
> „Was bringe ich für Conciliamus mit? Erstens: Sofortige Entlastung bei der BTP- und S/4HANA-Migration durch zwanzig Jahre Schnittstellenerfahrung. Zweitens: Höchste Qualität durch ISTQB- und ITIL-Methodik. Und drittens: Einen Innovationsschub durch den gezielten Einsatz von generativer KI. Ich freue mich darauf, dieses Wissen in euer Team einzubringen.“

---

### Folie 19: Das Enterprise Acronym Digest (200 Meilensteine, Frameworks & Standards)
* **Visuelles Motiv:** Symmetrisches 20×10-Tableau (20 Zeilen à 10 Spalten = exakt 200 Pills, passend zur Pecha-Kucha-Dramaturgie aus 20 Folien, vollständig scrollbar-frei mit 0px Layout-Jumping): Fester 128px Live-Inspector oben mit Gegenüberstellung *„SAP-Sprech vs. Informatik-Realität“*, dynamischer Impact-Badge und Architektur-Layer-Badge. 4-Wege-Steuerung (Chronologisch, Alphabetisch, Weltweiter Impact, 7 Architektur-Layer).
* **Kernbotschaft:** Tiefes technologisches Verständnis und historische Einordnung aller relevanten Enterprise- und KI-Standards.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „In zwanzig Jahren SAP-Integration habe ich gelernt: SAP benennt fundamentale Informatik gern mit eigenen Akronymen um. Dieses Digest entschlüsselt zweihundert Meilensteine – von der Industrialisierung über Bletchley Park und Ethernet bis zu NIS-2 und AGI 2030. Sortiert nach Zeitstrahl, Alphabet, weltweitem Impact oder Architektur-Stack. Fahrt einfach mit der Maus darüber!“

---

### Folie 20: Diskussion & Live-Demo
* **Visuelles Motiv:** Grand Finale Cockpit (06:40 Punktlandung): Klickbare Buttons zum Fiori Test-Runner und den Sprechertexten, Einladung an Markus Engelmann & Team Conciliamus zum Fachgespräch.
* **Kernbotschaft:** Punktgenaue Landung nach exakt 6 Minuten 40 Sekunden – nahtloser Übergang in Fragen und Live-Demo.
* **Sprechertext (20 Sek. / 45 Wörter):**
> „Genau sechs Minuten und vierzig Sekunden: Punktlandung! Vielen Dank für eure Aufmerksamkeit. Lasst uns jetzt keine weiteren Folien ansehen, sondern direkt live in die BTP-Integration Suite und unsere Fiori-Test-App springen. Markus, liebes Team: Die Bühne gehört euren Fragen – und ich drücke auf ‚Testsuite starten‘!“

---

## Präsentationssteuerung & Full-Screen Modus
Die Web-Präsentation (`pecha-kucha.html`) bietet eine professionelle Bühnen- und Referentensteuerung:
* **Full-Screen Modus (Vollbild):**
  * Umschalten über den **Vollbild-Button** in der Fiori-Header-Leiste oder der Fußleiste.
  * Tastatur-Shortcut: **`F`** für Vollbild aktivieren/deaktivieren (oder **`Esc`** zum Verlassen).
  * Optimierte Bühnen-Skalierung (`#slideCard` nutzt die volle Bildschirmbreite, saubere 16:9 Adaption).
* **Referenten-Notizen (`N`):** Ein- und Ausblenden des Sprechertext-Panels mit 20-Sekunden-Wortzählung.
* **Folienübersicht (`G`):** Modaler 20-Karten-Überblick zum direkten Anspringen beliebiger Folien.
* **Navigation:** `Space` (Pause/Fortsetzen), `←` / `→` (Vor/Zurück), `R` (Restart von Folie 01).
* **Geschwindigkeitskontrolle:** 20 Sekunden (Standard), 15s (Schnelllauf), 30s (Übung), Manuell.

---

## Technische Referenzen & Begleitdokumente
* **Live-App Testrunner:** [https://orcai-54321.web.app/test-runner.html](https://orcai-54321.web.app/test-runner.html)
* **Live Pecha Kucha URL:** [https://orcai-54321.web.app/pecha-kucha.html](https://orcai-54321.web.app/pecha-kucha.html)
* **SAP BTP Cockpit:** [Trial Global Account & Subaccount Section](https://account.hanatrial.ondemand.com/trial/#/globalaccount/34eec884-0c14-4a9d-a509-55a912f83aee/accountModel&//?section=SubaccountsSection&view=TilesView)
* **SAP Integration Suite Tenant:** [Tenant b9c123f3trial Shell Home](https://b9c123f3trial.integrationsuite-trial01.cfapps.us10-001.hana.ondemand.com/shell/home)
* **GitHub Repository:** [gonzo42nixon/Conciliamus](https://github.com/gonzo42nixon/Conciliamus)
* **Live iFlow Batch Receiver:** [Google Photos Screenshot](https://photos.app.goo.gl/mfS9oN94KfUXJK6bA)
* **Live iFlow Item Processor:** [Google Photos Screenshot](https://photos.app.goo.gl/y8m8vH3BDCQG7whU8)
* **Bruce Silver Methodik:** [BPMN Method & Style](https://www.methodandstyle.com/books/bpmn-method-and-style/)
* **Rheinwerk Fachliteratur:** [KI mit SAP](https://www.rheinwerk-verlag.de/sap/ki-mit-sap/)
