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
| **01** | Intro | **Start & Willkommen** | Dieter Rüffler: 20 Jahre Integrationsexpertise trifft moderne SAP BTP |
| **02** | Intro | **Profil & Werte** | TU Berlin, ISTQB CTFL, ITIL V2 – Solide Ingenieurskunst & Cloud-Agilität |
| **03** | Kontext | **Conciliamus & Johannesstift Diakonie** | Resiliente Stammdaten für das Rückgrat der Gesundheitswirtschaft |
| **04** | Challenge | **Die Integrationsaufgabe** | MDM-Massenbatch trifft auf transaktionales S/4HANA OData |
| **05** | GitOps | **Serverless GitOps & BTP CORS-Bypass (ADR-006)** | Zero-Docker & Zero-Cost via GitHub & Streamlit Community Cloud |
| **06** | Architektur | **Das Dual-iFlow-Paradigma** | Strikte Trennung von Ingest/Transport und fachlicher Verarbeitung |
| **07** | Security | **Zero-Trust & BTP Cloud Security** | OAuth2 Client Credentials, HTTPS TLS 1.3, BTP Secure Store |
| **08** | Governance | **End-to-End Nachvollziehbarkeit** | Durchgängige Correlation-ID vom Inbound-Header bis zum Audit-Log |
| **09** | Deep Dive | **iFlow 1: Ingest & Entkopplung** | `IFL_MDM_BP_Batch_Receiver`: Schneller Handshake & Validierung |
| **10** | Deep Dive | **Der Iterating Splitter** | Schonende Entpackung von 10 Partnern ohne Speicherüberlastung |
| **11** | Deep Dive | **iFlow 2: Item Processor** | `IFL_MDM_BP_Item_Processor`: Der atomare Einzelverarbeiter |
| **12** | Logik | **Idempotenz & Existenzprüfung** | OData GET `A_BusinessPartner`: Duplikatschutz durch semantische Keys |
| **13** | Protokoll | **Der CSRF- & Session-Handshake** | Two-Legged OData Call: Token & Cookie-Handling für POST & PATCH |
| **14** | Resilienz | **Dual-Channel Fehlerbehandlung** | Fachlicher Fehler (Audit Log) vs. Technischer Ausfall (Dead Letter Queue) |
| **15** | Qualität | **ISTQB-getriebenes Testing** | Systematischer 10er-Batch: 3x PATCH, 7x POST, Grenzwertanalyse |
| **16** | Beweis | **Live auf SAP BTP verifiziert** | Erfolgreicher End-to-End Durchlauf mit HTTP 200 OK am 04.09.2026 |
| **17** | Tooling | **Der Fiori-Lookalike Test-Runner** | Single-Viewport Web-App im authentischen SAP Fiori Horizon Look |
| **18** | Innovation | **Generative AI im SAP-Ökosystem** | Rheinwerk „KI mit SAP“: Schnittstellen-Auditing mit SAP Joule & LLMs |
| **19** | Fit | **Mehrwert für Conciliamus** | PI/PO-Migration beschleunigen, Plattform-Stabilität sichern, Team coachen |
| **20** | Finale | **Überleitung in die Live-Demo** | Fragen, Fachgespräch & Live-Ausführung auf der BTP Cloud Integration |

---

## Detaillierter Ablauf & 20-Sekunden-Sprechertexte

### Folie 01: Start & Willkommen
* **Visuelles Motiv:** Hero-Card Dieter Rüffler mit verlinktem offiziellen LinkedIn-Badge ([linkedin.com/in/dieter-rueffler-05981623b](https://www.linkedin.com/in/dieter-rueffler-05981623b/)), BTP Cloud Integration Visual Node (`b9c123f3trial`), Titel: *„Resiliente Business Partner Synchronisation auf SAP BTP“*.
* **Kernbotschaft:** Moderne Enterprise-Integration erfordert mehr als Code – sie braucht Erfahrung, Methodik und Ausfallsicherheit.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Guten Tag Herr Engelmann, hallo Team Conciliamus! Mein Name ist Dieter Rüffler. Ich verbinde über zwanzig Jahre gewachsene SAP-Integrationserfahrung mit den modernen Möglichkeiten der SAP Business Technology Platform. In den nächsten sechs Minuten und vierzig Sekunden zeige ich Ihnen, wie wir Stammdaten hochverfügbar, idempotent und methodisch sauber nach S/4HANA synchronisieren.“

---

### Folie 02: Profil, Ingenieurskunst & Zertifizierungen
* **Visuelles Motiv:** 4-teiliges Wappen- & Badge-Tableau: TU Berlin Diplom-Informatiker (2005), originale Credly-Badges für *SAP Certified Application Associate - Cloud Platform Integration*, *SAP Certified Technology Associate - Process Orchestration 7.50* und *AWS Certified Cloud Practitioner*, flankiert von ISTQB CTFL & ITIL V2 sowie offiziellem Credly-Verifikationslink ([credly.com/users/dieter-ruffler](https://www.credly.com/users/dieter-ruffler)).
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

### Folie 09: iFlow 1 – Ingest & Entkopplung
* **Visuelles Motiv:** Screenshot des deployed iFlows `IFL_MDM_BP_Batch_Receiver` (HTTPS Inbound, Groovy Validator, Splitter).
* **Kernbotschaft:** Schnelle Entlastung des Aufrufers und syntaktische Vorprüfung der Nutzlast.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Hier sehen Sie den ersten iFlow: IFL_MDM_BP_Batch_Receiver, deployed auf unserem BTP-Tenant. Er empfängt den JSON-Batch über HTTPS, prüft die Header-Struktur und validiert das JSON-Schema. Entspricht der Payload nicht der Spezifikation, wird der Aufruf sofort mit einem klaren HTTP 400 abgewiesen, bevor interne Ressourcen beansprucht werden.“

---

### Folie 10: Der Iterating Splitter
* **Visuelles Motiv:** Splitter-Icon, Visualisierung eines Arrays von 10 JSON-Objekten, die sequenziell an ProcessDirect übergeben werden.
* **Kernbotschaft:** Schutz vor Out-of-Memory Fehlern durch kontrollierte Einzelstrom-Verarbeitung.
* **Sprechertext (20 Sek. / 49 Wörter):**
> „Das Herzstück des ersten Flows ist der Iterating Splitter. Er zerlegt das JSON-Array in zehn eigenständige Datensätze. Dadurch bleibt der Speicherbedarf auf der Worker-Node minimal – selbst bei Tausenden von Partnern. Jeder Partner wird einzeln isoliert und deterministisch an den Item-Processor übergeben. Fehler schlagen so niemals auf Nachbardatensätze durch.“

---

### Folie 11: iFlow 2 – Single Item Processor
* **Visuelles Motiv:** Screenshot des deployed iFlows `IFL_MDM_BP_Item_Processor` (ProcessDirect Inbound, Router, OData GET/POST/PATCH).
* **Kernbotschaft:** Der Business-Motor: Präzise OData-Synchronisation mit S/4HANA.
* **Sprechertext (20 Sek. / 48 Wörter):**
> „Der zweite iFlow, IFL_MDM_BP_Item_Processor, steuert die Interaktion mit SAP S/4HANA. Er empfängt den Einzelpartner, liest die externe Partnernummer und entscheidet dynamisch über den Verarbeitungszweig. Auch hier gilt Bruce Silvers Leitlinie: Klare visuelle Trennung zwischen Existenzprüfung, Neuanlage und Änderung – ohne verschachtelte Skript-Labyrinthe.“

---

### Folie 12: Idempotenz & Existenzprüfung
* **Visuelles Motiv:** OData GET `A_BusinessPartner?$filter=SearchTerm1 eq '...'`, Entscheidungsknoten: Partner existiert? (Ja/Nein).
* **Kernbotschaft:** Verlässlicher Duplikatschutz durch semantische Schlüsselprüfung vor jeder Schreiboperation.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Stammdaten-Schnittstellen müssen idempotent sein: Mehrfaches Einspielen desselben Payloads darf keine Dubletten erzeugen. Unser Processor führt daher zuerst einen OData-GET auf die BusinessPartner-Entität durch, gefiltert nach dem externen Suchbegriff. Finden wir den Partner, ermitteln wir die interne SAP-ID für das spätere Update. Finden wir ihn nicht, leiten wir die Neuanlage ein.“

---

### Folie 13: Der CSRF- & Session-Handshake
* **Visuelles Motiv:** Two-Legged Call Sequenzdiagramm: 1. `GET` mit `x-csrf-token: fetch` + `Set-Cookie` ➔ 2. `POST/PATCH` mit Token + Cookie.
* **Kernbotschaft:** Sichere OData V2/V4 Schreibzugriffe ohne Token-Verlust oder Session-Timeouts.
* **Sprechertext (20 Sek. / 52 Wörter):**
> „Jeder erfahrene SAP-Integrator weiß: Schreibende OData-Aufrufe scheitern in der Praxis oft an abgelaufenen CSRF-Tokens. Unser iFlow implementiert den Two-Legged-Handshake perfekt: Wir fordern im Vorfeld ein x-csrf-token an, speichern das Session-Cookie im Exchange-Property und übergeben beides synchron an den POST- bzw. PATCH-Aufruf. Das garantiert hundert Prozent fehlerfreie Transaktionen ohne Session-Abbrüche.“

---

### Folie 14: Dual-Channel Resilienz & Fehlerbehandlung
* **Visuelles Motiv:** Split in zwei Pfade: Roter Pfad (Fachlicher Fehler ➔ Audit-Log) vs. Gelber Pfad (Technischer Fehler ➔ Data Store DLQ).
* **Kernbotschaft:** Klare Unterscheidung zwischen ungültigen Geschäftsdaten und vorübergehenden Netzwerkausfällen.
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Resilienz bedeutet Differenzierung: Ein fachlicher Fehler – etwa eine ungültige PLZ – darf nicht in einer Endlos-Wiederholschleife landen. Er wandert direkt ins Audit-Log für die Fachabteilung. Ein technischer Fehler hingegen – etwa ein OData-Timeout – landet in einer Data Store Dead Letter Queue, wo er automatisiert oder manuell wiedereingesteuert werden kann.“

---

### Folie 15: ISTQB-getriebenes Testing
* **Visuelles Motiv:** ISTQB Logo, Matrix der 10 Testdatensätze: 3x PATCH (Bestandskunden), 7x POST (Neuanlagen), Grenzwert-Checks.
* **Kernbotschaft:** Systematisches Testen aller Äste vor dem ersten Go-Live.
* **Sprechertext (20 Sek. / 49 Wörter):**
> „Nach ISTQB-Methodik habe ich eine strukturierte Test-Suite mit zehn repräsentativen Datensätzen vorbereitet: Drei Partner existieren bereits in S/4HANA und testen den PATCH-Pfad auf Herz und Nieren. Sieben Partner sind Neuanlagen und prüfen die POST-Generierung. Hinzu kommen Sonderzeichen- und Längenprüfungen, um alle Randfälle und Äquivalenzklassen vollständig abzudecken.“

---

### Folie 16: Live auf SAP BTP verifiziert (HTTP 200)
* **Visuelles Motiv:** BTP Monitoring Screenshot: Status `COMPLETED`, HTTP 200 OK, Verarbeitungszeit 1.2s, 10 von 10 erfolgreich.
* **Kernbotschaft:** Theorie ist gut – funktionierender Live-Betrieb auf dem echten Tenant ist der Beweis.
* **Sprechertext (20 Sek. / 47 Wörter):**
> „Und hier ist der reale Beweis: Gestern um 16:45 Uhr haben wir den End-to-End-Lauf über den Live-Endpunkt unserer BTP-Trial-Umgebung in US East AWS gefahren. Das Ergebnis: HTTP 200 OK, Verarbeitungsdauer unter zwei Sekunden, alle zehn Geschäftspartner wurden punktgenau gemappt und fehlerfrei über die OData-Sandbox synchronisiert.“

---

### Folie 17: Der Fiori-Lookalike Test-Runner
* **Visuelles Motiv:** Mockup der erstellten Single-Viewport Web-App im SAP Fiori Horizon Lookalike-Design mit Fiori ShellBar, KPI-Kacheln, aufklappbaren RGB-JSON-Pills und aufgleitendem Monitoring-Drawer.
* **Kernbotschaft:** Leichtgewichtige Web-App im vertrauten Fiori-Design ohne Framework-Overhead – 100% Single-Viewport Ergonomie nach ADR-005.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Um Integration für alle Beteiligten greifbar zu machen, habe ich eine eigenständige Test-Runner Web-App im SAP Fiori Horizon Lookalike-Design entwickelt. Nach ADR-005 im strikten Single-Viewport-Layout: Keine störende Fensterscrollbar, interaktive farbige JSON-Pills für jeden Geschäftspartner und ein ausklappbarer Monitoring-Drawer. So können auch Fachbereichskollegen Testläufe eigenständig verifizieren.“

---

### Folie 18: Generative AI & Moderne Integration
* **Visuelles Motiv:** Rheinwerk-Buch „KI mit SAP“, SAP Joule Icon, Schnittstellen-Dokumentation & Code-Generierung.
* **Kernbotschaft:** Traditionelle Integrationserfahrung multipliziert sich durch den gezielten Einsatz von Generativer KI.
* **Sprechertext (20 Sek. / 53 Wörter):**
> „Enterprise-Integration steht vor dem nächsten großen Evolutionssprung. Durch Generative AI, SAP Joule und LLM-gestützte Entwicklungs-Agenten können wir Groovy-Mappings beschleunigen, Testdaten synthetisieren und Schnittstellendokumentationen automatisiert pflegen. Wie Rheinwerks Fachbuchreihe ‚KI mit SAP‘ betont, geht es darum, fundiertes Architekturwissen durch KI als Produktivitäts-Multiplikator zu verstärken – genau das habe ich in diesem Projekt demonstriert.“

---

### Folie 19: Warum Conciliamus & Dieter Rüffler?
* **Visuelles Motiv:** Drei Säulen: 1. Plattform-Stabilität, 2. PI/PO-Migrationserfahrung, 3. Team-Coaching & Kultur.
* **Kernbotschaft:** Sofortige Entlastung im Tagesgeschäft und strategischer Weitblick für die BTP-Roadmap.
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Warum passe ich zu Conciliamus? Ich kenne die realen Herausforderungen gewachsener SAP PI/PO-Landschaften und weiß genau, wie man sie schrittweise und ohne Betriebsunterbrechung auf die BTP migriert. Ich bringe Ruhe und Verlässlichkeit in komplexe Schnittstellenprojekte und freue mich darauf, mein Wissen im Team von Herrn Engelmann kollegial weiterzugeben.“

---

### Folie 20: Diskussion & Live-Demo
* **Visuelles Motiv:** Einladung zur Live-Demo: Klick auf „Fiori-Lookalike Test-Runner starten“, QR-Code / Links zu GitHub, BTP & Fiori-Lookalike App.
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
