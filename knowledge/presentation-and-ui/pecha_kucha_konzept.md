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
  at: "2026-09-04T22:00:00Z"
relations:
  - { type: implementedBy, target: /presentation-and-ui/pecha-kucha-20x20.md }
---

# Pecha-Kucha-Präsentation: MDM Business Partner Synchronisation
## SAP Cloud Integration • Dual-iFlow Architektur • BPMN 2.0 Method & Style
**Referent:** Dieter Rüffler (Dipl.-Inform. TU Berlin, ISTQB CTFL, ITIL V2)  
**Zielgruppe:** Markus Engelmann & Team *Plattform & Integration*, Conciliamus GmbH (Johannesstift Diakonie gAG)  
**Format:** Pecha Kucha (20 Folien × 20 Sekunden = 6 Minuten 40 Sekunden)  
**Datum:** Mittwoch, 09.09.2026, 14:30 Uhr  

---

## Übersicht der 20 Folien

| # | Phase | Folientitel | Kernbotschaft / Visual |
|---|---|---|---|
| **01** | Intro | **Start & Willkommen** | Praxisaufgabe Conciliamus GmbH: Dieter Rüffler löst Business Partner Synchronisation mit SAP BTP Integration Suite |
| **02** | Intro | **Profil & Werte** | TU Berlin, ISTQB CTFL, ITIL V2 – Solide Ingenieurskunst & Cloud-Agilität |
| **03** | Kontext | **Conciliamus & Johannesstift Diakonie** | Resiliente Stammdaten für das Rückgrat der Gesundheitswirtschaft |
| **04** | Challenge | **Die Integrationsaufgabe** | MDM-Massenbatch trifft auf transaktionales S/4HANA OData |
| **05** | GitOps | **Serverless GitOps & BTP CORS-Bypass (ADR-006)** | Zero-Docker & Zero-Cost via GitHub & Streamlit Community Cloud |
| **06** | Architektur | **Das Dual-iFlow-Paradigma** | Strikte Trennung von Ingest/Transport und fachlicher Verarbeitung |
| **07** | Security | **Zero-Trust & BTP Cloud Security** | OAuth2 Client Credentials, HTTPS TLS 1.3, BTP Secure Store |
| **08** | Governance | **End-to-End Nachvollziehbarkeit** | Durchgängige Correlation-ID vom Inbound-Header bis zum Audit-Log |
| **09** | Deep Dive | **iFlow 1: Ingest & Iterating Splitter** | BPMN 2.0 Inbound-Pipeline & Streaming Splitter: 202 Quittierung und flaches RAM-Profil |
| **10** | Deep Dive | **iFlow 2: Item Processor** | `IFL_MDM_BP_Item_Processor`: Der atomare Einzelverarbeiter |
| **11** | Logik | **Idempotenz & Existenzprüfung** | OData GET `A_BusinessPartner`: Duplikatschutz durch semantische Keys |
| **12** | Protokoll | **Der CSRF- & Session-Handshake** | Two-Legged OData Call: Token & Cookie-Handling für POST & PATCH |
| **13** | Resilienz | **Dual-Channel Fehlerbehandlung** | Fachlicher Fehler (Audit Log) vs. Technischer Ausfall (Dead Letter Queue) |
| **14** | Qualität | **ISTQB-getriebenes Testing** | Systematischer 10er-Batch: 3x PATCH, 7x POST, Grenzwertanalyse |
| **15** | Beweis | **Live auf SAP BTP verifiziert** | Erfolgreicher End-to-End Durchlauf mit HTTP 200 OK am 04.09.2026 |
| **16** | Tooling | **Der Fiori-Lookalike Test-Runner** | Single-Viewport Web-App im authentischen SAP Fiori Horizon Look |
| **17** | Innovation | **Generative AI im SAP-Ökosystem** | Google OKF v0.2 & Gemini 3.6 Flash: Das Digital Brain des Architekten |
| **18** | Fit | **Mehrwert für Conciliamus & Dieter Rüffler** | Drei Säulen für den Teamerfolg: Architektur-Exzellenz, Methodenkompetenz, Innovationskraft |
| **19** | Glossar | **Das Enterprise Acronym Digest (150 Meilensteine, Frameworks & Standards)** | Vom SAP-Sprech zu solider Informatik: 150 Begriffe in 15×10-Matrix (inkl. Schickard 1623, Zuse Z1, ENIAC, Moore's Law, NeXT, Fiori/HTML5 & Walgesang-KI/Neurallingo), zweizeiligem Label-Layout (Jahr/Name), Toggleswitch (Chronologisch vs. A–Z), 32px-Festhöhe ohne Scrollbalken, Ausbleich-Filterung & Orange-Highlighter |
| **20** | Finale | **Überleitung in die Live-Demo** | Fragen, Fachgespräch & Live-Ausführung auf der BTP Cloud Integration |

---

## Detaillierter Ablauf & 20-Sekunden-Sprechertexte

### Folie 01: Start & Willkommen
* **Visuelles Motiv:** Hero-Card Dieter Rüffler mit verlinktem LinkedIn-Profil sowie anklickbare Showcase-Card zur Conciliamus-Praxisaufgabe mit originalem Deckblatt-Scan ([Praxisaufgabe PDF](https://firebasestorage.googleapis.com/v0/b/orcai-54321.firebasestorage.app/o/clients%2FACME%2Frecords%2FORCAI-260905-17H10-FILE-HSWWD%2FPraxisaufgabe%20%E2%80%93%20SAP%20Cloud%20Integration%20(SAP%20Integration%20Suite.pdf?alt=media&token=afecb33d-7bb0-4045-8bbe-579581fb67be)), Titel: *„Resiliente Business Partner Synchronisation“*, Untertitel: *„Lösungsarchitektur zur Praxisaufgabe der Conciliamus GmbH • Dieter Rüffler (SAP BTP & Integration Suite)“*.
* **Kernbotschaft:** Dieter Rüffler dokumentiert die fundierte Bearbeitung der Praxisaufgabe des potenziellen Arbeitgebers Conciliamus GmbH mit den Werkzeugen der SAP BTP & Integration Suite.
* **Sprechertext (20 Sek. / 55 Wörter):**
> „Guten Tag Herr Engelmann, hallo Team Conciliamus! Mein Name ist Dieter Rüffler. Diese Präsentation dokumentiert meine Lösungsarchitektur zu Ihrer Praxisaufgabe: die synchrone und asynchrone Anbindung von Business Partnern an SAP S/4HANA mit der SAP Integration Suite auf der BTP. In sechs Minuten und vierzig Sekunden zeige ich Ihnen Architektur, Mapping und Ausfallsicherheit – fundiert und praxiserprobt.“

---

### Folie 02: Profil, Ingenieurskunst & Zertifizierungen
* **Visuelles Motiv:** 4-teiliges Wappen- & Badge-Tableau: Spalte 1 mit interaktivem Scan der TU Berlin Diplom-Urkunde ([PDF](https://firebasestorage.googleapis.com/v0/b/orcai-54321.firebasestorage.app/o/clients%2FACME%2Frecords%2FORCAI-260905-20H00-FILE-N75WG%2FDieter-Rueffler-1991-Diplom-Informatiker-TU-Berlin.pdf?alt=media&token=675e2af4-6394-4e92-872b-1fc4c82ef0fc)), Spalte 2 mit originalem SAP Cloud Platform Integration Badge verlinkt auf Credly ([Credly Badge CPI](https://www.credly.com/badges/a5553b7e-8a58-4f09-b524-94f0befc2155)), Spalte 3 mit originalem SAP Process Orchestration 7.50 Badge verlinkt auf Credly ([Credly Badge PO](https://www.credly.com/badges/47280824-4ed5-4618-a502-e0f9de8c4696)), Spalte 4 mit ISTQB CTFL, ITIL V2 & AWS Certified Cloud Practitioner sowie offiziellem Credly-Verifikationslink ([credly.com/users/dieter-ruffler](https://www.credly.com/users/dieter-ruffler)).
* **Kernbotschaft:** Solide theoretische Informatik-Grundlagen gepaart mit offiziell verifizierten Zertifizierungen in Cloud Integration, Process Orchestration und Qualitätsmanagement.
* **Sprechertext (20 Sek. / 53 Wörter):**
> „Als Diplom-Informatiker der TU Berlin und zertifizierter SAP Cloud Platform Integration sowie Process Orchestration Specialist verbinde ich fundierte theoretische Grundlagen mit moderner Cloud-Praxis. Zusammen mit meinen Zertifizierungen in ISTQB CTFL, ITIL V2 und AWS bürge ich für kompromisslose Testdisziplin und betriebliche Stabilität – alles transparent auf Credly verifiziert.“

---

### Folie 03: Conciliamus & Johannesstift Diakonie
* **Visuelles Motiv:** Logo Johannesstift Diakonie gAG & Conciliamus GmbH, Organigramm Plattform & Integration, Bild eines modernen Klinikums.
* **Kernbotschaft:** IT in der Gesundheits- und Sozialwirtschaft verzeiht keine Datenfehler oder Systemstillstände.
* **Sprechertext (20 Sek. / 49 Wörter):**
> „Conciliamus bildet das technologische Rückgrat für Krankenhäuser, Pflege- und Sozialeinrichtungen der Johannesstift Diakonie. Hier geht es nicht um beliebige Datensätze – hinter jedem Geschäftspartner stehen Lieferanten lebenswichtiger Medizingüter oder Dienstleister. Ausfallzeiten oder inkonsistente Stammdaten haben direkte operative Auswirkungen. Deshalb steht bei mir Ausfallsicherheit und Nachvollziehbarkeit an allererster Stelle.“

---

### Folie 04: Die Integrationsaufgabe
* **Visuelles Motiv:** Quellsystem MDM (JSON-Batch mit 10 Geschäftspartnern) ➔ Pfeil mit Barriere ➔ Zielsystem SAP S/4HANA OData API.
* **Kernbotschaft:** Massen-Batches dürfen das transaktionale ERP-System niemals überlasten oder blockieren.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Die Aufgabenstellung: Ein zentrales MDM-System liefert Geschäftspartner als Batch-JSON an. Das Zielsystem, ein SAP S/4HANA Cloud, verlangt jedoch granulare OData-Aufrufe. Wie verhindern wir, dass ein einziger fehlerhafter Datensatz den gesamten Batch abbricht? Und wie schützen wir das ERP vor Lastspitzen? Die Antwort liegt in einer entkoppelten Integrationsarchitektur.“

---

### Folie 05: Serverless GitOps & BTP CORS-Bypass (ADR-006)
* **Visuelles Motiv:** Zweiteiliges Lösungs-Tableau: Links die automatisierte GitOps-Pipeline (`git push origin main` ➔ GitHub Webhook ➔ Streamlit Community Cloud in 20s, Zero-Docker, Zero-Cost) mit Direktverlinkung auf [ADR-006](https://github.com/gonzo42nixon/conciliamus-architecture-knowledge/blob/main/knowledge/decisions/adr-006-streamlit-cloud-agent-deployment.md); rechts die SAP BTP CORS-Bypass-Architektur (Browser-Preflight-Blockade HTTP 401 ❌ vs. serverseitige Python-Runtime HTTP 200/202 ✅).
* **Kernbotschaft:** Zero-Docker, Zero-Cost und Lösung des BTP-CORS-Dilemmas: Architekturwissen, KI-Agent und Testwerkzeuge kontinuierlich und sicher bereitstellen.
* **Sprechertext (20 Sek. / 52 Wörter):**
> „Mit ADR-006 lösen wir zwei zentrale Herausforderungen: Bereitstellungsaufwand und das berüchtigte SAP BTP CORS-Dilemma. Statt teurer Kubernetes-Cluster betreiben wir unseren Architecture Advisor serverlos via Streamlit Community Cloud direkt aus GitHub. Jeder Git-Push ist in zwanzig Sekunden weltweit live – und serverseitige Python-Calls umgehen die Browser-CORS-Blockade bei BTP-Aufrufen elegant und sicher.“

---

### Folie 06: Das Dual-iFlow-Paradigma
* **Visuelles Motiv:** Architekturdiagramm: iFlow 1 (`Batch_Receiver`) ➔ ProcessDirect ➔ iFlow 2 (`Item_Processor`).
* **Kernbotschaft:** Single Responsibility Principle: Trennung von Netzwerk-Ingest und fachlicher Verarbeitung.
* **Sprechertext (20 Sek. / 47 Wörter):**
> „Statt eines monolithischen Mammut-iFlows setze ich auf das bewährte Dual-iFlow-Pattern. Der erste Flow fungiert als schneller Empfänger und Entkoppler. Der zweite Flow übernimmt die fachliche Einzelverarbeitung. Gekoppelt werden beide über den hochperformanten, internen ProcessDirect-Adapter – absolut latenzfrei und ohne unnötige Netzwerk-Hops.“

---

### Folie 07: Zero-Trust & BTP Cloud Security
* **Visuelles Motiv:** BTP Shield-Icon & Security Dashboard Screenshot (vergrößerbar in Lightbox), direkte Verlinkung zum [BTP Cockpit Global Account](https://account.hanatrial.ondemand.com/trial/#/globalaccount/34eec884-0c14-4a9d-a509-55a912f83aee/accountModel&//?section=SubaccountsSection&view=TilesView) und dem [SAP Integration Suite Tenant](https://b9c123f3trial.integrationsuite-trial01.cfapps.us10-001.hana.ondemand.com/shell/home) (`b9c123f3trial`), flankiert von Security-Badges (OAuth2, TLS 1.3, XSUAA Service Keys).
* **Kernbotschaft:** Enterprise Security ab Sekunde Null – keine Klartext-Passwörter im Code, transparente Live-Tenant-Verifikation.
* **Sprechertext (20 Sek. / 46 Wörter):**
> „Sicherheit ist kein nachträgliches Feature. Der Inbound-Kanal ist über OAuth2 Client Credentials mit der BTP Service-Instanz abgesichert. Sensible Zielsystem-Schlüssel wie der Sandbox-API-Key liegen verschlüsselt im BTP Security Material Store. Selbst bei voller Einsicht in die iFlow-Artefakte verlassen vertrauliche Zugangsdaten zu keinem Zeitpunkt den gesicherten Tenant.“

---

### Folie 08: End-to-End Nachvollziehbarkeit & Governance
* **Visuelles Motiv:** Correlation-ID Header `SAP-CorrelationID`, Flow-Tracking vom HTTPS-Request über Groovy-Logger ins BTP Monitoring.
* **Kernbotschaft:** Lückenlose Rückverfolgbarkeit jedes einzelnen Datensatzes über Systemgrenzen hinweg.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Im Störfall zählt jede Minute. Unser Ingest-Flow generiert für jeden Aufruf eine eindeutige Correlation-ID, übernimmt bestehende Header und reicht sie an alle Einzelschritte weiter. Über maßgeschneiderte Groovy-Logger wird jeder Audit-Schritt im Message Processing Log festgehalten. Ein Support-Mitarbeiter findet so innerhalb von Sekunden den genauen Verarbeitungszustand jedes Partners.“

---

### Folie 09: iFlow 1 – Ingest & Iterating Splitter
* **Visuelles Motiv:** Zweiteiliges Tableau: Links der Screenshot des deployed iFlows `IFL_MDM_BP_Batch_Receiver` (HTTPS Inbound, JSON-to-XML Validierung, 202 Quittierung); rechts das Streaming-Speicherprofil (Monolith-Crash vs. stabile flache Streaming-Kurve &lt; 150 MB RAM).
* **Kernbotschaft:** Schnelle Entlastung des Aufrufers durch HTTP 202 und garantierter Out-of-Memory-Schutz durch streaming-orientierte Einzelverarbeitung.
* **Sprechertext (20 Sek. / 52 Wörter):**
> „Hier sehen Sie unseren Ingest-Flow IFL_MDM_BP_Batch_Receiver. Er nimmt den JSON-Batch entgegen, validiert das Schema und quittiert sofort mit HTTP 202 Accepted. Der integrierte Iterating Splitter streamt die Datensätze einzeln per In-Memory ProcessDirect an Flow 2 weiter – der Garbage Collector räumt sofort ab und der Speicherverbrauch bleibt dauerhaft unter 150 Megabyte.“

---

### Folie 10: iFlow 2 – Single Item Processor
* **Visuelles Motiv:** Screenshot des deployed iFlows `IFL_MDM_BP_Item_Processor` (ProcessDirect Inbound, Router, OData GET/POST/PATCH).
* **Kernbotschaft:** Der Business-Motor: Präzise OData-Synchronisation mit S/4HANA.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Der zweite iFlow, IFL_MDM_BP_Item_Processor, steuert die Interaktion mit SAP S/4HANA. Er empfängt den Einzelpartner, liest die externe Partnernummer und entscheidet dynamisch über den Verarbeitungszweig. Auch hier gilt Bruce Silvers Leitlinie: Klare visuelle Trennung zwischen Existenzprüfung, Neuanlage und Änderung – ohne verschachtelte Skript-Labyrinthe.“

---

### Folie 11: Idempotenz & Existenzprüfung
* **Visuelles Motiv:** OData GET `A_BusinessPartner?$filter=SearchTerm1 eq '...'`, Entscheidungsknoten: Partner existiert? (Ja/Nein).
* **Kernbotschaft:** Verlässlicher Duplikatschutz durch semantische Schlüsselprüfung vor jeder Schreiboperation.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Stammdaten-Schnittstellen müssen idempotent sein: Mehrfaches Einspielen desselben Payloads darf keine Dubletten erzeugen. Unser Processor führt daher zuerst einen OData-GET auf die BusinessPartner-Entität durch, gefiltert nach dem externen Suchbegriff. Finden wir den Partner, ermitteln wir die interne SAP-ID für das spätere Update. Finden wir ihn nicht, leiten wir die Neuanlage ein.“

---

### Folie 12: Der CSRF- & Session-Handshake
* **Visuelles Motiv:** Two-Legged Call Sequenzdiagramm: 1. `GET` mit `x-csrf-token: fetch` + `Set-Cookie` ➔ 2. `POST/PATCH` mit Token + Cookie.
* **Kernbotschaft:** Sichere OData V2/V4 Schreibzugriffe ohne Token-Verlust oder Session-Timeouts.
* **Sprechertext (20 Sek. / 52 Wörter):**
> „Jeder erfahrene SAP-Integrator weiß: Schreibende OData-Aufrufe scheitern in der Praxis oft an abgelaufenen CSRF-Tokens. Unser iFlow implementiert den Two-Legged-Handshake perfekt: Wir fordern im Vorfeld ein x-csrf-token an, speichern das Session-Cookie im Exchange-Property und übergeben beides synchron an den POST- bzw. PATCH-Aufruf. Das garantiert hundert Prozent fehlerfreie Transaktionen ohne Session-Abbrüche.“

---

### Folie 13: Dual-Channel Resilienz & Fehlerbehandlung
* **Visuelles Motiv:** Split in zwei Pfade: Roter Pfad (Fachlicher Fehler ➔ Audit-Log) vs. Gelber Pfad (Technischer Fehler ➔ Data Store DLQ).
* **Kernbotschaft:** Klare Unterscheidung zwischen ungültigen Geschäftsdaten und vorübergehenden Netzwerkausfällen (ADR-004).
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Resilienz bedeutet Differenzierung: Ein fachlicher Fehler – etwa eine ungültige PLZ – darf nicht in einer Endlos-Wiederholschleife landen. Er wandert direkt ins Audit-Log für die Fachabteilung. Ein technischer Fehler hingegen – etwa ein OData-Timeout – landet in einer Data Store Dead Letter Queue, wo er automatisiert oder manuell wiedereingesteuert werden kann.“

---

### Folie 14: ISTQB-getriebenes Testing
* **Visuelles Motiv:** ISTQB Logo, Matrix der 10 Testdatensätze: 3x PATCH (Bestandskunden), 7x POST (Neuanlagen), Grenzwert-Checks.
* **Kernbotschaft:** Systematisches Testen aller Äste vor dem ersten Go-Live.
* **Sprechertext (20 Sek. / 49 Wörter):**
> „Nach ISTQB-Methodik habe ich eine strukturierte Test-Suite mit zehn repräsentativen Datensätzen vorbereitet: Drei Partner existieren bereits in S/4HANA und testen den PATCH-Pfad auf Herz und Nieren. Sieben Partner sind Neuanlagen und prüfen die POST-Generierung. Hinzu kommen Sonderzeichen- und Längenprüfungen, um alle Randfälle und Äquivalenzklassen vollständig abzudecken.“

---

### Folie 15: Live auf SAP BTP verifiziert (HTTP 200)
* **Visuelles Motiv:** BTP Monitoring Screenshot: Status `COMPLETED`, HTTP 200 OK, Verarbeitungszeit 1.2s, 10 von 10 erfolgreich.
* **Kernbotschaft:** Theorie ist gut – funktionierender Live-Betrieb auf dem echten Tenant ist der Beweis.
* **Sprechertext (20 Sek. / 47 Wörter):**
> „Und hier ist der reale Beweis: Gestern um 16:45 Uhr haben wir den End-to-End-Lauf über den Live-Endpunkt unserer BTP-Trial-Umgebung in US East AWS gefahren. Das Ergebnis: HTTP 200 OK, Verarbeitungsdauer unter zwei Sekunden, alle zehn Geschäftspartner wurden punktgenau gemappt und fehlerfrei über die OData-Sandbox synchronisiert.“

---

### Folie 16: Der Fiori-Lookalike Test-Runner
* **Visuelles Motiv:** Mockup der erstellten Single-Viewport Web-App im SAP Fiori Horizon Lookalike-Design mit Fiori ShellBar, KPI-Kacheln, aufklappbaren RGB-JSON-Pills und aufgleitendem Monitoring-Drawer.
* **Kernbotschaft:** Leichtgewichtige Web-App im vertrauten Fiori-Design ohne Framework-Overhead – 100% Single-Viewport Ergonomie nach ADR-005.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Um Integration für alle Beteiligten greifbar zu machen, habe ich eine eigenständige Test-Runner Web-App im SAP Fiori Horizon Lookalike-Design entwickelt. Nach ADR-005 im strikten Single-Viewport-Layout: Keine störende Fensterscrollbar, interaktive farbige JSON-Pills für jeden Geschäftspartner und ein ausklappbarer Monitoring-Drawer. So können auch Fachbereichskollegen Testläufe eigenständig verifizieren.“

---

### Folie 17: Generative AI im SAP-Ökosystem
* **Visuelles Motiv:** Google Open Knowledge Format v0.2 Graph (28 Knoten, 72 Kanten), gekoppelt an Gemini 3.6 Flash & Streamlit Cloud.
* **Kernbotschaft:** Digital Brain des Architekten: Zero-Hallucination Architekturberatung quellenbasiert aus dem Projekt-Repository.
* **Sprechertext (20 Sek. / 53 Wörter):**
> „Als Autor des Kapitels ‚KI mit SAP‘ im Rheinwerk-Verlag denke ich Integration weiter. Das gesamte Architekturwissen dieser Lösung liegt im Google Open Knowledge Format v0.2 vor. Gekoppelt an Gemini 3.6 Flash und serverlos auf Streamlit Cloud bereitgestellt nach ADR-006, fungiert ein KI-Agent als ständiger Berater für mein Team – vollkommen faktenfest und quellenbasiert.“

---

### Folie 18: Mehrwert für Conciliamus & Dieter Rüffler
* **Visuelles Motiv:** Drei Säulen: 1. Architektur-Exzellenz (BTP & S/4HANA), 2. Methodenkompetenz (ISTQB, ITIL, Bruce Silver), 3. Innovationskraft (GenAI & Digital Brain).
* **Kernbotschaft:** Sofortige Entlastung im Tagesgeschäft, PI/PO-Migrationssicherheit und zukunftssichere Cloud-Architektur.
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Was bringe ich für Conciliamus mit? Erstens: Sofortige Entlastung bei der BTP- und S/4HANA-Migration durch zwanzig Jahre Schnittstellenerfahrung. Zweitens: Höchste Qualität durch ISTQB- und ITIL-Methodik. Und drittens: Einen Innovationsschub durch den gezielten Einsatz von generativer KI. Ich freue mich darauf, dieses Wissen in Ihr Team einzubringen.“

---

### Folie 19: Das Enterprise Acronym Digest (200 Meilensteine, Frameworks & Standards)
* **Visuelles Motiv:** Symmetrisches 20×10-Tableau (20 Zeilen à 10 Spalten = exakt 200 Pills, passend zur Pecha-Kucha-Dramaturgie aus 20 Folien, vollständig scrollbar-frei mit 0px Layout-Jumping und vollständiger vertikaler Raumausnutzung der Card-Höhe): Fester 128px Live-Inspector (`#digestInspector`) oben mit Gegenüberstellung *„SAP-Sprech vs. Informatik-Realität“*, dynamischer Impact-Badge (`#inspectImpact`, z. B. `🔥 Impact: 100/100 (Epochal)`) und Architektur-Layer-Badge (`#inspectLayer`, z. B. `🏗️ L4: Enterprise ERP & SAP BTP`). Alle 200 Pills besitzen ein konsistentes zweizeiliges Label-Layout mit fixer 28px Höhe: Zeile 1 zeigt das Meilensteinjahr (825–2030), Zeile 2 den Konzeptnamen. Enthält die Ursprünge der Informatik (Al-Chwarizmis Algorithmus 825, Schickards Rechenmaschine 1623, James Watts Industrialisierung 1784, Jacquard-Lochkarte 1805, Babbage Analytical Engine 1837, Ada Lovelace 1843, Hollerith-Maschine 1890), Industrie- und Krypto-Urknall (IBM Gründung 1911, Erster Weltkrieg & Funk/Logistik 1914, Zuse Z1 1938, HP Garage 1939, Zweiter Weltkrieg & Turing-Enigma 1939, ENIAC 1945, Zuse Plankalkül 1945, Bipolartransistor 1947, Claude Shannons Bit & Informationstheorie 1948, Norbert Wieners Kybernetik 1948, Alan Turings Test 1950), Netzwerk- & Rechnerpioniere (UNIX 1969, Codds SQL 1970, Dennis Ritchies C 1972, Bob Metcalfes Ethernet 1973, TCP/IP 1974, DNS 1983, Ciscos Multi-Protokoll-Router 1984, Netscape Navigator & Web-Boom 1994, Peter Shors Quanten-Algorithmus 1994), Firmengründungen (Microsoft 1975, Apple 1976, Oracle 1977, RSA Krypto 1977, Dell 1984, Lenovo 1984, Nvidia 1993, Amazon 1994, Google 1998, Alibaba 1999), den Beginn des Cloud-Computing (2006, Eric Schmidt / AWS), Nvidia CUDA GPU-Computing (2006), Bitcoin & Blockchain (2008), GitHub (2008), Zero-Trust-Architektur (2010), AlexNet & Deep-Learning-Urknall (2012), TypeScript (2012), Starlink LEO-Mesh (2019), Enterprise Application Integration (EAI 1998), Wikipedia (2001), Semantic Web (2001), Docker (2013) und Kubernetes (2014), HTML- und HTTP-Generationen, EU-Regulierungen & Cyber-Resilienz (DSGVO/GDPR 2018, Ukraine Cyberwar & Cloud-Migration 2022, NIS-2 Richtlinie 2024, DORA Resilienz 2025, EU AI Act 2024), frontier AI (DeepSeek 2024, OpenAI Codex 2025, Google Open Knowledge Format OKF 2026) und den inspirierenden Zukunftshorizont **General AI (AGI 2030+)**.
* **Interaktive 4-Wege-Steuerung:** Über einen vierstufigen interaktiven Toggle-Switch im Header kann wechselweise zwischen:
  1. **`📅 Chronologisch`** (nach Entstehungsjahr 825–2030),
  2. **`🔤 A–Z`** (strikt alphabetisch nach Konzeptname der zweiten Zeile),
  3. **`🔥 Impact`** (nach kalibriertem historischem Bedeutungsindex von 1 bis 100 sortiert, epochale Errungenschaften wie Transistor, Shannon Bit, UNIX, Ethernet, Algorithmus, WWW oder Cloud-Computing zuerst), und
  4. **`🏗️ Stack`** (nach den 7 klassischen Schichten der Enterprise-Architektur sortiert: Layer 1 Hardware ➔ Layer 2 OS & Netz ➔ Layer 3 Daten & APIs ➔ Layer 4 ERP & BTP ➔ Layer 5 UI & Frameworks ➔ Layer 6 Security & KRITIS ➔ Layer 7 KI & Frontier) umgeschaltet werden.
* **Filterung & Hervorhebung:** Interaktive Ausbleich-Filterung (`is-bleached` mit 18% Opazität statt `display:none`, Pills behalten ihre exakte Gitterposition) mit 8 Kategorien, kombiniert mit augenfälligem Orange-Highlighting (`#f97316` Hintergrund, schwarze fette Schrift) bei Hover/Klick.
* **Kernbotschaft:** Vom Marketing- und SAP-Sprech zu solider, transparenter Informatik – 200 Schlüsselbegriffe der IT-Geschichte und Enterprise-Architektur (von Al-Chwarizmi 825 über Bletchley Park, Shannon Bit, Ethernet, CUDA und Hyperscaler-Gründungen bis zu NIS-2, Google OKF 2026 und AGI 2030) entschlüsselt, wechselweise nach Zeitstrahl, Alphabet, historischem Impact oder Architektur-Stack sortierbar.
* **Sprechertext (20 Sek. / 54 Wörter):**
> „In zwanzig Jahren SAP-Integration habe ich gelernt: SAP benennt fundamentale Informatik gern mit eigenen Akronymen um. Dieses Digest entschlüsselt zweihundert Meilensteine – von der Industrialisierung über Bletchley Park und Ethernet bis zu NIS-2 und AGI 2030. Sortieren Sie nach Zeitstrahl, Alphabet, weltweitem Impact oder dem siebenschichtigen Architektur-Stack. Fahren Sie einfach mit der Maus darüber!“

---

### Folie 20: Diskussion & Live-Demo
* **Visuelles Motiv:** Grand Finale Cockpit (06:40 Punktlandung): Klickbare Buttons zu Fiori-Lookalike Test-Runner und Sprechertexten, Einladung an Markus Engelmann & Team zum Fachgespräch.
* **Kernbotschaft:** Nahtloser Übergang in das Fachgespräch und die Live-Ausführung.
* **Sprechertext (20 Sek. / 46 Wörter):**
> „Genau sechs Minuten und vierzig Sekunden. Ich bedanke mich herzlich für Ihre Aufmerksamkeit! Lassen Sie uns jetzt keine weiteren Folien ansehen, sondern live in die BTP-Integration Suite und unsere Fiori-Lookalike-Test-App springen. Herr Engelmann, die Bühne gehört Ihren Fragen – und ich drücke auf ‚Testsuite starten‘!“

---

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
* **Live-App Testrunner:** `http://localhost:8080` (oder `docs/test_runner_app.html`)
* **Live Pecha Kucha URL:** [https://orcai-54321.web.app/pecha-kucha.html](https://orcai-54321.web.app/pecha-kucha.html)
* **SAP BTP Cockpit:** [Trial Global Account & Subaccount Section](https://account.hanatrial.ondemand.com/trial/#/globalaccount/34eec884-0c14-4a9d-a509-55a912f83aee/accountModel&//?section=SubaccountsSection&view=TilesView)
* **SAP Integration Suite Tenant:** [Tenant b9c123f3trial Shell Home](https://b9c123f3trial.integrationsuite-trial01.cfapps.us10-001.hana.ondemand.com/shell/home)
* **GitHub Repository:** [gonzo42nixon/Conciliamus](https://github.com/gonzo42nixon/Conciliamus)
* **Live iFlow Batch Receiver:** [Google Photos Screenshot](https://photos.app.goo.gl/mfS9oN94KfUXJK6bA)
* **Live iFlow Item Processor:** [Google Photos Screenshot](https://photos.app.goo.gl/y8m8vH3BDCQG7whU8)
* **Bruce Silver Methodik:** [BPMN Method & Style](https://www.methodandstyle.com/books/bpmn-method-and-style/)
* **Rheinwerk Fachliteratur:** [KI mit SAP](https://www.rheinwerk-verlag.de/sap/ki-mit-sap/)
