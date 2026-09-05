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
| **05** | Methodik | **BPMN 2.0 Method & Style** | Bruce Silver Standard: Selbstdokumentierend [Aktiv-Verb] + [Objekt] |
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
| **17** | Tooling | **Fiori Horizon Test-Runner** | Single-Page Web-App mit Monitoring-Drawer für Fachbereich & Devs |
| **18** | Innovation | **Generative AI im SAP-Ökosystem** | Rheinwerk „KI mit SAP“: Schnittstellen-Auditing mit SAP Joule & LLMs |
| **19** | Fit | **Mehrwert für Conciliamus** | PI/PO-Migration beschleunigen, Plattform-Stabilität sichern, Team coachen |
| **20** | Finale | **Überleitung in die Live-Demo** | Fragen, Fachgespräch & Live-Ausführung auf der BTP Cloud Integration |

---

## Detaillierter Ablauf & 20-Sekunden-Sprechertexte

### Folie 01: Start & Willkommen
* **Visuelles Motiv:** Großes SAP BTP Logo, Porträt Dieter Rüffler, Titel: *„Resiliente Business Partner Synchronisation auf SAP BTP“*.
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

### Folie 05: Methodik – Bruce Silver „BPMN Method & Style“
* **Visuelles Motiv:** Buchcover Bruce Silver 2nd Edition, Schema: *[Aktiv-Verb] + [Objekt]* für Tasks, *[Zustand]* für Events, schraffierte Default-Gateways.
* **Kernbotschaft:** Lesbare, selbstdokumentierende Integrationsflüsse statt unübersichtlicher Spaghetti-Modelle.
* **Sprechertext (20 Sek. / 51 Wörter):**
> „Gute Architektur beginnt bei der Notation. Ich modelliere konsequent nach Bruce Silvers BPMN 2.0 Method & Style. Jeder Schritt folgt der Sprachform ‚Aktiv-Verb plus Objekt‘ – etwa ‚Existenz prüfen‘ oder ‚Delta patchen‘. Das schafft absolute Klarheit: Entwickler, Administratoren und der Fachbereich verstehen den iFlow sofort auf den ersten Blick, ohne Handbücher wälzen zu müssen.“

---

### Folie 06: Das Dual-iFlow-Paradigma
* **Visuelles Motiv:** Architekturdiagramm: iFlow 1 (`Batch_Receiver`) ➔ ProcessDirect ➔ iFlow 2 (`Item_Processor`).
* **Kernbotschaft:** Single Responsibility Principle: Trennung von Netzwerk-Ingest und fachlicher Verarbeitung.
* **Sprechertext (20 Sek. / 47 Wörter):**
> „Statt eines monolithischen Mammut-iFlows setze ich auf das bewährte Dual-iFlow-Pattern. Der erste Flow fungiert als schneller Empfänger und Entkoppler. Der zweite Flow übernimmt die fachliche Einzelverarbeitung. Gekoppelt werden beide über den hochperformanten, internen ProcessDirect-Adapter – absolut latenzfrei und ohne unnötige Netzwerk-Hops.“

---

### Folie 07: Zero-Trust & BTP Cloud Security
* **Visuelles Motiv:** BTP Shield-Icon, OAuth2 Client Credentials Flow, Secure Parameter `SANDBOX_API_KEY` im BTP Keystore.
* **Kernbotschaft:** Enterprise Security ab Sekunde Null – keine Klartext-Passwörter im Code.
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

### Folie 17: Der SAP Fiori Horizon Test-Runner
* **Visuelles Motiv:** Screenshot der erstellten Web-App mit Fiori ShellBar, KPI-Kacheln und aufgleitendem Monitoring-Drawer.
* **Kernbotschaft:** Entwickler-Werkzeuge dürfen modern, zugänglich und intuitiv sein.
* **Sprechertext (20 Sek. / 50 Wörter):**
> „Um diesen Test jederzeit transparent wiederholbar zu machen, habe ich eine Single-Page Web-App im modernen SAP Fiori Horizon Design gebaut. Mit einem Klick triggert sie den OAuth2-Handshake, feuert den Batch und zeigt die Antwortkarten, Handshake-Logs und Rohdaten in einem eleganten Fiori-Side-Drawer an – ganz ohne Konsolen-Chaos.“

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
* **Visuelles Motiv:** Einladung zur Live-Demo: Klick auf „Testsuite starten“, QR-Code / Links zu GitHub, BTP & Fiori App.
* **Kernbotschaft:** Nahtloser Übergang in das Fachgespräch und die Live-Ausführung.
* **Sprechertext (20 Sek. / 46 Wörter):**
> „Genau sechs Minuten und vierzig Sekunden. Ich bedanke mich herzlich für Ihre Aufmerksamkeit! Lassen Sie uns jetzt keine weiteren Folien ansehen, sondern live in die BTP-Integration Suite und unsere Fiori-Test-App springen. Herr Engelmann, die Bühne gehört Ihren Fragen – und ich drücke auf ‚Testsuite starten‘!“

---

## Technische Referenzen & Begleitdokumente
* **Live-App Testrunner:** `http://localhost:8080` (oder `docs/test_runner_app.html`)
* **GitHub Repository:** [gonzo42nixon/Conciliamus](https://github.com/gonzo42nixon/Conciliamus)
* **Live iFlow Batch Receiver:** [Google Photos Screenshot](https://photos.app.goo.gl/mfS9oN94KfUXJK6bA)
* **Live iFlow Item Processor:** [Google Photos Screenshot](https://photos.app.goo.gl/y8m8vH3BDCQG7whU8)
* **Bruce Silver Methodik:** [BPMN Method & Style](https://www.methodandstyle.com/books/bpmn-method-and-style/)
* **Rheinwerk Fachliteratur:** [KI mit SAP](https://www.rheinwerk-verlag.de/sap/ki-mit-sap/)
