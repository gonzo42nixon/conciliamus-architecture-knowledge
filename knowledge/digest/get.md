---
id: digest/get
type: Architecture Concept
title: "HTTP GET (RFC 9110)"
description: "Sichere, idempotente HTTP-Standardmethode für Leseabfragen ohne zustandsändernde Seiteneffekte."
resource: btp://conciliamus/digest/get
tags: ["digest","concept","http-verb","web-ui-frameworks","year-1991"]
status: verified
layer: 5
impact: 82
category: "HTTP-Verb"
year: "1991"
generated:
  by: "human:dieter-rueffler"
  at: "2026-09-07T13:00:00Z"
---

# HTTP GET (RFC 9110)

## Begriff & Technische Einordnung
- **Akronym / Begriff:** `GET`
- **Meilenstein / Epoche:** Jahr 1991
- **Kategorie:** `HTTP-Verb`
- **Architektur-Ebene:** `Layer 5: Web, UI & Frameworks`
- **Impact-Score:** `82 / 100`

## Bedeutung in der SAP-Welt
OData V2 GET Call (A_BusinessPartner?=SearchTerm1 eq ...) für die Existenzprüfung

## Fundamentale technische Bedeutung (Real World)
Sichere, idempotente HTTP-Standardmethode für Leseabfragen ohne zustandsändernde Seiteneffekte.

## Kontext & Praxisbezug (BTP Integration Suite / Conciliamus)
Kern unserer Idempotenz-Prüfung in Folie 11: Ermittelt, ob Partner existiert (Count == 0 vs. 1).
